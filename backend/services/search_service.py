import httpx
import asyncio
from typing import List, Dict, Any
from config import SERPER_API_KEY, REGIONS
import logging

logger = logging.getLogger(__name__)

SERPER_SHOPPING_ENDPOINT = "https://google.serper.dev/shopping"
RESULTS_PER_QUERY = 20
MAX_RESULTS_PER_REGION = 20


def _build_queries(ingredients: str, region_key: str) -> List[str]:
    """
    Build queries based solely on ingredients.
    Each region gets language-appropriate queries.
    """
    parts = [i.strip() for i in ingredients.split(",") if i.strip()]
    first = parts[0] if parts else ""
    top2 = " ".join(parts[:2])
    top3 = " ".join(parts[:3])

    if region_key == "CZ":
        return [
            f"{first} doplněk stravy koupit",
            f"{first} kapsle tablety cena",
            f"{top2} doplněk stravy",
            f"{top3} kapsle koupit",
        ]
    elif region_key == "EU":
        return [
            f"{first} supplement buy",
            f"{first} capsules supplement",
            f"{top2} supplement capsules",
            f"{top3} supplement buy",
        ]
    else:  # USA
        return [
            f"{first} supplement capsules buy",
            f"best {first} supplement",
            f"{top2} supplement buy",
            f"{top3} capsules supplement",
        ]


async def _search_shopping(query: str, region: Dict, client: httpx.AsyncClient) -> List[Dict]:
    try:
        response = await client.post(
            SERPER_SHOPPING_ENDPOINT,
            headers={
                "X-API-KEY": SERPER_API_KEY,
                "Content-Type": "application/json",
            },
            json={
                "q": query,
                "gl": region["gl"],
                "hl": region["hl"],
                "num": RESULTS_PER_QUERY,
            }
        )
        response.raise_for_status()
        results = response.json().get("shopping", [])
        logger.info(f"  '{query}' → {len(results)} results")
        return results
    except httpx.HTTPStatusError as e:
        logger.error(f"Serper error: {e.response.status_code} - {e.response.text}")
        return []
    except Exception as e:
        logger.error(f"Shopping search error: {e}")
        return []


async def search_competitors(ingredients: str, region_key: str) -> List[Dict[str, Any]]:
    region = REGIONS[region_key]
    queries = _build_queries(ingredients, region_key)
    logger.info(f"[{region_key}] Running {len(queries)} queries...")

    async with httpx.AsyncClient(timeout=15.0) as client:
        all_batches = await asyncio.gather(*[_search_shopping(q, region, client) for q in queries])

    all_results = [r for batch in all_batches for r in batch]

    seen = set()
    unique = []
    for r in all_results:
        key = r.get("link") or r.get("title", "")
        if key and key not in seen:
            seen.add(key)
            unique.append(r)

    logger.info(f"[{region_key}] {len(unique)} unique products after dedup")
    return unique[:MAX_RESULTS_PER_REGION]


async def search_all_regions(ingredients: str) -> Dict[str, List[Dict]]:
    cz, eu, usa = await asyncio.gather(
        search_competitors(ingredients, "CZ"),
        search_competitors(ingredients, "EU"),
        search_competitors(ingredients, "USA"),
    )
    return {"CZ": cz, "EU": eu, "USA": usa}
