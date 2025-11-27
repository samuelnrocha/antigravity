import oracledb
import random
import time
from datetime import datetime

# --- CONFIGURAÇÃO ORACLE ---
# Preencha com suas credenciais da nuvem
ORACLE_USER = "rm568552"
ORACLE_PASS = "090505"
# O DSN geralmente parece com: "host:port/service_name"
ORACLE_DSN  = "oracle.fiap.com.br:1521/orcl" 

def conectar_oracle():
    """Cria e retorna uma conexão com o banco Oracle."""
    try:
        conn = oracledb.connect(user=ORACLE_USER, password=ORACLE_PASS, dsn=ORACLE_DSN)
        return conn
    except Exception as e:
        print(f"[ERRO] Falha ao conectar no Oracle: {e}")
        return None

def iniciar_banco():
    """Cria a tabela no Oracle se ela não existir."""
    conn = conectar_oracle()
    if not conn: return

    cursor = conn.cursor()
    
    # No Oracle, a sintaxe de criação é um pouco diferente.
    # Usamos GENERATED ALWAYS AS IDENTITY para o ID autoincremental (Oracle 12c+)
    sql_create = """
        BEGIN
            EXECUTE IMMEDIATE 'CREATE TABLE interacoes_totem (
                id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                timestamp DATE DEFAULT SYSDATE,
                id_sensor VARCHAR2(50),
                tipo_interacao VARCHAR2(50),
                valor NUMBER(1)
            )';
        EXCEPTION
            WHEN OTHERS THEN
                IF SQLCODE != -955 THEN -- Ignora erro se a tabela já existe
                    RAISE;
                END IF;
        END;
    """
    
    try:
        cursor.execute(sql_create)
        print("[SISTEMA] Tabela 'interacoes_totem' verificada/criada no Oracle.")
    except Exception as e:
        print(f"[ERRO] Falha na criação da tabela: {e}")
    finally:
        conn.close()

def simular_dados_sensor():
    """Gera dados simulados."""
    sensores = ["tela_toque", "sensor_presenca", "gatilho_camera"]
    sensor_ativo = random.choice(sensores)
    valor = 1 if random.random() > 0.3 else 0
    
    return {
        "id_sensor": sensor_ativo,
        "tipo_interacao": "usuario_detectado" if valor == 1 else "verificacao_ociosa",
        "valor": valor
    }

def salvar_no_oracle(dados):
    """Insere o dado simulado no Oracle."""
    conn = conectar_oracle()
    if not conn: return

    cursor = conn.cursor()
    
    # Sintaxe de insert Oracle usa :1, :2, :3 ou :nome para bind variables
    sql_insert = """
        INSERT INTO interacoes_totem (id_sensor, tipo_interacao, valor)
        VALUES (:1, :2, :3)
    """
    
    try:
        cursor.execute(sql_insert, (dados['id_sensor'], dados['tipo_interacao'], dados['valor']))
        conn.commit()
        print(f"[ORACLE CLOUD] Dado Persistido: {dados}")
    except Exception as e:
        print(f"[ERRO] Falha ao inserir: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    iniciar_banco()
    print("--- Iniciando Simulação Totem (Oracle Cloud) ---")
    
    try:
        while True:
            dados = simular_dados_sensor()
            salvar_no_oracle(dados)
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n[SISTEMA] Encerrado.")