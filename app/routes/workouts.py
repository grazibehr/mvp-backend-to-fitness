from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from app.database import get_db
from app.models.models import User, Workout, WorkoutExercise, Exercise, WorkoutHistory
from app.schemas.schemas import (
    CreateWorkoutRequest, UpdateWorkoutRequest, WorkoutResponse,
    WorkoutExerciseResponse, WorkoutHistoryRequest, WorkoutHistoryResponse
)
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/workouts", tags=["Treinos"])


def _format_workout(workout: Workout) -> WorkoutResponse:
    exercises = []
    for we in sorted(workout.workout_exercises, key=lambda x: x.order_index):
        exercises.append(WorkoutExerciseResponse(
            id=we.id,
            exercise_id=we.exercise_id,
            name=we.exercise.name if we.exercise else None,
            muscle_group=we.exercise.muscle_group if we.exercise else None,
            difficulty=we.exercise.difficulty if we.exercise else None,
            sets=we.sets,
            reps=we.reps,
            weight=we.weight,
            order_index=we.order_index
        ))
    return WorkoutResponse(
        id=workout.id,
        name=workout.name,
        day_of_week=workout.day_of_week,
        exercise_count=len(exercises),
        exercises=exercises,
        created_at=workout.created_at
    )


@router.get("", response_model=List[WorkoutResponse], summary="Listar treinos do usuário")
def list_workouts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    workouts = (
        db.query(Workout)
        .options(joinedload(Workout.workout_exercises).joinedload(WorkoutExercise.exercise))
        .filter(Workout.user_id == current_user.id)
        .order_by(Workout.day_of_week)
        .all()
    )
    return [_format_workout(w) for w in workouts]


@router.post("", status_code=201, summary="Criar treino")
def create_workout(
    body: CreateWorkoutRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    workout = Workout(user_id=current_user.id, name=body.name, day_of_week=body.day_of_week)
    db.add(workout)
    db.flush()

    for i, ex in enumerate(body.exercises or []):
        we = WorkoutExercise(
            workout_id=workout.id,
            exercise_id=ex.exercise_id,
            sets=ex.sets,
            reps=ex.reps,
            weight=ex.weight,
            order_index=i
        )
        db.add(we)

    db.commit()
    return {"message": "Treino criado com sucesso", "id": workout.id}


@router.put("/{workout_id}", summary="Atualizar treino")
def update_workout(
    workout_id: int,
    body: UpdateWorkoutRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    workout = db.query(Workout).filter(
        Workout.id == workout_id, Workout.user_id == current_user.id
    ).first()
    if not workout:
        raise HTTPException(status_code=404, detail="Treino nao encontrado")

    if body.name is not None:
        workout.name = body.name
    if body.day_of_week is not None:
        workout.day_of_week = body.day_of_week

    if body.exercises is not None:
        db.query(WorkoutExercise).filter(WorkoutExercise.workout_id == workout_id).delete()
        for i, ex in enumerate(body.exercises):
            we = WorkoutExercise(
                workout_id=workout_id,
                exercise_id=ex.exercise_id,
                sets=ex.sets,
                reps=ex.reps,
                weight=ex.weight,
                order_index=i
            )
            db.add(we)

    db.commit()
    return {"message": "Treino atualizado com sucesso"}


@router.delete("/{workout_id}", summary="Excluir treino")
def delete_workout(
    workout_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    workout = db.query(Workout).filter(
        Workout.id == workout_id, Workout.user_id == current_user.id
    ).first()
    if not workout:
        raise HTTPException(status_code=404, detail="Treino nao encontrado")

    db.delete(workout)
    db.commit()
    return {"message": "Treino excluido com sucesso"}


@router.get("/history", response_model=List[WorkoutHistoryResponse], summary="Histórico de treinos")
def get_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return (
        db.query(WorkoutHistory)
        .filter(WorkoutHistory.user_id == current_user.id)
        .order_by(WorkoutHistory.completed_at.desc())
        .limit(50)
        .all()
    )


@router.post("/history", status_code=201, summary="Registrar histórico de treino")
def save_history(
    body: WorkoutHistoryRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    record = WorkoutHistory(
        user_id=current_user.id,
        **body.model_dump()
    )
    db.add(record)
    db.commit()
    return {"message": "Historico registrado com sucesso"}
