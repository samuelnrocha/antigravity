# Arquivo: src/database/connector.py
import sqlite3
import pandas as pd
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH)

# --- VERSÃO 3: Adicionando Comandos e Latência ---
TABLE_NAME = "FLEXMEDIA_LIVE_V3"

db_type = os.getenv("DB_TYPE", "sqlite")
print(f"--- [CONFIG] Banco definido como: {db_type.upper()} ---")

try:
    import oracledb
    ORACLE_AVAILABLE = True
except ImportError:
    ORACLE_AVAILABLE = False

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
            if not ORACLE_AVAILABLE: raise Exception("Biblioteca 'oracledb' necessária.")
            user = os.getenv("ORACLE_USER")
            password = os.getenv("ORACLE_PASS")
            dsn = os.getenv("ORACLE_DSN")
            return oracledb.connect(user=user, password=password, dsn=dsn)
        
    def init_db(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Schema V3: Adicionado acao, latencia e status
        if self.driver == "sqlite":
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    id_sensor TEXT,
                    tempo_permanencia REAL,
                    tempo_interacao REAL,
                    acao_usuario TEXT,
                    tempo_resposta_ms INTEGER,
                    status_sistema TEXT,
                    tipo_interacao TEXT
                )
            ''')
        
        elif self.driver == "oracle":
            try:
                # Criação segura no Oracle
                sql_create = f"""
                    CREATE TABLE {TABLE_NAME} (
                        id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                        timestamp DATE DEFAULT SYSDATE,
                        id_sensor VARCHAR2(50),
                        tempo_permanencia NUMBER(10,2),
                        tempo_interacao NUMBER(10,2),
                        acao_usuario VARCHAR2(50),
                        tempo_resposta_ms NUMBER(10),
                        status_sistema VARCHAR2(20),
                        tipo_interacao VARCHAR2(50)
                    )
                """
                cursor.execute(sql_create)
                print(f"✅ Tabela {TABLE_NAME} criada no Oracle.")
            except Exception:
                pass

        conn.commit()
        conn.close()
    
    def contar_total(self):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}")
            total = cursor.fetchone()[0]
            conn.close()
            return total
        except Exception:
            return 0

    def salvar_interacao(self, dados):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Preparando dados (Fallback para None se não houver ação)
            acao = dados.get('acao_usuario', 'Nenhuma')
            latencia = dados.get('tempo_resposta_ms', 0)
            status = dados.get('status_sistema', 'N/A')

            if self.driver == "sqlite":
                cursor.execute(f'''
                    INSERT INTO {TABLE_NAME} 
                    (timestamp, id_sensor, tempo_permanencia, tempo_interacao, acao_usuario, tempo_resposta_ms, status_sistema, tipo_interacao)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (dados['timestamp'], dados['id_sensor'], dados['tempo_permanencia'], dados['tempo_interacao'], acao, latencia, status, dados['tipo_interacao']))
            
            elif self.driver == "oracle":
                sql = f"""
                    INSERT INTO {TABLE_NAME} 
                    (id_sensor, tempo_permanencia, tempo_interacao, acao_usuario, tempo_resposta_ms, status_sistema, tipo_interacao)
                    VALUES (:1, :2, :3, :4, :5, :6, :7) 
                """
                cursor.execute(sql, (dados['id_sensor'], dados['tempo_permanencia'], dados['tempo_interacao'], acao, latencia, status, dados['tipo_interacao']))

            conn.commit()
            conn.close()
        except Exception as e:
            print(f"[ERRO AO SALVAR] {e}")

    def ler_dados(self, limit=50):
            try:
                conn = self.get_connection()
                if self.driver == "sqlite":
                    query = f"SELECT * FROM {TABLE_NAME} ORDER BY id DESC LIMIT {limit}"
                else:
                    query = f"""
                        SELECT id, timestamp, id_sensor, 
                            tempo_permanencia, 
                            tempo_interacao,
                            acao_usuario,
                            tempo_resposta_ms,
                            status_sistema,
                            tipo_interacao 
                        FROM {TABLE_NAME} 
                        ORDER BY id DESC 
                        FETCH FIRST {limit} ROWS ONLY
                    """
                df = pd.read_sql(query, conn)
                df.columns = df.columns.str.lower()
                conn.close()

                # --- LIMPEZA DE DADOS (DATA CLEANING) ---
                if not df.empty:
                    # 1. Remove duplicatas exatas (caso o sensor tenha enviado 2x)
                    # Ignoramos a coluna 'id' pois ela é sempre única no banco
                    subset_cols = [c for c in df.columns if c != 'id']
                    duplicadas = df.duplicated(subset=subset_cols).sum()
                    if duplicadas > 0:
                        df = df.drop_duplicates(subset=subset_cols)
                        # print(f"🧹 Limpeza: {duplicadas} registros duplicados removidos.")

                return df
            except Exception:
                return pd.DataFrame()