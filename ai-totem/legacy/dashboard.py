        conn = oracledb.connect(user=ORACLE_USER, password=ORACLE_PASS, dsn=ORACLE_DSN)
        
        # Oracle não suporta 'LIMIT', usa 'FETCH FIRST' ou ROWNUM.
        # Ordenamos decrescente para pegar os mais novos.
        query = """
            SELECT id, timestamp, id_sensor, tipo_interacao, valor 
            FROM interacoes_totem 
            ORDER BY id DESC 
            FETCH FIRST 50 ROWS ONLY
        """
        
        df = pd.read_sql(query, conn)
        df.columns = df.columns.str.lower()
        conn.close()
        return df
    except Exception as e:
        st.error(f"Erro de conexão com Oracle: {e}")
        return pd.DataFrame()

# --- INTERFACE ---
st.title("☁️ Dashboard Totem FlexMedia (Oracle Cloud)")

placeholder = st.empty()

while True:
    df = carregar_dados_oracle()

    with placeholder.container():
        if not df.empty:
            # Métricas
            col1, col2, col3 = st.columns(3)
            col1.metric("Registros Carregados", len(df))
            col2.metric("Interações (Últimas 50)", int(df[df['valor'] == 1]['valor'].count()))
            col3.metric("Último Sensor", df.iloc[0]['id_sensor'])

            # Gráfico
            st.subheader("Atividade Recente")
            # Precisamos garantir que timestamp seja datetime para o gráfico funcionar
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            st.line_chart(df.set_index('timestamp')['valor'])
            
            # Tabela
            st.dataframe(df)
        else:
            st.info("Aguardando dados ou conectando ao banco...")
            
    time.sleep(2)