# Arquivo: src/sensors/simulator.py
import time
import random
import datetime
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.database.connector import DBConnector
from src.core.schemas import InteracaoSchema # Importa o Validador
from pydantic import ValidationError

def gerar_dados_complexos():
    sensores = ["totem_entrada", "totem_praca", "quiosque_food"]
    acoes = ["ver_mapa", "cardapio", "promo_dia", "chamar_ajuda", "scan_qr"]
    
    sensor = random.choice(sensores)
    tempo_permanencia = round(random.uniform(3.0, 90.0), 2)
    
    # Lógica de Interação
    interagiu = random.choice([True, False, True])
    
    if interagiu:
        fator = random.uniform(0.2, 0.8)
        tempo_interacao = round(tempo_permanencia * fator, 2)
        acao_usuario = random.choice(acoes)
        tempo_resposta_ms = random.randint(20, 2500) if sensor == "totem_praca" else random.randint(20, 500)
        status_sistema = "SUCESSO" if random.random() > 0.05 else "ERRO_TIMEOUT"
        
        if tempo_interacao > 30: tipo = "Engajado"
        elif tempo_interacao > 10: tipo = "Normal"
        else: tipo = "Explorador"
    else:
        tempo_interacao = 0.0
        acao_usuario = "Nenhuma"
        tempo_resposta_ms = 0
        status_sistema = "N/A"
        tipo = "Ocioso"
    
    # Dados Brutos (Dicionário)
    raw_data = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "id_sensor": sensor,
        "tempo_permanencia": tempo_permanencia,
        "tempo_interacao": tempo_interacao,
        "tipo_interacao": tipo,
        "acao_usuario": acao_usuario,
        "tempo_resposta_ms": tempo_resposta_ms,
        "status_sistema": status_sistema
    }

    # --- A MÁGICA DA VALIDAÇÃO ---
    # Transformamos o dict bruto no Schema Validado.
    # Se houver erro, ele lança exceção e não retorna dado sujo.
    try:
        dado_limpo = InteracaoSchema(**raw_data)
        # Retorna o dicionário limpo e padronizado pelo Pydantic
        return dado_limpo.model_dump() 
    except ValidationError as e:
        print(f"❌ DADO RECUSADO PELO VALIDADOR: {e}")
        return None

if __name__ == "__main__":
    db = DBConnector()
    db.init_db()
    
    print(f"--- 📡 Simulador Enterprise (Validado) Iniciado ---")
    
    try:
        while True:
            dado_validado = gerar_dados_complexos()
            
            if dado_validado:
                # O banco só recebe se passou pelo Pydantic
                db.salvar_interacao(dado_validado)
                
                if dado_validado['tempo_interacao'] > 0:
                    print(f"✅ [{dado_validado['id_sensor']}] Validado & Salvo: {dado_validado['acao_usuario']}")
                else:
                    print(f"💤 [{dado_validado['id_sensor']}] Ocioso (Validado)")
            
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nSimulação parada.")