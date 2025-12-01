# Arquivo: src/ml_engine/predictor.py
import pickle
import os
import pandas as pd

class FlexPredictor:
    def __init__(self):
        self.model_path = os.path.join(os.path.dirname(__file__), '../../data/models/interaction_classifier.pkl')
        self.model = self._load_model()

    def _load_model(self):
        if os.path.exists(self.model_path):
            with open(self.model_path, 'rb') as f:
                return pickle.load(f)
        return None

    def predict(self, tempo_permanencia, tempo_interacao):
        """Retorna a classificação (str) e a probabilidade (float)."""
        if not self.model:
            return "Modelo Não Treinado", 0.0
        
        # Cria dataframe com mesmos nomes de colunas do treino
        input_data = pd.DataFrame({
            'tempo_permanencia': [tempo_permanencia],
            'tempo_interacao': [tempo_interacao]
        })
        
        try:
            prediction = self.model.predict(input_data)[0]
            # Probabilidade da classe escolhida (confiança)
            proba = self.model.predict_proba(input_data).max()
            return prediction, proba
        except Exception as e:
            return "Erro ML", 0.0