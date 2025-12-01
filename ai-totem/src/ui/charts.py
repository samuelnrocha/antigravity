# Arquivo: src/ui/charts.py
import streamlit as st
import pandas as pd
import altair as alt

def render_kpis(df, total_registros):
    """Renderiza a linha principal de indicadores."""
    # Tratamento de segurança
    for col in ['tempo_permanencia', 'tempo_interacao', 'tempo_resposta_ms']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    # Filtrando apenas quem interagiu
    interacoes = df[df['tempo_interacao'] > 0]
    engajados = df[df['tipo_interacao'] == 'Engajado']
    
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Sessões", total_registros)
    
    # Taxa de Engajamento Real (Engajados / Total)
    taxa_engajamento = (len(engajados) / len(df)) * 100 if len(df) > 0 else 0
    k2.metric("Taxa de Engajamento", f"{taxa_engajamento:.1f}%")
    
    # Tempo Médio (Presença vs Uso)
    media_perm = df['tempo_permanencia'].mean() if not df.empty else 0
    k3.metric("Tempo Médio (Presença)", f"{media_perm:.1f}s")
    
    # UX Score (Latência)
    latencia = df['tempo_resposta_ms'].mean() if not df.empty else 0
    status_ux = "Lento 🐢" if latencia > 1000 else "Fluido ⚡"
    k4.metric("Performance (Latência)", f"{latencia:.0f}ms", delta=status_ux, delta_color="inverse")

def render_ml_insights(ultima_interacao, predicao_ia, probabilidade):
    """Mostra o Cérebro da IA."""
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        st.caption("📡 Último Dado Recebido")
        st.write(f"**{ultima_interacao['id_sensor']}**")
        st.write(f"Presença: {ultima_interacao['tempo_permanencia']}s")
        
    with col2:
        st.caption("🧠 Análise em Tempo Real (IA)")
        cor_barra = "green" if predicao_ia == "Engajado" else "orange"
        st.progress(float(probabilidade))
        st.markdown(f"Classificação: **:{cor_barra}[{predicao_ia}]** ({probabilidade*100:.1f}% confiança)")
        
    with col3:
        st.caption("🎯 Ação Sugerida")
        if predicao_ia == "Engajado":
            st.success("Oferecer Promoção")
        elif predicao_ia == "Normal":
            st.info("Exibir Menu")
        else:
            st.warning("Atrair Atenção")

def render_analise_comportamental(df):
    """(RECUPERADO) Gráficos V2: Dispersão e Tempos."""
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("📉 Funil de Engajamento")
        st.caption("Quem fica mais tempo, interage mais?")
        if not df.empty:
            # O gráfico que você sentiu falta!
            st.scatter_chart(
                df,
                x='tempo_permanencia',
                y='tempo_interacao',
                color='tipo_interacao',
                size='tempo_interacao',
                height=300
            )
            
    with c2:
        st.subheader("⏱️ Presença vs. Interação")
        st.caption("Média de tempo por perfil de usuário")
        if not df.empty:
            # Compara média de presença vs interação
            chart_data = df.groupby('tipo_interacao')[['tempo_permanencia', 'tempo_interacao']].mean()
            st.bar_chart(chart_data, height=300)

def render_analise_temporal_ranking(df):
    """Gráficos V3: Tendências e Ranking."""
    # Preparação
    if 'timestamp' in df.columns:
        df['data_hora'] = pd.to_datetime(df['timestamp'])
        df['dia_semana'] = df['data_hora'].dt.day_name()
        df['hora'] = df['data_hora'].dt.hour

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("📅 Tendência Semanal")
        engajados_por_dia = df[df['tipo_interacao'] == 'Engajado']['dia_semana'].value_counts()
        if not engajados_por_dia.empty:
            st.bar_chart(engajados_por_dia, height=250)
        else:
            st.info("Sem dados suficientes.")
            
    with c2:
        st.subheader("🏆 Top Totens (Engajamento)")
        ranking = df[df['tipo_interacao'] == 'Engajado']['id_sensor'].value_counts()
        if not ranking.empty:
            st.bar_chart(ranking, height=250, color="#FF4B4B") # Cor destaque
        else:
            st.info("Sem engajamento para rankear.")

def render_analise_tecnica(df):
    """Gráficos de Performance e Comandos."""
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("🔥 Mapa de Calor de Ações")
        df_cmds = df[df['acao_usuario'] != 'Nenhuma']['acao_usuario'].value_counts()
        if not df_cmds.empty:
            st.bar_chart(df_cmds, height=250)
            
    with c2:
        st.subheader("⚡ Monitor de Latência (ms)")
        df_lat = df[df['tempo_resposta_ms'] > 0].reset_index()
        if not df_lat.empty:
            st.line_chart(df_lat, y='tempo_resposta_ms', height=250)

def render_tabela(df):
    with st.expander("🔎 Auditoria dos Dados (Tabela Completa)"):
        st.dataframe(df, use_container_width=True)