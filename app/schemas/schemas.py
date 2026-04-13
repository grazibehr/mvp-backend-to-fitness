from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List
from datetime import datetime


# ==================== AUTH ====================

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    name: str

    @field_validator("password")
    @classmethod
    def password_min_length(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError("A senha deve ter no minimo 6 caracteres")
        return v

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("O nome nao pode ser vazio")
        return v.strip()


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    gender: Optional[str] = None
    age: Optional[int] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    activity_level: Optional[str] = None
    goal: Optional[str] = None
    body_type: Optional[str] = None
    body_fat_percentage: Optional[float] = None
    bmi: Optional[float] = None
    bmi_category: Optional[str] = None
    daily_calorie_target: Optional[int] = 2000
    daily_protein_target: Optional[int] = 150
    daily_carbs_target: Optional[int] = 250
    daily_fat_target: Optional[int] = 67
    health_conditions: Optional[List[str]] = []
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class AuthResponse(BaseModel):
    message: str
    token: str
    user: UserResponse


# ==================== USER ====================

class UpdateProfileRequest(BaseModel):
    name: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[int] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    activity_level: Optional[str] = None
    goal: Optional[str] = None
    body_type: Optional[str] = None
    body_fat_percentage: Optional[float] = None
    health_conditions: Optional[List[str]] = None


# ==================== EXERCISE ====================

class ExerciseResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    muscle_group: Optional[str] = None
    difficulty: Optional[str] = None
    equipment: Optional[str] = None
    contraindicated: Optional[List[str]] = []

    model_config = {"from_attributes": True}


# ==================== WORKOUT ====================

class WorkoutExerciseInput(BaseModel):
    exercise_id: int
    sets: Optional[int] = 3
    reps: Optional[str] = "12"
    weight: Optional[float] = None


class WorkoutExerciseResponse(BaseModel):
    id: int
    exercise_id: int
    name: Optional[str] = None
    muscle_group: Optional[str] = None
    difficulty: Optional[str] = None
    sets: int
    reps: str
    weight: Optional[float] = None
    order_index: int

    model_config = {"from_attributes": True}


class CreateWorkoutRequest(BaseModel):
    name: str
    day_of_week: Optional[int] = None
    exercises: Optional[List[WorkoutExerciseInput]] = []


class UpdateWorkoutRequest(BaseModel):
    name: Optional[str] = None
    day_of_week: Optional[int] = None
    exercises: Optional[List[WorkoutExerciseInput]] = None


class WorkoutResponse(BaseModel):
    id: int
    name: str
    day_of_week: Optional[int] = None
    exercise_count: int = 0
    exercises: List[WorkoutExerciseResponse] = []
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class WorkoutHistoryRequest(BaseModel):
    workout_id: Optional[int] = None
    workout_name: Optional[str] = None
    duration: Optional[int] = None
    exercises_completed: Optional[int] = 0
    total_exercises: Optional[int] = 0
    total_sets: Optional[int] = 0


class WorkoutHistoryResponse(BaseModel):
    id: int
    workout_id: Optional[int] = None
    workout_name: Optional[str] = None
    duration: Optional[int] = None
    exercises_completed: int = 0
    total_exercises: int = 0
    total_sets: int = 0
    completed_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ==================== FOOD ====================

class CreateFoodRequest(BaseModel):
    name: str
    category: Optional[str] = "Outros"
    calories: Optional[float] = 0
    protein: Optional[float] = 0
    carbs: Optional[float] = 0
    fat: Optional[float] = 0
    fiber: Optional[float] = 0
    portion_size: Optional[float] = 100
    portion_description: Optional[str] = "100g"


class UpdateFoodRequest(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    calories: Optional[float] = None
    protein: Optional[float] = None
    carbs: Optional[float] = None
    fat: Optional[float] = None
    fiber: Optional[float] = None
    portion_size: Optional[float] = None
    portion_description: Optional[str] = None


class FoodResponse(BaseModel):
    id: int
    name: str
    category: Optional[str] = None
    calories: float = 0
    protein: float = 0
    carbs: float = 0
    fat: float = 0
    fiber: float = 0
    portion_size: float = 100
    portion_description: str = "100g"

    model_config = {"from_attributes": True}


# ==================== MEAL ====================

class MealItemInput(BaseModel):
    food_id: Optional[int] = None
    food_name: str
    quantity: Optional[float] = 1
    calories: Optional[float] = 0
    protein: Optional[float] = 0
    carbs: Optional[float] = 0
    fat: Optional[float] = 0


class CreateMealRequest(BaseModel):
    meal_type: str
    date: Optional[str] = None
    items: Optional[List[MealItemInput]] = []


class MealItemResponse(BaseModel):
    id: int
    food_id: Optional[int] = None
    food_name: str
    quantity: float
    calories: float
    protein: float
    carbs: float
    fat: float

    model_config = {"from_attributes": True}


class MealResponse(BaseModel):
    id: int
    meal_type: str
    date: str
    total_calories: float = 0
    total_protein: float = 0
    total_carbs: float = 0
    total_fat: float = 0
    items: List[MealItemResponse] = []

    model_config = {"from_attributes": True}


class NutritionalSummary(BaseModel):
    consumed: dict
    targets: dict
