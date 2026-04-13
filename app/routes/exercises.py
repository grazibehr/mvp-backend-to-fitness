from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.models import Exercise
from app.schemas.schemas import ExerciseResponse

router = APIRouter(prefix="/exercises", tags=["Exercícios"])


@router.get("", response_model=List[ExerciseResponse], summary="Listar exercícios")
def list_exercises(
    muscle_group: Optional[str] = Query(None, description="Filtrar por grupo muscular"),
    difficulty: Optional[str] = Query(None, description="Filtrar por dificuldade"),
    search: Optional[str] = Query(None, description="Buscar por nome"),
    db: Session = Depends(get_db)
):
    query = db.query(Exercise)
    if muscle_group:
        query = query.filter(Exercise.muscle_group == muscle_group)
    if difficulty:
        query = query.filter(Exercise.difficulty == difficulty)
    if search:
        query = query.filter(Exercise.name.ilike(f"%{search}%"))
    return query.order_by(Exercise.muscle_group, Exercise.name).all()


@router.get("/muscle-groups", response_model=List[str], summary="Listar grupos musculares")
def get_muscle_groups(db: Session = Depends(get_db)):
    rows = db.query(Exercise.muscle_group).distinct().all()
    return sorted([r[0] for r in rows if r[0]])


@router.get("/{exercise_id}", response_model=ExerciseResponse, summary="Buscar exercício por ID")
def get_exercise(exercise_id: int, db: Session = Depends(get_db)):
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercicio nao encontrado")
    return exercise
