# Arquivo: src/sensors/simulator.py
import time
import random
import datetime
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.database.connector import DBConnector

def gerar_dados_inteligentes():
    sensores = ["totem_entrada", "totem_praca", "quiosque_food"]
    sensor = random.choice(sensores)
    
    # 1. Simula Sensor de Presença (Ultrassônico/ESP32-CAM)
    # A pessoa ficou entre 5s e 2 minutos na frente do totem
    tempo_permanencia = round(random.uniform(5.0, 120.0), 2)
    
    # 2. Simula Sensor de Toque (Capacitivo)
    # 60% de chance da pessoa interagir se ela parou
    interagiu = random.choice([True, False, True]) # 66% chance
    
    if interagiu:
        # O tempo de toque é sempre MENOR que o tempo de presença
        fator = random.uniform(0.1, 0.9)
        tempo_interacao = round(tempo_permanencia * fator, 2)
        
        # Classificação para o ML
        if tempo_interacao > 20:
            tipo = "Engajado"
        elif tempo_interacao > 5:
            tipo = "Normal"
        else:
            tipo = "Curioso"
    else:
        tempo_interacao = 0.0
        tipo = "Ocioso" # Apenas olhou e saiu
    
    return {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "id_sensor": sensor,
        "tempo_permanencia": tempo_permanencia,
        "tempo_interacao": tempo_interacao,
        "tipo_interacao": tipo
    }

def hotfix_schema_oracle(db):
    """Garante que a tabela Oracle tenha as colunas novas."""
    if db.driver == 'oracle':
        conn = db.get_connection()
        cursor = conn.cursor()
        print("🔧 Verificando Schema do Oracle...")
        
        # 1. Ajustar 'valor' (Interação)
        try:
            cursor.execute("ALTER TABLE interacoes_totem MODIFY (valor NUMBER(10,2))")
        except: pass
        
        # 2. Criar 'tempo_permanencia'
        try:
            cursor.execute("ALTER TABLE interacoes_totem ADD (tempo_permanencia NUMBER(10,2) DEFAULT 0)")
            print("✅ Coluna 'TEMPO_PERMANENCIA' adicionada no Oracle.")
        except Exception as e:
            # Se já existir (ORA-01430), ignoramos
            pass
            
        conn.commit()
        conn.close()

if __name__ == "__main__":
    db = DBConnector()
    db.init_db()
    
    # # Tenta ajustar o Oracle se necessário
    # if db.driver == 'oracle':
    #     hotfix_schema_oracle(db)
    
    print(f"--- 📡 Simulador Multi-Sensor Iniciado ({db.driver.upper()}) ---")
    print("Gerando dados de Presença (ESP32-CAM) + Toque (ESP32)...")
    
    try:
        while True:
            dado = gerar_dados_inteligentes()
            db.salvar_interacao(dado)
            
            print(f"[{dado['id_sensor']}] Presença: {dado['tempo_permanencia']}s | Toque: {dado['tempo_interacao']}s -> {dado['tipo_interacao']}")
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nSimulação parada.")