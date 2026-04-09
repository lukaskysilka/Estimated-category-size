from typing import List, Dict, Any
from config import REVIEWS_TO_SALES_RATIO, REGIONS
from services.currency_service import fetch_usd_rates, get_usd_rate
import logging

logger = logging.getLogger(__name__)


def estimate_product_market(product: Dict, usd_rates: Dict[str, float]) -> Dict:
    """Calculate estimated sales and revenue for one product using live rates."""
    reviews = product.get("reviews") or 0
    price = product.get("price") or 0
    region_key = product.get("region", "USA")
    currency = product.get("currency", "USD")

    estimated_sales = reviews * REVIEWS_TO_SALES_RATIO
    revenue_local = estimated_sales * price
    revenue_usd = revenue_local * get_usd_rate(currency, usd_rates)

    return {
        **product,
        "estimated_sales": estimated_sales,
        "revenue_local": round(revenue_local, 2),
        "revenue_usd": round(revenue_usd, 2),
    }


async def aggregate_market_size(products_by_region: Dict[str, List[Dict]]) -> Dict[str, Any]:
    """
    Aggregate market size estimation across all regions using live exchange rates.
    """
    # Fetch live rates once for the whole calculation
    usd_rates = await fetch_usd_rates()
    logger.info(f"Using rates: {usd_rates}")

    region_summaries = {}
    total_usd = 0.0
    all_competitors = []

    for region_key, products in products_by_region.items():
        region_cfg = REGIONS[region_key]

        # Only include products with REAL reviews and price found
        real_products = [p for p in products if p.get("reviews_found") and p.get("price_found")]
        enriched = [estimate_product_market(p, usd_rates) for p in real_products]
        enriched.sort(key=lambda x: x["revenue_usd"], reverse=True)

        total_local = sum(p["revenue_local"] for p in enriched)
        total_region_usd = sum(p["revenue_usd"] for p in enriched)
        total_usd += total_region_usd

        region_summaries[region_key] = {
            "region": region_key,
            "currency": region_cfg["currency"],
            "currency_symbol": region_cfg["currency_symbol"],
            "total_local": round(total_local, 2),
            "total_usd": round(total_region_usd, 2),
            "product_count": len(enriched),
            "avg_price": round(sum(p["price"] for p in enriched) / max(len(enriched), 1), 2),
            "total_reviews": sum(p["reviews"] for p in enriched),
            "top_competitors": enriched[:5],
        }

        all_competitors.extend(enriched)

    all_competitors.sort(key=lambda x: x["revenue_usd"], reverse=True)

    czk_rate = round(usd_rates.get("CZK", 23.0), 2)
    eur_rate = round(usd_rates.get("EUR", 0.93), 2)

    return {
        "total_market_usd": round(total_usd, 2),
        "regions": region_summaries,
        "top_global_competitors": all_competitors[:10],
        "exchange_rates": {
            "CZK": czk_rate,
            "EUR": eur_rate,
            "source": "frankfurter.app (live)",
        },
        "methodology": {
            "ratio": REVIEWS_TO_SALES_RATIO,
            "note": f"Formula: Reviews × {REVIEWS_TO_SALES_RATIO} sales × Price. 1 USD = {czk_rate} CZK, {eur_rate} EUR.",
        }
    }
