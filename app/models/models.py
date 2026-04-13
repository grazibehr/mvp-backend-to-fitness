from sqlalchemy import Column, Integer, String, Float, Boolean, Text, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    gender = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    weight = Column(Float, nullable=True)
    height = Column(Float, nullable=True)
    activity_level = Column(String, nullable=True)
    goal = Column(String, nullable=True)
    body_type = Column(String, nullable=True)
    body_fat_percentage = Column(Float, nullable=True)
    bmi = Column(Float, nullable=True)
    bmi_category = Column(String, nullable=True)
    daily_calorie_target = Column(Integer, default=2000)
    daily_protein_target = Column(Integer, default=150)
    daily_carbs_target = Column(Integer, default=250)
    daily_fat_target = Column(Integer, default=67)
    health_conditions = Column(JSON, default=list)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    workouts = relationship("Workout", back_populates="user", cascade="all, delete-orphan")
    meals = relationship("Meal", back_populates="user", cascade="all, delete-orphan")
    foods = relationship("Food", back_populates="user")
    workout_history = relationship("WorkoutHistory", back_populates="user", cascade="all, delete-orphan")


class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    muscle_group = Column(String, nullable=True)
    difficulty = Column(String, nullable=True)
    equipment = Column(String, nullable=True)
    contraindicated = Column(JSON, default=list)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    workout_exercises = relationship("WorkoutExercise", back_populates="exercise")


class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    day_of_week = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="workouts")
    workout_exercises = relationship("WorkoutExercise", back_populates="workout", cascade="all, delete-orphan")


class WorkoutExercise(Base):
    __tablename__ = "workout_exercises"

    id = Column(Integer, primary_key=True, index=True)
    workout_id = Column(Integer, ForeignKey("workouts.id"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)
    sets = Column(Integer, default=3)
    reps = Column(String, default="12")
    weight = Column(Float, nullable=True)
    order_index = Column(Integer, default=0)

    workout = relationship("Workout", back_populates="workout_exercises")
    exercise = relationship("Exercise", back_populates="workout_exercises")


class WorkoutHistory(Base):
    __tablename__ = "workout_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    workout_id = Column(Integer, nullable=True)
    workout_name = Column(String, nullable=True)
    duration = Column(Integer, nullable=True)
    exercises_completed = Column(Integer, default=0)
    total_exercises = Column(Integer, default=0)
    total_sets = Column(Integer, default=0)
    completed_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="workout_history")


class Food(Base):
    __tablename__ = "foods"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String, default="Outros")
    calories = Column(Float, default=0)
    protein = Column(Float, default=0)
    carbs = Column(Float, default=0)
    fat = Column(Float, default=0)
    fiber = Column(Float, default=0)
    portion_size = Column(Float, default=100)
    portion_description = Column(String, default="100g")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="foods")
    meal_items = relationship("MealItem", back_populates="food")


class Meal(Base):
    __tablename__ = "meals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    meal_type = Column(String, nullable=False)
    date = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="meals")
    items = relationship("MealItem", back_populates="meal", cascade="all, delete-orphan")


class MealItem(Base):
    __tablename__ = "meal_items"

    id = Column(Integer, primary_key=True, index=True)
    meal_id = Column(Integer, ForeignKey("meals.id"), nullable=False)
    food_id = Column(Integer, ForeignKey("foods.id"), nullable=True)
    food_name = Column(String, nullable=False)
    quantity = Column(Float, default=1)
    calories = Column(Float, default=0)
    protein = Column(Float, default=0)
    carbs = Column(Float, default=0)
    fat = Column(Float, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    meal = relationship("Meal", back_populates="items")
    food = relationship("Food", back_populates="meal_items")
