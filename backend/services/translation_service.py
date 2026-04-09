from typing import List

# Czech → English dictionary for supplement ingredients
CZ_TO_EN = {
    # Česnek
    "černý česnek": "black garlic",
    "česnek": "garlic",
    "allicin": "allicin",
    # Vitamíny
    "vitamin c": "vitamin c",
    "vitamin d": "vitamin d",
    "vitamin d3": "vitamin d3",
    "vitamin e": "vitamin e",
    "vitamin k": "vitamin k",
    "vitamin k2": "vitamin k2",
    "vitamin b12": "vitamin b12",
    "vitamin b6": "vitamin b6",
    "kyselina listová": "folic acid",
    "biotín": "biotin",
    "biotin": "biotin",
    "niacin": "niacin",
    # Minerály
    "hořčík": "magnesium",
    "zinek": "zinc",
    "železo": "iron",
    "vápník": "calcium",
    "selen": "selenium",
    "jód": "iodine",
    "jod": "iodine",
    "draslík": "potassium",
    "chrom": "chromium",
    "měď": "copper",
    "mangan": "manganese",
    "fosfor": "phosphorus",
    # Aminokyseliny a stimulanty
    "kofein": "caffeine",
    "taurin": "taurine",
    "l-karnitin": "l-carnitine",
    "l-arginin": "l-arginine",
    "l-glutamin": "l-glutamine",
    "l-theanin": "l-theanine",
    "kreatin": "creatine",
    "bcaa": "bcaa",
    # Byliny
    "kurkuma": "turmeric",
    "kurkumin": "curcumin",
    "ženšen": "ginseng",
    "echinacea": "echinacea",
    "třezalka": "st johns wort",
    "valeriána": "valerian",
    "kozlík": "valerian",
    "ashwagandha": "ashwagandha",
    "maca": "maca",
    "rakytník": "sea buckthorn",
    "bezinka": "elderberry",
    "elderberry": "elderberry",
    "moringa": "moringa",
    "spirulina": "spirulina",
    "chlorella": "chlorella",
    "goji": "goji",
    "acai": "acai",
    # Houby
    "reishi": "reishi mushroom",
    "chaga": "chaga mushroom",
    "lions mane": "lions mane mushroom",
    "hlíva": "oyster mushroom",
    # Omega & oleje
    "omega 3": "omega 3",
    "omega-3": "omega 3",
    "rybí olej": "fish oil",
    "lněný olej": "flaxseed oil",
    "konopný olej": "hemp oil",
    # Ostatní
    "kolagen": "collagen",
    "hyaluronová kyselina": "hyaluronic acid",
    "probiotika": "probiotics",
    "prebiotika": "prebiotics",
    "melatonin": "melatonin",
    "q10": "coq10",
    "koenzym q10": "coq10",
    "resveratrol": "resveratrol",
    "glutathion": "glutathione",
    "alfa lipoová kyselina": "alpha lipoic acid",
    "msm": "msm",
    "glukosamin": "glucosamine",
    "chondroitin": "chondroitin",
    "bromelain": "bromelain",
}


def translate_ingredient(ingredient: str) -> str:
    """
    Translate a single ingredient from Czech to English.
    Returns original if no translation found.
    """
    key = ingredient.strip().lower()
    return CZ_TO_EN.get(key, ingredient.strip())


def translate_ingredients(ingredients: str) -> List[str]:
    """
    Translate all ingredients to English.
    Returns list of translated ingredient strings.
    """
    parts = [i.strip() for i in ingredients.split(",") if i.strip()]
    return [translate_ingredient(p) for p in parts]
