from app.database import SessionLocal, engine
from app.models.models import Base, Exercise, Food


def run_seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    if db.query(Exercise).count() > 0:
        db.close()
        return

    exercises = [
        # Peito
        {"name": "Supino Reto", "muscle_group": "Peito", "difficulty": "intermediate", "description": "Exercicio basico para desenvolvimento do peitoral", "contraindicated": ["shoulder_injury"]},
        {"name": "Supino Inclinado", "muscle_group": "Peito", "difficulty": "intermediate", "description": "Foco na parte superior do peitoral", "contraindicated": ["shoulder_injury"]},
        {"name": "Crucifixo", "muscle_group": "Peito", "difficulty": "beginner", "description": "Isolamento do peitoral", "contraindicated": ["shoulder_injury"]},
        {"name": "Flexao de Bracos", "muscle_group": "Peito", "difficulty": "beginner", "description": "Exercicio com peso corporal", "contraindicated": ["wrist_injury"]},
        {"name": "Crossover", "muscle_group": "Peito", "difficulty": "intermediate", "description": "Exercicio com cabos para definicao", "contraindicated": []},
        # Costas
        {"name": "Puxada Frontal", "muscle_group": "Costas", "difficulty": "intermediate", "description": "Desenvolvimento da largura das costas", "contraindicated": ["shoulder_injury"]},
        {"name": "Remada Curvada", "muscle_group": "Costas", "difficulty": "intermediate", "description": "Espessura das costas", "contraindicated": ["back_pain"]},
        {"name": "Remada Unilateral", "muscle_group": "Costas", "difficulty": "beginner", "description": "Trabalho unilateral das costas", "contraindicated": []},
        {"name": "Pulldown", "muscle_group": "Costas", "difficulty": "beginner", "description": "Maquina para costas", "contraindicated": []},
        {"name": "Barra Fixa", "muscle_group": "Costas", "difficulty": "advanced", "description": "Exercicio avancado com peso corporal", "contraindicated": ["shoulder_injury"]},
        # Pernas
        {"name": "Agachamento Livre", "muscle_group": "Pernas", "difficulty": "intermediate", "description": "Exercicio fundamental para pernas", "contraindicated": ["knee_injury", "back_pain"]},
        {"name": "Leg Press", "muscle_group": "Pernas", "difficulty": "beginner", "description": "Maquina para quadriceps", "contraindicated": ["knee_injury"]},
        {"name": "Cadeira Extensora", "muscle_group": "Pernas", "difficulty": "beginner", "description": "Isolamento do quadriceps", "contraindicated": ["knee_injury"]},
        {"name": "Mesa Flexora", "muscle_group": "Pernas", "difficulty": "beginner", "description": "Isolamento do posterior", "contraindicated": []},
        {"name": "Stiff", "muscle_group": "Pernas", "difficulty": "intermediate", "description": "Posterior de coxa e gluteos", "contraindicated": ["back_pain"]},
        {"name": "Panturrilha em Pe", "muscle_group": "Pernas", "difficulty": "beginner", "description": "Desenvolvimento da panturrilha", "contraindicated": []},
        # Ombros
        {"name": "Desenvolvimento", "muscle_group": "Ombros", "difficulty": "intermediate", "description": "Exercicio principal para ombros", "contraindicated": ["shoulder_injury"]},
        {"name": "Elevacao Lateral", "muscle_group": "Ombros", "difficulty": "beginner", "description": "Isolamento do deltoide lateral", "contraindicated": ["shoulder_injury"]},
        {"name": "Elevacao Frontal", "muscle_group": "Ombros", "difficulty": "beginner", "description": "Deltoide anterior", "contraindicated": ["shoulder_injury"]},
        {"name": "Face Pull", "muscle_group": "Ombros", "difficulty": "beginner", "description": "Deltoide posterior e manguito", "contraindicated": []},
        # Biceps
        {"name": "Rosca Direta", "muscle_group": "Biceps", "difficulty": "beginner", "description": "Exercicio basico para biceps", "contraindicated": []},
        {"name": "Rosca Alternada", "muscle_group": "Biceps", "difficulty": "beginner", "description": "Trabalho unilateral do biceps", "contraindicated": []},
        {"name": "Rosca Martelo", "muscle_group": "Biceps", "difficulty": "beginner", "description": "Braquial e biceps", "contraindicated": []},
        {"name": "Rosca Scott", "muscle_group": "Biceps", "difficulty": "intermediate", "description": "Isolamento do biceps", "contraindicated": []},
        # Triceps
        {"name": "Triceps Pulley", "muscle_group": "Triceps", "difficulty": "beginner", "description": "Exercicio basico para triceps", "contraindicated": []},
        {"name": "Triceps Frances", "muscle_group": "Triceps", "difficulty": "intermediate", "description": "Cabeca longa do triceps", "contraindicated": ["elbow_injury"]},
        {"name": "Triceps Testa", "muscle_group": "Triceps", "difficulty": "intermediate", "description": "Isolamento do triceps", "contraindicated": ["elbow_injury"]},
        {"name": "Mergulho", "muscle_group": "Triceps", "difficulty": "intermediate", "description": "Exercicio com peso corporal", "contraindicated": ["shoulder_injury"]},
        # Abdomen
        {"name": "Abdominal Crunch", "muscle_group": "Abdomen", "difficulty": "beginner", "description": "Exercicio basico de abdomen", "contraindicated": ["back_pain"]},
        {"name": "Prancha", "muscle_group": "Abdomen", "difficulty": "beginner", "description": "Isometrico para core", "contraindicated": []},
        {"name": "Elevacao de Pernas", "muscle_group": "Abdomen", "difficulty": "intermediate", "description": "Abdomen inferior", "contraindicated": ["back_pain"]},
        {"name": "Russian Twist", "muscle_group": "Abdomen", "difficulty": "intermediate", "description": "Obliquos", "contraindicated": ["back_pain"]},
    ]

    foods = [
        # Proteinas
        {"name": "Frango Grelhado", "category": "Proteinas", "calories": 165, "protein": 31, "carbs": 0, "fat": 3.6, "portion_size": 100, "portion_description": "100g"},
        {"name": "Ovo Inteiro", "category": "Proteinas", "calories": 155, "protein": 13, "carbs": 1.1, "fat": 11, "portion_size": 100, "portion_description": "2 unidades"},
        {"name": "Clara de Ovo", "category": "Proteinas", "calories": 52, "protein": 11, "carbs": 0.7, "fat": 0.2, "portion_size": 100, "portion_description": "100g"},
        {"name": "Carne Bovina Magra", "category": "Proteinas", "calories": 250, "protein": 26, "carbs": 0, "fat": 15, "portion_size": 100, "portion_description": "100g"},
        {"name": "Peixe Tilapia", "category": "Proteinas", "calories": 128, "protein": 26, "carbs": 0, "fat": 2.7, "portion_size": 100, "portion_description": "100g"},
        {"name": "Atum em Agua", "category": "Proteinas", "calories": 116, "protein": 26, "carbs": 0, "fat": 0.8, "portion_size": 100, "portion_description": "100g"},
        {"name": "Whey Protein", "category": "Proteinas", "calories": 120, "protein": 24, "carbs": 3, "fat": 1.5, "portion_size": 30, "portion_description": "1 scoop (30g)"},
        # Carboidratos
        {"name": "Arroz Branco", "category": "Carboidratos", "calories": 130, "protein": 2.7, "carbs": 28, "fat": 0.3, "portion_size": 100, "portion_description": "100g"},
        {"name": "Arroz Integral", "category": "Carboidratos", "calories": 111, "protein": 2.6, "carbs": 23, "fat": 0.9, "portion_size": 100, "portion_description": "100g"},
        {"name": "Batata Doce", "category": "Carboidratos", "calories": 86, "protein": 1.6, "carbs": 20, "fat": 0.1, "portion_size": 100, "portion_description": "100g"},
        {"name": "Macarrao", "category": "Carboidratos", "calories": 131, "protein": 5, "carbs": 25, "fat": 1.1, "portion_size": 100, "portion_description": "100g"},
        {"name": "Pao Integral", "category": "Carboidratos", "calories": 247, "protein": 13, "carbs": 41, "fat": 4.2, "portion_size": 100, "portion_description": "2 fatias"},
        {"name": "Aveia", "category": "Carboidratos", "calories": 389, "protein": 17, "carbs": 66, "fat": 7, "portion_size": 100, "portion_description": "100g"},
        {"name": "Banana", "category": "Carboidratos", "calories": 89, "protein": 1.1, "carbs": 23, "fat": 0.3, "portion_size": 100, "portion_description": "1 unidade media"},
        # Gorduras
        {"name": "Azeite de Oliva", "category": "Gorduras", "calories": 884, "protein": 0, "carbs": 0, "fat": 100, "portion_size": 15, "portion_description": "1 colher de sopa"},
        {"name": "Amendoim", "category": "Gorduras", "calories": 567, "protein": 26, "carbs": 16, "fat": 49, "portion_size": 30, "portion_description": "30g"},
        {"name": "Castanha de Caju", "category": "Gorduras", "calories": 553, "protein": 18, "carbs": 30, "fat": 44, "portion_size": 30, "portion_description": "30g"},
        {"name": "Abacate", "category": "Gorduras", "calories": 160, "protein": 2, "carbs": 9, "fat": 15, "portion_size": 100, "portion_description": "100g"},
        # Laticinios
        {"name": "Leite Desnatado", "category": "Laticinios", "calories": 34, "protein": 3.4, "carbs": 5, "fat": 0.1, "portion_size": 100, "portion_description": "100ml"},
        {"name": "Iogurte Natural", "category": "Laticinios", "calories": 61, "protein": 3.5, "carbs": 4.7, "fat": 3.3, "portion_size": 100, "portion_description": "100g"},
        {"name": "Queijo Cottage", "category": "Laticinios", "calories": 98, "protein": 11, "carbs": 3.4, "fat": 4.3, "portion_size": 100, "portion_description": "100g"},
        {"name": "Queijo Minas", "category": "Laticinios", "calories": 264, "protein": 17, "carbs": 3, "fat": 20, "portion_size": 30, "portion_description": "1 fatia"},
        # Vegetais
        {"name": "Brocolis", "category": "Vegetais", "calories": 34, "protein": 2.8, "carbs": 7, "fat": 0.4, "fiber": 2.6, "portion_size": 100, "portion_description": "100g"},
        {"name": "Espinafre", "category": "Vegetais", "calories": 23, "protein": 2.9, "carbs": 3.6, "fat": 0.4, "fiber": 2.2, "portion_size": 100, "portion_description": "100g"},
        {"name": "Alface", "category": "Vegetais", "calories": 15, "protein": 1.4, "carbs": 2.9, "fat": 0.2, "fiber": 1.3, "portion_size": 100, "portion_description": "100g"},
        {"name": "Tomate", "category": "Vegetais", "calories": 18, "protein": 0.9, "carbs": 3.9, "fat": 0.2, "fiber": 1.2, "portion_size": 100, "portion_description": "100g"},
        {"name": "Cenoura", "category": "Vegetais", "calories": 41, "protein": 0.9, "carbs": 10, "fat": 0.2, "fiber": 2.8, "portion_size": 100, "portion_description": "100g"},
    ]

    db.bulk_insert_mappings(Exercise, exercises)
    db.bulk_insert_mappings(Food, foods)
    db.commit()
    db.close()
    print("Seed concluido com sucesso!")


if __name__ == "__main__":
    run_seed()
