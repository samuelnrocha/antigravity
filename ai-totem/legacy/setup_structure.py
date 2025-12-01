import os
from pathlib import Path

# Nome do projeto (Raiz)
PROJECT_NAME = "flexmedia_core"

# Estrutura de Pastas
DIRS = [
    "config",
    "data/raw",
    "data/processed",
    "data/models",
    "notebooks",
    "src/database",
    "src/ml_engine",
    "src/sensors",
    "src/ui",
]

# Conteúdo inicial dos Arquivos (Boilerplate)
FILES = {
    # Dependências
    "requirements.txt": """pandas
streamlit
scikit-learn
matplotlib
oracledb
python-dotenv
""",

    # Ignorar lixo e segredos
    ".gitignore": """__pycache__/
*.pyc
.env
.DS_Store
data/
!data/raw/.gitkeep
!data/processed/.gitkeep
!data/models/.gitkeep
""",

    # Configurações
    "config/settings.py": """import os
from dotenv import load_dotenv

load_dotenv()

# Configurações do Banco
DB_TYPE = os.getenv("DB_TYPE", "sqlite") # sqlite ou oracle
ORACLE_USER = os.getenv("ORACLE_USER", "")
ORACLE_PASS = os.getenv("ORACLE_PASS", "")
ORACLE_DSN = os.getenv("ORACLE_DSN", "")
""",

    # Arquivo de Segredos (Template)
    ".env": """DB_TYPE=sqlite
ORACLE_USER=rm550000
ORACLE_PASS=sua_senha_aqui
ORACLE_DSN=host_do_oracle
""",

    # Readme
    "README.md": """# 📡 FlexMedia Core

Sistema de Inteligência Artificial para Totens Interativos.

## Estrutura
- `src/`: Código fonte da aplicação.
- `data/`: Armazenamento de dados locais e modelos.
- `notebooks/`: Experimentos e análises exploratórias.

## Como Rodar
1. Instale as dependências: `pip install -r requirements.txt`
2. Rode o Dashboard: `streamlit run src/ui/app.py`
""",

    # Entry Point Simples
    "main.py": """import os
import sys

# Adiciona o diretório atual ao path para importações funcionarem
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("🚀 FlexMedia System está pronto!")
    print("Para rodar o dashboard: streamlit run src/ui/app.py")
""",
    
    # Placeholders para evitar erros de importação
    "src/__init__.py": "",
    "src/database/__init__.py": "",
    "src/ml_engine/__init__.py": "",
    "src/sensors/__init__.py": "",
    "src/ui/__init__.py": "",
    
    # Arquivo vazio para o git manter as pastas de dados
    "data/raw/.gitkeep": "",
    "data/processed/.gitkeep": "",
    "data/models/.gitkeep": "",
}

def create_structure():
    base_path = Path.cwd()
    
    print(f"🔨 Construindo estrutura do projeto em: {base_path}")

    # 1. Criar Diretórios
    for directory in DIRS:
        dir_path = base_path / directory
        try:
            os.makedirs(dir_path, exist_ok=True)
            print(f"   [DIR]  Criado: {directory}")
        except Exception as e:
            print(f"   [ERRO] Falha ao criar {directory}: {e}")

    # 2. Criar Arquivos
    for file_path, content in FILES.items():
        full_path = base_path / file_path
        
        # Só cria se não existir para não sobrescrever trabalho feito
        if not full_path.exists():
            try:
                with open(full_path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"   [FILE] Criado: {file_path}")
            except Exception as e:
                print(f"   [ERRO] Falha ao criar {file_path}: {e}")
        else:
            print(f"   [SKIP] Já existe: {file_path}")

    print("\n✅ Estrutura 'Professional Grade' pronta! Let's code.")

if __name__ == "__main__":
    create_structure()