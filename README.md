# To Fitness API

API REST desenvolvida em **Python + FastAPI** para o sistema **To Fitness** — plataforma de controle de treinos, refeições e metas de saúde pessoal.

---

## Arquitetura

```
┌─────────────────────────────────┐
│  Frontend Vue 3 (to-fitness)    │
│  port 5173                      │
└─────────────────────────────────┘
         │ REST (GET / POST / PUT / DELETE)
         ▼
┌─────────────────────────────────┐      ┌──────────────────────────────┐
│  To Fitness API (FastAPI)       │─────▶│  Open Food Facts             │
│  SQLite + SQLAlchemy            │      │  world.openfoodfacts.org     │
│  port 8000  →  /docs (Swagger)  │─────▶│  Wger Workout Manager        │
└─────────────────────────────────┘      │  wger.de/api/v2              │
                                         │  TheMealDB                   │
                                         │  themealdb.com/api           │
                                         └──────────────────────────────┘
```

---

## APIs Externas utilizadas

### Open Food Facts
- **URL**: https://world.openfoodfacts.org
- **Licença**: Open Database License (ODbL)
- **Cadastro**: Não necessário
- **Rotas consumidas**:
  - `GET /cgi/search.pl` — busca de alimentos por nome
  - `GET /api/v0/product/{barcode}.json` — busca por código de barras

### Wger Workout Manager
- **URL**: https://wger.de/api/v2
- **Licença**: GNU Affero General Public License (AGPL)
- **Cadastro**: Não necessário
- **Rotas consumidas**:
  - `GET /exerciseinfo/` — busca e listagem de exercícios com traduções
  - `GET /exercisecategory/` — categorias de exercícios
  - `GET /muscle/` — grupos musculares

### TheMealDB
- **URL**: https://www.themealdb.com/api/json/v1/1
- **Licença**: Gratuita para uso pessoal e educacional (Creative Commons)
- **Cadastro**: Não necessário
- **Rotas consumidas**:
  - `GET /search.php?s={query}` — busca de receitas por nome
  - `GET /filter.php?c={category}` — filtra receitas por categoria
  - `GET /lookup.php?i={id}` — detalhes de uma receita
  - `GET /categories.php` — lista de categorias de receitas

---

## Tecnologias

| Item | Tecnologia |
|------|-----------|
| Linguagem | Python 3.11 |
| Framework | FastAPI |
| Banco de dados | SQLite (via SQLAlchemy) |
| Autenticação | JWT (python-jose + passlib/bcrypt) |
| Documentação | Swagger UI (embutido no FastAPI) |
| HTTP Client | httpx |
| Container | Docker |

---

## Estrutura de pastas

```
mvp-backend/
├── app/
│   ├── main.py              # Entrada da aplicação
│   ├── database.py          # Configuração SQLAlchemy
│   ├── seed.py              # Dados iniciais (exercícios e alimentos)
│   ├── models/
│   │   └── models.py        # Modelos do banco de dados
│   ├── schemas/
│   │   └── schemas.py       # Schemas Pydantic (validação)
│   ├── middleware/
│   │   └── auth.py          # Autenticação JWT
│   ├── routes/
│   │   ├── auth.py          # POST /register, POST /login
│   │   ├── users.py         # GET/PUT /users/profile
│   │   ├── exercises.py     # GET /exercises
│   │   ├── workouts.py      # GET/POST/PUT/DELETE /workouts
│   │   ├── foods.py         # GET/POST/PUT/DELETE /foods
│   │   ├── meals.py         # GET/POST/DELETE /meals
│   │   └── external.py      # Integração APIs externas
│   └── services/
│       └── external_apis.py # Lógica de consumo das APIs externas
├── requirements.txt
├── Dockerfile
└── .env.example
```

---

## Instalação e execução local

### Pré-requisitos
- Python 3.11+
- pip

### Passos

```bash
# 1. Clone o repositório
git clone https://github.com/grazibehr/mvp-backend-to-fitness.git
cd mvp-backend-to-fitness

# 2. Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure as variáveis de ambiente
cp .env.example .env

# 5. Inicie o servidor
uvicorn app.main:app --reload --port 8000
```

A API estará disponível em: http://localhost:8000

Documentação Swagger: http://localhost:8000/docs

---

## Execução com Docker

```bash
# Build da imagem
docker build -t to-fitness-api .

# Executar o container
docker run -p 8000:8000 to-fitness-api
```

---

## Rotas disponíveis

| Método | Rota | Descrição | Auth |
|--------|------|-----------|------|
| POST | `/api/auth/register` | Cadastrar usuário | Não |
| POST | `/api/auth/login` | Login | Não |
| GET | `/api/users/profile` | Obter perfil | Sim |
| PUT | `/api/users/profile` | Atualizar perfil + calcular metas | Sim |
| GET | `/api/exercises` | Listar exercícios (filtros: muscle_group, difficulty, search) | Não |
| GET | `/api/exercises/muscle-groups` | Grupos musculares | Não |
| GET | `/api/workouts` | Listar treinos do usuário | Sim |
| POST | `/api/workouts` | Criar treino | Sim |
| PUT | `/api/workouts/{id}` | Atualizar treino | Sim |
| DELETE | `/api/workouts/{id}` | Excluir treino | Sim |
| GET | `/api/workouts/history` | Histórico de treinos | Sim |
| POST | `/api/workouts/history` | Registrar treino concluído | Sim |
| GET | `/api/foods` | Listar alimentos (filtros: category, search) | Não |
| POST | `/api/foods` | Cadastrar alimento personalizado | Sim |
| PUT | `/api/foods/{id}` | Atualizar alimento | Sim |
| DELETE | `/api/foods/{id}` | Excluir alimento | Sim |
| GET | `/api/meals` | Refeições do dia | Sim |
| GET | `/api/meals/summary` | Resumo nutricional do dia | Sim |
| POST | `/api/meals` | Criar refeição | Sim |
| POST | `/api/meals/{id}/items` | Adicionar item à refeição | Sim |
| DELETE | `/api/meals/items/{id}` | Remover item da refeição | Sim |
| DELETE | `/api/meals/{id}` | Excluir refeição | Sim |
| GET | `/api/external/foods/search` | Buscar alimentos — Open Food Facts | Não |
| GET | `/api/external/foods/barcode/{barcode}` | Buscar por código de barras | Não |
| GET | `/api/external/exercises/search` | Buscar exercícios — Wger | Não |
| GET | `/api/external/exercises/categories` | Categorias — Wger | Não |
| GET | `/api/external/exercises/muscles` | Músculos — Wger | Não |
| GET | `/api/external/recipes/search` | Buscar receitas — TheMealDB | Não |
| GET | `/api/external/recipes/categories` | Categorias de receitas — TheMealDB | Não |

> Acesse `/docs` para a documentação interativa completa (Swagger UI).
