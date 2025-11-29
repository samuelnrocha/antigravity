# Arquivo: src/database/connector.py
import sqlite3
import pandas as pd
import os
from pathlib import Path
from dotenv import load_dotenv

# --- CONFIGURAÇÃO ---
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH)

# Debug
db_type = os.getenv("DB_TYPE", "sqlite")
print(f"--- [CONFIG] Banco definido como: {db_type.upper()} ---")

try:
    import oracledb
    ORACLE_AVAILABLE = True
except ImportError:
    ORACLE_AVAILABLE = False
    print("--- [AVISO] 'oracledb' não instalado. ---")

DB_SQLITE_PATH = BASE_DIR / "data" / "processed" / "flexmedia.db"

class DBConnector:
    def __init__(self, driver=None):
        if driver:
            self.driver = driver
        else:
            self.driver = os.getenv("DB_TYPE", "sqlite").lower()
    
    def get_connection(self):
        if self.driver == "sqlite":
            os.makedirs(os.path.dirname(DB_SQLITE_PATH), exist_ok=True)
            return sqlite3.connect(str(DB_SQLITE_PATH))
        
        elif self.driver == "oracle":
            if not ORACLE_AVAILABLE:
                raise Exception("Biblioteca 'oracledb' necessária.")
            
            user = os.getenv("ORACLE_USER")
            password = os.getenv("ORACLE_PASS")
            dsn = os.getenv("ORACLE_DSN")
            
            if not (user and password and dsn):
                raise Exception("Credenciais Oracle incompletas no .env")
                
            return oracledb.connect(user=user, password=password, dsn=dsn)
        
    def init_db(self):
        """Cria tabela no SQLite com novos campos."""
        if self.driver == "sqlite":
            conn = self.get_connection()
            cursor = conn.cursor()
            # Adicionado campo 'tempo_permanencia'
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS interacoes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    id_sensor TEXT,
                    tempo_permanencia REAL,
                    tempo_interacao REAL,
                    tipo_interacao TEXT
                )
            ''')
            conn.commit()
            conn.close()
    
    def contar_total(self):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            table = "interacoes" if self.driver == "sqlite" else "interacoes_totem"
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            total = cursor.fetchone()[0]
            conn.close()
            return total
        except Exception:
            return 0

    def salvar_interacao(self, dados):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            if self.driver == "sqlite":
                cursor.execute('''
                    INSERT INTO interacoes (timestamp, id_sensor, tempo_permanencia, tempo_interacao, tipo_interacao)
                    VALUES (?, ?, ?, ?, ?)
                ''', (dados['timestamp'], dados['id_sensor'], dados['tempo_permanencia'], dados['tempo_interacao'], dados['tipo_interacao']))
            
            elif self.driver == "oracle":
                # Mapeamento para Oracle (Assumindo colunas criadas)
                # Vamos usar: VALOR = tempo_interacao, e vamos precisar criar uma nova coluna TEMPO_PERMANENCIA no Oracle via script ou o hotfix do simulador
                sql = """
                    INSERT INTO interacoes_totem (id_sensor, tempo_permanencia, valor, tipo_interacao)
                    VALUES (:1, :2, :3, :4) 
                """
                cursor.execute(sql, (dados['id_sensor'], dados['tempo_permanencia'], dados['tempo_interacao'], dados['tipo_interacao']))

            conn.commit()
            conn.close()
        except Exception as e:
            print(f"[ERRO AO SALVAR] {e}")

    def ler_dados(self, limit=50):
        try:
            conn = self.get_connection()
            if self.driver == "sqlite":
                query = f"SELECT * FROM interacoes ORDER BY id DESC LIMIT {limit}"
            else:
                # Alias para padronizar o DataFrame
                query = f"""
                    SELECT id, timestamp, id_sensor, 
                           tempo_permanencia, 
                           valor as tempo_interacao, 
                           tipo_interacao 
                    FROM interacoes_totem 
                    ORDER BY id DESC 
                    FETCH FIRST {limit} ROWS ONLY
                """
            df = pd.read_sql(query, conn)
            df.columns = df.columns.str.lower()
            conn.close()
            return df
        except Exception:
            return pd.DataFrame()