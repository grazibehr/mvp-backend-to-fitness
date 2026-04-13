from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.database import engine
from app.models.models import Base
from app.routes import auth, users, exercises, workouts, foods, meals, external
from app.seed import run_seed
import os

load_dotenv()

ENV = os.getenv("ENV", "development")

Base.metadata.create_all(bind=engine)
run_seed()

app = FastAPI(
    title="To Fitness API",
    description=(
        "API REST para o app **To Fitness** — controle de treinos, refeições e metas de saúde.\n\n"
        "## APIs Externas utilizadas\n"
        "- **Open Food Facts** — Banco de dados aberto de alimentos. "
        "Licença: Open Database License (ODbL). Gratuita, sem necessidade de cadastro. "
        "URL base: `https://world.openfoodfacts.org`\n"
        "- **Wger Workout Manager** — Base de exercícios físicos. "
        "Licença: GNU AGPL. Gratuita, sem necessidade de cadastro. "
        "URL base: `https://wger.de/api/v2`\n"
        "- **TheMealDB** — Base de receitas culinárias. "
        "Licença: Gratuita para uso pessoal e educacional. Sem necessidade de cadastro. "
        "URL base: `https://www.themealdb.com/api/json/v1/1`"
    ),
    version="1.0.0",
    contact={"name": "To Fitness", "url": "https://github.com"},
    docs_url="/docs" if ENV != "production" else None,
    redoc_url="/redoc" if ENV != "production" else None,
)

allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(exercises.router, prefix="/api")
app.include_router(workouts.router, prefix="/api")
app.include_router(foods.router, prefix="/api")
app.include_router(meals.router, prefix="/api")
app.include_router(external.router, prefix="/api")


@app.get("/api/health", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "To Fitness API funcionando!"}
