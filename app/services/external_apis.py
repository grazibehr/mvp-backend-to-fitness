import httpx
import time

OPEN_FOOD_FACTS_URL = "https://world.openfoodfacts.org"
WGER_URL = "https://wger.de/api/v2"
THEMEALDB_URL = "https://www.themealdb.com/api/json/v1/1"

# Mapeamento de categorias TheMealDB para objetivos fitness
_MEAL_CATEGORY_TAGS = {
    "Chicken": {"is_high_protein": True, "good_for_muscle_gain": True},
    "Beef": {"is_high_protein": True, "good_for_muscle_gain": True},
    "Seafood": {"is_high_protein": True, "good_for_weight_loss": True},
    "Lamb": {"is_high_protein": True, "good_for_muscle_gain": True},
    "Vegetarian": {"is_low_carb": False, "good_for_weight_loss": True},
    "Vegan": {"good_for_weight_loss": True},
    "Starter": {"good_for_weight_loss": True},
    "Breakfast": {"good_for_muscle_gain": True},
    "Pasta": {"good_for_muscle_gain": True},
}

_cache: dict = {}
_CACHE_TTL = 3600  # 1 hora


def _cache_get(key: str):
    entry = _cache.get(key)
    if entry and time.time() - entry["ts"] < _CACHE_TTL:
        return entry["data"]
    return None


def _cache_set(key: str, data):
    _cache[key] = {"data": data, "ts": time.time()}


def _parse_food_product(product: dict) -> dict:
    return {
        "id": product.get("id") or product.get("code"),
        "name": product.get("product_name") or product.get("product_name_pt") or "Sem nome",
        "brand": product.get("brands", ""),
        "image": product.get("image_small_url") or product.get("image_url"),
        "calories": product.get("nutriments", {}).get("energy-kcal_100g", 0) or 0,
        "protein": product.get("nutriments", {}).get("proteins_100g", 0) or 0,
        "carbs": product.get("nutriments", {}).get("carbohydrates_100g", 0) or 0,
        "fat": product.get("nutriments", {}).get("fat_100g", 0) or 0,
        "fiber": product.get("nutriments", {}).get("fiber_100g", 0) or 0,
        "portion_size": 100,
        "portion_description": "100g"
    }


FOOD_FIELDS = "id,code,product_name,product_name_pt,brands,image_small_url,image_url,nutriments"

async def search_foods_open_food_facts(query: str, page: int = 1) -> dict:
    cache_key = f"foods:{query}:{page}"
    cached = _cache_get(cache_key)
    if cached:
        return cached

    url = (
        f"{OPEN_FOOD_FACTS_URL}/cgi/search.pl"
        f"?search_terms={query}&search_simple=1&action=process"
        f"&json=1&page={page}&page_size=10"
        f"&fields={FOOD_FIELDS}"
    )
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(url)
        response.raise_for_status()
        data = response.json()

    products = [_parse_food_product(p) for p in data.get("products", []) if p.get("product_name")]
    total = int(data.get("count", 0) or 0)

    result = {
        "products": products,
        "total": total,
        "page": page,
        "pages": max(1, -(-total // 10))
    }
    _cache_set(cache_key, result)
    return result


async def get_food_by_barcode(barcode: str) -> dict | None:
    url = f"{OPEN_FOOD_FACTS_URL}/api/v0/product/{barcode}.json"
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(url)
        response.raise_for_status()
        data = response.json()

    if data.get("status") != 1:
        return None

    product = data["product"]
    result = _parse_food_product(product)
    result["barcode"] = barcode
    result["ingredients"] = product.get("ingredients_text") or product.get("ingredients_text_pt", "")
    return result


def _get_translation(translations: list, preferred_lang: int = 4) -> dict:
    """Get translation in preferred language, fallback to English (2) only."""
    for lang in [preferred_lang, 2]:
        for t in translations:
            if t.get("language") == lang and t.get("name"):
                return t
    return {}


async def search_exercises_wger(query: str = "", language: int = 4, limit: int = 20, offset: int = 0, category: int = 0) -> dict:
    """language=4 is Portuguese, language=2 is English"""
    cache_key = f"exercises:{query}:{language}:{limit}:{offset}:{category}"
    cached = _cache_get(cache_key)
    if cached:
        return cached

    params = {"format": "json", "limit": limit, "offset": offset}
    if query:
        params["name"] = query
    if category:
        params["category"] = category

    async with httpx.AsyncClient(timeout=15) as client:
        response = await client.get(f"{WGER_URL}/exerciseinfo/", params=params)
        response.raise_for_status()
        data = response.json()

    exercises = []
    for ex in data.get("results", []):
        translation = _get_translation(ex.get("translations", []), language)
        name = translation.get("name", "")
        description = translation.get("description", "")
        if not name:
            continue
        category = ex.get("category", {})
        exercises.append({
            "id": ex.get("id"),
            "uuid": ex.get("uuid"),
            "name": name,
            "description": description,
            "category": category.get("id") if isinstance(category, dict) else category,
            "category_name": category.get("name", "") if isinstance(category, dict) else "",
            "muscles": [m.get("id") if isinstance(m, dict) else m for m in ex.get("muscles", [])],
            "muscles_secondary": [m.get("id") if isinstance(m, dict) else m for m in ex.get("muscles_secondary", [])],
            "equipment": [e.get("id") if isinstance(e, dict) else e for e in ex.get("equipment", [])]
        })

    result = {"exercises": exercises, "total": data.get("count", 0)}
    _cache_set(cache_key, result)
    return result


async def get_wger_categories() -> list:
    cached = _cache_get("wger_categories")
    if cached:
        return cached
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(f"{WGER_URL}/exercisecategory/", params={"format": "json"})
        response.raise_for_status()
        data = response.json()
    result = data.get("results", [])
    _cache_set("wger_categories", result)
    return result


async def get_wger_muscles() -> list:
    cached = _cache_get("wger_muscles")
    if cached:
        return cached
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(f"{WGER_URL}/muscle/", params={"format": "json"})
        response.raise_for_status()
        data = response.json()
    result = data.get("results", [])
    _cache_set("wger_muscles", result)
    return result


def _parse_meal(meal: dict) -> dict:
    ingredients = []
    for i in range(1, 21):
        ing = meal.get(f"strIngredient{i}", "")
        measure = meal.get(f"strMeasure{i}", "")
        if ing and ing.strip():
            ingredients.append({"name": ing.strip(), "measure": measure.strip()})

    category = meal.get("strCategory", "")
    tags = _MEAL_CATEGORY_TAGS.get(category, {})

    return {
        "id": meal.get("idMeal"),
        "name": meal.get("strMeal", ""),
        "category": category,
        "area": meal.get("strArea", ""),
        "instructions": meal.get("strInstructions", ""),
        "image": meal.get("strMealThumb", ""),
        "tags": meal.get("strTags", ""),
        "youtube": meal.get("strYoutube", ""),
        "ingredients": ingredients,
        "is_high_protein": tags.get("is_high_protein", False),
        "is_low_carb": tags.get("is_low_carb", False),
        "good_for_weight_loss": tags.get("good_for_weight_loss", False),
        "good_for_muscle_gain": tags.get("good_for_muscle_gain", False),
    }


async def search_recipes_themealdb(query: str = "", category: str = "") -> dict:
    cache_key = f"recipes:{query}:{category}"
    cached = _cache_get(cache_key)
    if cached:
        return cached

    async with httpx.AsyncClient(timeout=10) as client:
        if query:
            resp = await client.get(f"{THEMEALDB_URL}/search.php", params={"s": query})
            resp.raise_for_status()
            data = resp.json()
            meals = data.get("meals") or []
        elif category:
            resp = await client.get(f"{THEMEALDB_URL}/filter.php", params={"c": category})
            resp.raise_for_status()
            data = resp.json()
            # filter.php returns minimal data, fetch details for first 12
            previews = (data.get("meals") or [])[:12]
            meals = []
            for preview in previews:
                detail_resp = await client.get(f"{THEMEALDB_URL}/lookup.php", params={"i": preview["idMeal"]})
                detail_data = detail_resp.json()
                if detail_data.get("meals"):
                    meals.append(detail_data["meals"][0])
        else:
            # Default: fetch healthy categories
            result = []
            for cat in ["Chicken", "Seafood", "Vegetarian"]:
                resp = await client.get(f"{THEMEALDB_URL}/filter.php", params={"c": cat})
                resp.raise_for_status()
                previews = (resp.json().get("meals") or [])[:5]
                for preview in previews:
                    detail_resp = await client.get(f"{THEMEALDB_URL}/lookup.php", params={"i": preview["idMeal"]})
                    detail_data = detail_resp.json()
                    if detail_data.get("meals"):
                        result.append(_parse_meal(detail_data["meals"][0]))
            _cache_set(cache_key, {"recipes": result, "total": len(result)})
            return {"recipes": result, "total": len(result)}

    parsed = [_parse_meal(m) for m in meals]
    result = {"recipes": parsed, "total": len(parsed)}
    _cache_set(cache_key, result)
    return result


async def get_recipe_categories_themealdb() -> list:
    cached = _cache_get("meal_categories")
    if cached:
        return cached
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(f"{THEMEALDB_URL}/categories.php")
        resp.raise_for_status()
        data = resp.json()
    result = [
        {"id": c["idCategory"], "name": c["strCategory"], "image": c["strCategoryThumb"]}
        for c in (data.get("categories") or [])
    ]
    _cache_set("meal_categories", result)
    return result
