import re
import asyncio
import httpx
from bs4 import BeautifulSoup
from typing import Optional, Dict, List
from config import REGIONS
import logging
import json

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9,cs;q=0.8",
}

# Max plausible price per region (sanity check)
MAX_PRICE = {"CZ": 5000.0, "EU": 300.0, "USA": 300.0}
MIN_PRICE = {"CZ": 50.0, "EU": 2.0, "USA": 2.0}

REVIEW_PATTERNS = [
    r'(\d[\d,]+)\s*(?:global ratings|customer reviews)',
    r'(\d[\d,]+)\s*(?:verified reviews|verified ratings)',
    r'(\d[\d,]+)\s*(?:star ratings|star reviews)',
    r'(\d[\d,]+)\s*hodnocení',
    r'(\d[\d,]+)\s*recenzí',
    r'(\d[\d,]+)\s*Bewertungen',
]


def _parse_price(raw: str) -> Optional[float]:
    """Parse price string like '$29.99', '29,99 €', '1.299,00 Kč'."""
    if not raw:
        return None
    s = str(raw).strip()
    # European: 1.299,00 → remove dot thousands separator, replace comma decimal
    if re.search(r'\d{1,3}\.\d{3},\d{2}', s):
        s = s.replace('.', '').replace(',', '.')
    # Simple comma decimal: 29,99
    elif re.match(r'^[^\d]*\d+,\d{2}[^\d]*$', s):
        s = s.replace(',', '.')
    # Remove all non-numeric except dot
    cleaned = re.sub(r'[^\d.]', '', s)
    try:
        val = float(cleaned)
        return val if val > 0 else None
    except ValueError:
        return None


def _extract_reviews_from_text(text: str) -> Optional[int]:
    for pattern in REVIEW_PATTERNS:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            raw = match.group(1).replace(",", "").replace(".", "").replace(" ", "")
            try:
                val = int(raw)
                if 0 < val < 10_000_000:
                    return val
            except ValueError:
                continue
    return None


def _extract_from_jsonld(soup: BeautifulSoup) -> tuple[Optional[float], Optional[int]]:
    price, reviews = None, None
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(script.string or "")
            items = data if isinstance(data, list) else [data]
            for item in items:
                if not isinstance(item, dict):
                    continue
                agg = item.get("aggregateRating", {})
                if not reviews:
                    rc = agg.get("reviewCount") or agg.get("ratingCount")
                    if rc:
                        try:
                            reviews = int(str(rc).replace(",", "").split(".")[0])
                        except Exception:
                            pass
                if not price:
                    offers = item.get("offers") or item.get("Offers") or {}
                    if isinstance(offers, list):
                        offers = offers[0] if offers else {}
                    p = offers.get("price") or offers.get("lowPrice")
                    if p:
                        try:
                            price = float(str(p).replace(",", ""))
                        except Exception:
                            pass
                if price and reviews:
                    break
        except Exception:
            continue
        if price and reviews:
            break
    return price, reviews


async def _fetch_reviews(url: str) -> Optional[int]:
    """Fetch product page just to get review count."""
    try:
        async with httpx.AsyncClient(timeout=10.0, follow_redirects=True, headers=HEADERS) as client:
            response = await client.get(url)
            if response.status_code != 200:
                return None
            soup = BeautifulSoup(response.text, "html.parser")

            # 1. JSON-LD
            _, reviews = _extract_from_jsonld(soup)
            if reviews:
                return reviews

            # 2. Full page text
            return _extract_reviews_from_text(soup.get_text(" ", strip=True))
    except Exception as e:
        logger.warning(f"Failed to fetch reviews from {url}: {e}")
        return None


async def parse_search_result(result: Dict, region_key: str) -> Dict:
    """
    Parse a Serper Shopping result.
    Shopping results already contain price and often ratingCount directly.
    """
    region = REGIONS[region_key]
    title = result.get("title", "Unknown Product")
    link = result.get("link", "")
    source = result.get("source", "")

    # --- Price: directly from Shopping result ---
    price_raw = result.get("price", "")
    price = _parse_price(str(price_raw)) if price_raw else None

    # Sanity check price
    if price:
        if price > MAX_PRICE[region_key] or price < MIN_PRICE[region_key]:
            logger.info(f"Price {price} out of range for {region_key}, discarding: {title}")
            price = None

    # --- Reviews: directly from Shopping result ---
    reviews = None
    rating_count = result.get("ratingCount") or result.get("reviewCount")
    if rating_count:
        try:
            reviews = int(str(rating_count).replace(",", "").split(".")[0])
        except Exception:
            pass

    # Rating
    rating = result.get("rating")
    if rating:
        try:
            rating = float(rating)
        except Exception:
            rating = None

    # --- Fetch page if reviews still missing ---
    if reviews is None and link:
        logger.info(f"Fetching page for reviews: {link}")
        reviews = await _fetch_reviews(link)

    price_found = price is not None
    reviews_found = reviews is not None

    return {
        "name": title[:80],
        "url": link,
        "snippet": source,
        "price": round(price, 2) if price else None,
        "reviews": reviews,           # None = not found, no fallback
        "rating": rating,
        "region": region_key,
        "currency": region["currency"],
        "price_found": price_found,
        "reviews_found": reviews_found,
    }


async def parse_all_results(results_by_region: Dict[str, List[Dict]]) -> Dict[str, List[Dict]]:
    """Parse all shopping results concurrently."""
    parsed = {}
    for region_key, results in results_by_region.items():
        tasks = [parse_search_result(r, region_key) for r in results]
        parsed[region_key] = list(await asyncio.gather(*tasks))
    return parsed
