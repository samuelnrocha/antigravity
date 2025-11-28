import os
import sys

# Adiciona o diretório atual ao path para importações funcionarem
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("🚀 FlexMedia System está pronto!")
    print("Para rodar o dashboard: streamlit run src/ui/app.py")
