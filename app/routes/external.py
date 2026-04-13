from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.services.external_apis import (
    search_foods_open_food_facts,
    get_food_by_barcode,
    search_exercises_wger,
    get_wger_categories,
    get_wger_muscles,
    search_recipes_themealdb,
    get_recipe_categories_themealdb
)

router = APIRouter(prefix="/external", tags=["APIs Externas"])


# ============================================================
# ALIMENTOS — Open Food Facts (gratuita, sem autenticação)
# Licença: Open Database License (ODbL)
# URL: https://world.openfoodfacts.org
# ============================================================

@router.get(
    "/foods/search",
    summary="Buscar alimentos — Open Food Facts",
    description=(
        "Busca alimentos na base pública **Open Food Facts**. "
        "Licença: Open Database License (ODbL). Sem necessidade de cadastro. "
        "Rota utilizada: `GET https://world.openfoodfacts.org/cgi/search.pl`"
    )
)
async def search_foods(
    query: str = Query(..., description="Termo de busca (ex: frango, arroz)"),
    page: Optional[int] = Query(1, description="Página de resultados")
):
    try:
        return await search_foods_open_food_facts(query, page)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Erro ao buscar na API externa: {str(e)}")


@router.get(
    "/foods/barcode/{barcode}",
    summary="Buscar alimento por código de barras — Open Food Facts",
    description=(
        "Busca um produto pelo **código de barras** na base pública Open Food Facts. "
        "Rota utilizada: `GET https://world.openfoodfacts.org/api/v0/product/{barcode}.json`"
    )
)
async def get_food_barcode(barcode: str):
    try:
        food = await get_food_by_barcode(barcode)
        if not food:
            raise HTTPException(status_code=404, detail="Produto nao encontrado")
        return food
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Erro ao buscar na API externa: {str(e)}")


# ============================================================
# EXERCÍCIOS — Wger (gratuita, sem autenticação)
# Licença: GNU Affero General Public License (AGPL)
# URL: https://wger.de/api/v2
# ============================================================

@router.get(
    "/exercises/search",
    summary="Buscar exercícios — Wger",
    description=(
        "Busca exercícios na API pública **Wger Workout Manager**. "
        "Licença: GNU AGPL. Sem necessidade de cadastro. "
        "Rota utilizada: `GET https://wger.de/api/v2/exercise/`"
    )
)
async def search_exercises(
    query: Optional[str] = Query(None, description="Nome do exercício"),
    language: Optional[int] = Query(4, description="Idioma: 2=Inglês, 4=Português"),
    limit: Optional[int] = Query(20, description="Resultados por página (máx 100)"),
    offset: Optional[int] = Query(0, description="Offset para paginação"),
    category: Optional[int] = Query(0, description="ID da categoria (8=Braços, 9=Pernas, 10=Abdômen, 11=Peito, 12=Costas, 13=Ombros, 14=Panturrilha)")
):
    try:
        return await search_exercises_wger(query or "", language, min(limit, 100), offset, category or 0)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Erro ao buscar na API externa: {str(e)}")


@router.get(
    "/exercises/categories",
    summary="Listar categorias de exercícios — Wger",
    description="Retorna as categorias de exercícios da API pública Wger."
)
async def list_exercise_categories():
    try:
        return await get_wger_categories()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Erro ao buscar na API externa: {str(e)}")


@router.get(
    "/exercises/muscles",
    summary="Listar músculos — Wger",
    description="Retorna a lista de músculos da API pública Wger."
)
async def list_muscles():
    try:
        return await get_wger_muscles()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Erro ao buscar na API externa: {str(e)}")


# ============================================================
# RECEITAS — TheMealDB (gratuita, sem autenticação)
# URL: https://www.themealdb.com/api/json/v1/1
# ============================================================

@router.get("/recipes/search", summary="Buscar receitas — TheMealDB")
async def search_recipes(
    query: Optional[str] = Query(None, description="Nome da receita"),
    category: Optional[str] = Query(None, description="Categoria (Chicken, Seafood, Vegetarian...)")
):
    try:
        return await search_recipes_themealdb(query or "", category or "")
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Erro ao buscar receitas: {str(e)}")


@router.get("/recipes/categories", summary="Categorias de receitas — TheMealDB")
async def list_recipe_categories():
    try:
        return await get_recipe_categories_themealdb()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Erro ao buscar categorias: {str(e)}")
