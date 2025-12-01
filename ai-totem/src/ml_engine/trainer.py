# Arquivo: src/ml_engine/trainer.py
import pandas as pd
import pickle
import os
import sys

# Hack para importar módulos irmãos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.database.connector import DBConnector

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

def train_model():
    print("🤖 Iniciando treinamento do modelo de IA...")
    
    # 1. Carregar dados do Banco
    db = DBConnector()
    # Pega um bom volume de dados para treino (ex: 500 registros)
    df = db.ler_dados(limit=1000)
    
    if len(df) < 50:
        print("⚠️ Dados insuficientes! Rode o simulador por mais tempo antes de treinar.")
        return

    # 2. Prepara as Features (X) e o Alvo (y)
    # Vamos ensinar a IA: "Com base no tempo parado e no tempo de toque, qual o perfil?"
    
    # Garante numérico
    df['tempo_permanencia'] = pd.to_numeric(df['tempo_permanencia'], errors='coerce').fillna(0)
    df['tempo_interacao'] = pd.to_numeric(df['tempo_interacao'], errors='coerce').fillna(0)
    
    features = ['tempo_permanencia', 'tempo_interacao']
    target = 'tipo_interacao'
    
    X = df[features]
    y = df[target]

    # 3. Separa treino e teste (70% aprende, 30% faz prova)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # 4. Cria e Treina o Modelo (Random Forest)
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    # 5. Avalia a performance
    predictions = clf.predict(X_test)
    acc = accuracy_score(y_test, predictions)
    print(f"✅ Modelo treinado com Acurácia de: {acc*100:.2f}%")
    print("\nRelatório de Classificação:")
    print(classification_report(y_test, predictions))

    # 6. Salva o "Cérebro" na pasta data/models
    model_path = os.path.join(os.path.dirname(__file__), '../../data/models/interaction_classifier.pkl')
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    
    with open(model_path, 'wb') as f:
        pickle.dump(clf, f)
    print(f"💾 Modelo salvo em: {model_path}")

if __name__ == "__main__":
    train_model()