# Arquivo: src/ui/app.py
import streamlit as st
import pandas as pd
import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.database.connector import DBConnector

st.set_page_config(page_title="FlexMedia Analytics", layout="wide", page_icon="📊")

# --- SIDEBAR ---
with st.sidebar:
    st.title("⚙️ Controle")
    driver_opt = st.radio("Fonte de Dados", ["SQLite (Local)", "Oracle Cloud"])
    limit_view = st.slider("Janela de Análise", 20, 200, 50)
    st.markdown("---")
    st.caption("v2.1 - Presença & Interação")

driver_code = "sqlite" if "SQLite" in driver_opt else "oracle"
db = DBConnector(driver=driver_code)

# --- MAIN ---
st.title("📊 FlexMedia Analytics")
st.markdown("### Integração de Sensores: Presença vs. Toque")

placeholder = st.empty()

while True:
    df = db.ler_dados(limit=limit_view)
    total = db.contar_total()

    with placeholder.container():
        if not df.empty:
            # Tratamento de dados (Garantir numérico)
            cols = ['tempo_permanencia', 'tempo_interacao']
            for col in cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

            # --- KPIS DE NEGÓCIO ---
            k1, k2, k3, k4 = st.columns(4)
            k1.metric("Total de Sessões", total)
            
            # Cálculo da Taxa de Conversão (Quem tocou / Quem parou)
            # Consideramos conversão se tempo_interacao > 0
            conversoes = df[df['tempo_interacao'] > 0].shape[0]
            taxa = (conversoes / len(df)) * 100 if len(df) > 0 else 0
            
            k2.metric("Taxa de Conversão", f"{taxa:.1f}%")
            
            media_perm = df['tempo_permanencia'].mean()
            k3.metric("Tempo Médio (Presença)", f"{media_perm:.1f}s")
            
            media_int = df['tempo_interacao'].mean()
            k4.metric("Tempo Médio (Uso)", f"{media_int:.1f}s")

            # --- VISUALIZAÇÃO ESTATÍSTICA ---
            col_chart1, col_chart2 = st.columns(2)
            
            with col_chart1:
                st.subheader("📉 Funil de Engajamento (Scatter)")
                st.caption("Relação: Quanto mais tempo fica, mais interage?")
                # Scatter Plot nativo do Streamlit
                st.scatter_chart(
                    df,
                    x='tempo_permanencia',
                    y='tempo_interacao',
                    color='tipo_interacao',
                    size='tempo_interacao'
                )

            with col_chart2:
                st.subheader("⏱️ Linha do Tempo")
                st.line_chart(df[['tempo_permanencia', 'tempo_interacao']])

            with st.expander("🔎 Dados Brutos do Sensor"):
                st.dataframe(df, use_container_width=True)
        else:
            st.warning("Aguardando dados dos sensores...")
            
    time.sleep(2)