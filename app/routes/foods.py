from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.models import User, Food
from app.schemas.schemas import CreateFoodRequest, UpdateFoodRequest, FoodResponse
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/foods", tags=["Alimentos"])


@router.get("", response_model=List[FoodResponse], summary="Listar alimentos")
def list_foods(
    category: Optional[str] = Query(None, description="Filtrar por categoria"),
    search: Optional[str] = Query(None, description="Buscar por nome"),
    db: Session = Depends(get_db)
):
    query = db.query(Food)
    if category:
        query = query.filter(Food.category == category)
    if search:
        query = query.filter(Food.name.ilike(f"%{search}%"))
    return query.order_by(Food.category, Food.name).all()


@router.get("/categories", response_model=List[str], summary="Listar categorias de alimentos")
def get_categories(db: Session = Depends(get_db)):
    rows = db.query(Food.category).distinct().all()
    return sorted([r[0] for r in rows if r[0]])


@router.get("/{food_id}", response_model=FoodResponse, summary="Buscar alimento por ID")
def get_food(food_id: int, db: Session = Depends(get_db)):
    food = db.query(Food).filter(Food.id == food_id).first()
    if not food:
        raise HTTPException(status_code=404, detail="Alimento nao encontrado")
    return food


@router.post("", response_model=FoodResponse, status_code=201, summary="Cadastrar alimento personalizado")
def create_food(
    body: CreateFoodRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    food = Food(**body.model_dump(), user_id=current_user.id)
    db.add(food)
    db.commit()
    db.refresh(food)
    return food


@router.put("/{food_id}", summary="Atualizar alimento personalizado")
def update_food(
    food_id: int,
    body: UpdateFoodRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    food = db.query(Food).filter(Food.id == food_id, Food.user_id == current_user.id).first()
    if not food:
        raise HTTPException(status_code=404, detail="Alimento nao encontrado ou sem permissao")

    for field, value in body.model_dump(exclude_none=True).items():
        setattr(food, field, value)

    db.commit()
    return {"message": "Alimento atualizado com sucesso"}


@router.delete("/{food_id}", summary="Excluir alimento personalizado")
def delete_food(
    food_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    food = db.query(Food).filter(Food.id == food_id, Food.user_id == current_user.id).first()
    if not food:
        raise HTTPException(status_code=404, detail="Alimento nao encontrado ou sem permissao")

    db.delete(food)
    db.commit()
    return {"message": "Alimento excluido com sucesso"}
