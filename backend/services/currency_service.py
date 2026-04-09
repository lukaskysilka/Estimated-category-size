import httpx
import logging
from typing import Dict

logger = logging.getLogger(__name__)

# Fallback rates if API is unavailable
FALLBACK_RATES = {
    "CZK": 23.0,   # 1 USD = 23 CZK
    "EUR": 0.93,   # 1 USD = 0.93 EUR
    "USD": 1.0,
}

_cached_rates: Dict[str, float] = {}


async def fetch_usd_rates() -> Dict[str, float]:
    """
    Fetch current exchange rates from frankfurter.app.
    Returns how many units of each currency equal 1 USD.
    No API key required.
    """
    global _cached_rates

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(
                "https://api.frankfurter.app/latest",
                params={"from": "USD", "to": "CZK,EUR"},
            )
            response.raise_for_status()
            data = response.json()
            rates = data.get("rates", {})
            rates["USD"] = 1.0

            logger.info(f"Live exchange rates: 1 USD = {rates.get('CZK')} CZK, {rates.get('EUR')} EUR")
            _cached_rates = rates
            return rates

    except Exception as e:
        logger.warning(f"Could not fetch exchange rates ({e}), using fallback: {FALLBACK_RATES}")
        return FALLBACK_RATES


def get_usd_rate(currency: str, rates: Dict[str, float]) -> float:
    """
    Returns how many USD = 1 unit of given currency.
    e.g. CZK: 1/23 = 0.0435
    """
    per_usd = rates.get(currency, 1.0)
    return 1.0 / per_usd if per_usd else 1.0
