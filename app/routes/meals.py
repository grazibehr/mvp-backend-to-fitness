from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app.database import get_db
from app.models.models import User, Meal, MealItem
from app.schemas.schemas import CreateMealRequest, MealItemInput, MealResponse, MealItemResponse, NutritionalSummary
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/meals", tags=["Refeições"])


def _format_meal(meal: Meal) -> MealResponse:
    items = [
        MealItemResponse(
            id=item.id,
            food_id=item.food_id,
            food_name=item.food_name,
            quantity=item.quantity,
            calories=item.calories,
            protein=item.protein,
            carbs=item.carbs,
            fat=item.fat
        )
        for item in meal.items
    ]
    return MealResponse(
        id=meal.id,
        meal_type=meal.meal_type,
        date=meal.date,
        total_calories=sum(i.calories for i in meal.items),
        total_protein=sum(i.protein for i in meal.items),
        total_carbs=sum(i.carbs for i in meal.items),
        total_fat=sum(i.fat for i in meal.items),
        items=items
    )


@router.get("", response_model=List[MealResponse], summary="Listar refeições do dia")
def list_meals(
    date_param: Optional[str] = Query(None, alias="date", description="Data no formato YYYY-MM-DD"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    target_date = date_param or str(date.today())
    meals = (
        db.query(Meal)
        .filter(Meal.user_id == current_user.id, Meal.date == target_date)
        .order_by(Meal.meal_type)
        .all()
    )
    return [_format_meal(m) for m in meals]


@router.get("/summary", summary="Resumo nutricional do dia")
def get_summary(
    date_param: Optional[str] = Query(None, alias="date", description="Data no formato YYYY-MM-DD"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    target_date = date_param or str(date.today())
    meals = db.query(Meal).filter(
        Meal.user_id == current_user.id, Meal.date == target_date
    ).all()

    total_calories = sum(item.calories for meal in meals for item in meal.items)
    total_protein = sum(item.protein for meal in meals for item in meal.items)
    total_carbs = sum(item.carbs for meal in meals for item in meal.items)
    total_fat = sum(item.fat for meal in meals for item in meal.items)

    return {
        "consumed": {
            "total_calories": round(total_calories, 1),
            "total_protein": round(total_protein, 1),
            "total_carbs": round(total_carbs, 1),
            "total_fat": round(total_fat, 1)
        },
        "targets": {
            "daily_calorie_target": current_user.daily_calorie_target,
            "daily_protein_target": current_user.daily_protein_target,
            "daily_carbs_target": current_user.daily_carbs_target,
            "daily_fat_target": current_user.daily_fat_target
        }
    }


@router.post("", status_code=201, summary="Criar refeição")
def create_meal(
    body: CreateMealRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    target_date = body.date or str(date.today())

    meal = db.query(Meal).filter(
        Meal.user_id == current_user.id,
        Meal.meal_type == body.meal_type,
        Meal.date == target_date
    ).first()

    if not meal:
        meal = Meal(user_id=current_user.id, meal_type=body.meal_type, date=target_date)
        db.add(meal)
        db.flush()

    for item_data in (body.items or []):
        item = MealItem(
            meal_id=meal.id,
            food_id=item_data.food_id,
            food_name=item_data.food_name,
            quantity=item_data.quantity,
            calories=item_data.calories,
            protein=item_data.protein,
            carbs=item_data.carbs,
            fat=item_data.fat
        )
        db.add(item)

    db.commit()
    return {"message": "Refeicao criada com sucesso", "id": meal.id}


@router.post("/{meal_id}/items", status_code=201, summary="Adicionar item à refeição")
def add_item(
    meal_id: int,
    body: MealItemInput,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    meal = db.query(Meal).filter(Meal.id == meal_id, Meal.user_id == current_user.id).first()
    if not meal:
        raise HTTPException(status_code=404, detail="Refeicao nao encontrada")

    item = MealItem(
        meal_id=meal_id,
        food_id=body.food_id,
        food_name=body.food_name,
        quantity=body.quantity,
        calories=body.calories,
        protein=body.protein,
        carbs=body.carbs,
        fat=body.fat
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return {"message": "Item adicionado com sucesso", "id": item.id}


@router.delete("/items/{item_id}", summary="Remover item da refeição")
def remove_item(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    item = (
        db.query(MealItem)
        .join(Meal)
        .filter(MealItem.id == item_id, Meal.user_id == current_user.id)
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="Item nao encontrado")

    db.delete(item)
    db.commit()
    return {"message": "Item removido com sucesso"}


@router.delete("/{meal_id}", summary="Excluir refeição")
def delete_meal(
    meal_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    meal = db.query(Meal).filter(Meal.id == meal_id, Meal.user_id == current_user.id).first()
    if not meal:
        raise HTTPException(status_code=404, detail="Refeicao nao encontrada")

    db.delete(meal)
    db.commit()
    return {"message": "Refeicao excluida com sucesso"}
