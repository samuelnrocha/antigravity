# Arquivo: src/ui/app.py
import streamlit as st
import pandas as pd
import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.database.connector import DBConnector
from src.ml_engine.predictor import FlexPredictor
import src.ui.charts as charts

st.set_page_config(page_title="FlexMedia Enterprise", layout="wide", page_icon="🏢")

# --- CACHE & SETUP ---
@st.cache_resource
def load_ai():
    return FlexPredictor()

ai_brain = load_ai()

# --- SIDEBAR (INPUTS) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3094/3094843.png", width=80)
    st.title("FlexMedia Control")
    st.markdown("---")
    
    driver_opt = st.radio("Fonte de Dados", ["SQLite (Local)", "Oracle Cloud"])
    limit_view = st.slider("Janela de Dados", 50, 1000, 200)
    
    st.markdown("### 📍 Filtros")

# Inicialização DB
driver_code = "sqlite" if "SQLite" in driver_opt else "oracle"
db = DBConnector(driver=driver_code)

# Pre-load da lista de totens
try:
    df_init = db.ler_dados(limit=500)
    lista_totens = ["Todos"] + sorted(df_init['id_sensor'].unique().tolist()) if not df_init.empty else ["Todos"]
except:
    lista_totens = ["Todos"]

with st.sidebar:
    filtro_totem = st.selectbox("Selecione o Totem:", lista_totens)
    st.info("Pressione 'R' para recarregar se novos totens surgirem.")

# --- MAIN PAGE ---
st.title("🏢 Dashboard Integrado de Inteligência")
st.markdown(f"Monitoramento em tempo real • Driver: **{driver_opt}**")

placeholder = st.empty()

while True:
    # 1. Coleta
    df = db.ler_dados(limit=limit_view)
    total_db = db.contar_total()

    # 2. Filtro
    df_filtered = df.copy()
    if filtro_totem != "Todos":
        df_filtered = df[df['id_sensor'] == filtro_totem]

    with placeholder.container():
        if not df_filtered.empty:
            # Tratamento
            cols_num = ['tempo_permanencia', 'tempo_interacao', 'tempo_resposta_ms']
            for c in cols_num:
                if c in df_filtered.columns:
                    df_filtered[c] = pd.to_numeric(df_filtered[c], errors='coerce').fillna(0)

            # --- BLOCO 1: KPIs & IA (Sempre visíveis) ---
            charts.render_kpis(df_filtered, len(df_filtered))
            
            # IA validando o último registro
            ultimo_dado = df_filtered.iloc[0]
            pred, proba = ai_brain.predict(ultimo_dado['tempo_permanencia'], ultimo_dado['tempo_interacao'])
            charts.render_ml_insights(ultimo_dado, pred, proba)

            st.divider()

            # --- BLOCO 2: Análise Profunda (ABAS) ---
            tab_cliente, tab_biz, tab_tech = st.tabs([
                "👥 Comportamento (V2)", 
                "📊 Inteligência de Negócio (V3)", 
                "⚡ Técnica & UX"
            ])

            with tab_cliente:
                # AQUI voltaram os gráficos de dispersão e tempo!
                charts.render_analise_comportamental(df_filtered)
            
            with tab_biz:
                # Aqui ficam as tendências e ranking
                charts.render_analise_temporal_ranking(df_filtered)
                
            with tab_tech:
                # Aqui ficam latência e comandos
                charts.render_analise_tecnica(df_filtered)

            # --- BLOCO 3: Dados ---
            charts.render_tabela(df_filtered)

        else:
            if filtro_totem != "Todos" and not df.empty:
                st.warning(f"Sem dados para o filtro: {filtro_totem}")
            else:
                st.info("Aguardando fluxo de dados...")
    
    time.sleep(2)