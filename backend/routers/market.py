from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from services.search_service import search_all_regions
from services.scraper_service import parse_all_results
from services.estimator_service import aggregate_market_size
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/market", tags=["market"])


class EstimateRequest(BaseModel):
    ingredients: str = Field(..., min_length=5, max_length=1000, example="caffeine, taurine, B vitamins, L-carnitine")


class EstimateResponse(BaseModel):
    total_market_usd: float
    regions: dict
    top_global_competitors: list
    exchange_rates: dict
    methodology: dict


@router.post("/estimate", response_model=EstimateResponse)
async def estimate_market(request: EstimateRequest):
    """
    Main endpoint: searches competitors in CZ, EU, USA and returns market size estimate.
    """
    try:
        logger.info(f"Starting market estimate for ingredients: {request.ingredients[:80]}")

        # 1. Search competitors across all regions
        raw_results = await search_all_regions(request.ingredients)

        # 2. Fetch actual product pages and extract real price & reviews
        parsed_by_region = await parse_all_results(raw_results)

        # 3. Run estimation formula with live exchange rates
        estimation = await aggregate_market_size(parsed_by_region)

        logger.info(f"Estimate complete. Total market: ${estimation['total_market_usd']:,.0f}")
        return estimation

    except Exception as e:
        logger.error(f"Estimation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health():
    return {"status": "ok", "service": "Movit Market Estimator"}
