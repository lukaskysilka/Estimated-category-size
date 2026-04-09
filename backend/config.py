import os
from dotenv import load_dotenv

load_dotenv()

# -- API Keys ------------------------------------------------------------------
SERPER_API_KEY = os.getenv("SERPER_API_KEY", "YOUR_SERPER_KEY_HERE")

# -- Estimation heuristics -----------------------------------------------------
REVIEWS_TO_SALES_RATIO = 50  # 1 review = 50 sales (industry standard)

# -- Region settings -----------------------------------------------------------
REGIONS = {
    "CZ": {"gl": "cz", "hl": "cs", "currency": "CZK", "currency_symbol": "Kč"},
    "EU": {"gl": "de", "hl": "de", "currency": "EUR", "currency_symbol": "€"},
    "USA": {"gl": "us", "hl": "en", "currency": "USD", "currency_symbol": "$"},
}

# -- CORS ----------------------------------------------------------------------
ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:3000",
    "https://estimated-category-size.vercel.app",
    "https://estimated-category-size-iep7c7r2e-lukaskysilkas-projects.vercel.app",
]
