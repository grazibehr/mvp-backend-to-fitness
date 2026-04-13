from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.database import get_db
from app.models.models import User
from app.schemas.schemas import RegisterRequest, LoginRequest, AuthResponse, UserResponse
from app.middleware.auth import create_access_token

router = APIRouter(prefix="/auth", tags=["Autenticação"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register", response_model=AuthResponse, status_code=201, summary="Cadastrar novo usuário")
def register(body: RegisterRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == body.email).first():
        raise HTTPException(status_code=400, detail="Email ja cadastrado")

    hashed_password = pwd_context.hash(body.password)
    user = User(email=body.email, password=hashed_password, name=body.name)
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(user.id)
    return AuthResponse(
        message="Usuario criado com sucesso",
        token=token,
        user=UserResponse.model_validate(user)
    )


@router.post("/login", response_model=AuthResponse, summary="Login do usuário")
def login(body: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == body.email).first()
    if not user or not pwd_context.verify(body.password, user.password):
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")

    token = create_access_token(user.id)
    return AuthResponse(
        message="Login realizado com sucesso",
        token=token,
        user=UserResponse.model_validate(user)
    )
