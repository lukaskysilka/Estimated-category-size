import httpx
import asyncio
from typing import List, Dict, Any
from config import SERPER_API_KEY, REGIONS
from services.translation_service import translate_ingredients
import logging

logger = logging.getLogger(__name__)

SERPER_SHOPPING_ENDPOINT = "https://google.serper.dev/shopping"
RESULTS_PER_QUERY = 20
MAX_RESULTS_PER_REGION = 20


def _build_queries(ingredients: str, region_key: str) -> List[str]:
    """
    CZ: Czech ingredient names.
    EU/USA: Translated English names for accurate results.
    """
    # Czech parts for CZ queries
    cz_parts = [i.strip() for i in ingredients.split(",") if i.strip()]
    cz_first = cz_parts[0] if cz_parts else ""
    cz_top2 = " ".join(cz_parts[:2])
    cz_top3 = " ".join(cz_parts[:3])

    # English parts for EU/USA queries
    en_parts = translate_ingredients(ingredients)
    en_first = en_parts[0] if en_parts else cz_first
    en_top2 = " ".join(en_parts[:2])
    en_top3 = " ".join(en_parts[:3])

    if region_key == "CZ":
        return [
            f"{cz_first} doplněk stravy koupit",
            f"{cz_first} kapsle tablety cena",
            f"{cz_top2} doplněk stravy",
            f"{cz_top3} kapsle koupit",
        ]
    elif region_key == "EU":
        return [
            f"{en_first} supplement buy",
            f"{en_first} capsules supplement",
            f"{en_top2} supplement capsules",
            f"{en_top3} supplement buy",
        ]
    else:  # USA
        return [
            f"{en_first} supplement capsules buy",
            f"best {en_first} supplement",
            f"{en_top2} supplement buy",
            f"{en_top3} capsules supplement",
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
