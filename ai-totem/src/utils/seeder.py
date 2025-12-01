# Arquivo: src/utils/seeder.py
import sys
import os
import time

# Ajuste de path para importar módulos irmãos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.database.connector import DBConnector
from src.sensors.simulador import gerar_dados_complexos

def popular_banco(qtd_registros=300):
    print(f"🌱 Iniciando Seeding de {qtd_registros} registros...")
    
    db = DBConnector()
    db.init_db() # Garante que a tabela existe
    
    start_time = time.time()
    
    for i in range(qtd_registros):
        # Gera o dado usando a lógica complexa (com latência, comandos, etc)
        dado = gerar_dados_complexos()
        
        # Salva no banco
        db.salvar_interacao(dado)
        
        # Barra de progresso visual simples
        if i % 10 == 0:
            sys.stdout.write(f"\rProcessando: {i}/{qtd_registros} ({(i/qtd_registros)*100:.1f}%)")
            sys.stdout.flush()
            
    end_time = time.time()
    print(f"\n✅ Concluído! {qtd_registros} registros inseridos em {end_time - start_time:.2f} segundos.")
    print(f"🎯 Banco alvo: {db.driver.upper()}")

if __name__ == "__main__":
    # Pergunta quantos dados quer gerar (padrão 300)
    try:
        qtd = int(input("Quantos registros deseja gerar? [300]: ") or 300)
    except ValueError:
        qtd = 300
        
    popular_banco(qtd)