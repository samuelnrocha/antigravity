import os
from dotenv import load_dotenv

load_dotenv()

# Configurações do Banco
DB_TYPE = os.getenv("DB_TYPE", "sqlite") # sqlite ou oracle
ORACLE_USER = os.getenv("ORACLE_USER", "")
ORACLE_PASS = os.getenv("ORACLE_PASS", "")
ORACLE_DSN = os.getenv("ORACLE_DSN", "")
