from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import User
from app.schemas.schemas import UserResponse, UpdateProfileRequest
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/users", tags=["Usuários"])


@router.get("/profile", response_model=UserResponse, summary="Obter perfil do usuário")
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/profile", summary="Atualizar perfil e calcular metas nutricionais")
def update_profile(
    body: UpdateProfileRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    update_data = body.model_dump(exclude_none=True)

    for field, value in update_data.items():
        setattr(current_user, field, value)

    weight = current_user.weight
    height = current_user.height
    age = current_user.age
    gender = current_user.gender
    activity_level = current_user.activity_level
    goal = current_user.goal

    if all([weight, height, age, gender, activity_level]):
        if gender == "male":
            tmb = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
        else:
            tmb = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

        activity_factors = {
            "sedentary": 1.2,
            "light": 1.375,
            "moderate": 1.55,
            "active": 1.725,
            "very_active": 1.9
        }
        daily_calories = round(tmb * activity_factors.get(activity_level, 1.55))

        if goal in ("lose_weight", "lose_fat"):
            daily_calories = round(daily_calories * 0.8)
        elif goal == "gain_muscle":
            daily_calories = round(daily_calories * 1.1)

        daily_protein = round(weight * 2)
        daily_fat = round((daily_calories * 0.25) / 9)
        daily_carbs = round((daily_calories - (daily_protein * 4) - (daily_fat * 9)) / 4)

        # Calcular IMC
        height_m = height / 100
        bmi = round(weight / (height_m ** 2), 1)
        if bmi < 18.5:
            bmi_category = "underweight"
        elif bmi < 25:
            bmi_category = "normal"
        elif bmi < 30:
            bmi_category = "overweight"
        elif bmi < 35:
            bmi_category = "obese_1"
        elif bmi < 40:
            bmi_category = "obese_2"
        else:
            bmi_category = "obese_3"

        current_user.daily_calorie_target = daily_calories
        current_user.daily_protein_target = daily_protein
        current_user.daily_carbs_target = daily_carbs
        current_user.daily_fat_target = daily_fat
        current_user.bmi = bmi
        current_user.bmi_category = bmi_category

    db.commit()
    db.refresh(current_user)

    return {
        "message": "Perfil atualizado com sucesso",
        "targets": {
            "daily_calorie_target": current_user.daily_calorie_target,
            "daily_protein_target": current_user.daily_protein_target,
            "daily_carbs_target": current_user.daily_carbs_target,
            "daily_fat_target": current_user.daily_fat_target
        }
    }
