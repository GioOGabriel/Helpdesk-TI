import sqlite3  
import pandas as pd
import streamlit as st
import datetime
import plotly.express as px

#Função de automação de alertas
def disparar_alerta_urgente(solicitante, categoria, descricao):
    #Alerta visual em tempo real na interface
    st.toast(":rotating_light: Chamado de alta prioridade registrado!", icon="🚨")
    st.warning(
        ":warning: Este chamado possui prioridade ALTA. A equipe de TI foi notificada para atendimento urgente."
    )

    #Registro automatico em arquivo de log de incidentes
    data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mensagem_log = f"[{data_hora}] ALERTA CRÍTICO | Solicitante: {solicitante} | Categoria: {categoria} | Descrição: {descricao}\n"

    with open("alertas_urgentes.log", "a", encoding="utf-8") as f:
        f.write(mensagem_log)

#Função pra garantir que a tabela seja criada automaticamente caso não exista
def init_db():
    conn = sqlite3.connect('helpdesk.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chamados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        solicitante TEXT NOT NULL,
        categoria TEXT NOT NULL,
        descricao TEXT NOT NULL,
        prioridade TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Aberto',
        data_abertura DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

init_db() #executando ao carregar o script


#Conexão com o banco de dados SQlite
def get_connection():
    return sqlite3.connect('helpdesk.db')

#Insere o chamado no banco de dados
def criar_chamado(solicitante, categoria, descricao, prioridade):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO chamados (solicitante, categoria, descricao, prioridade)
        VALUES (?, ?, ?, ?)
    """,
        (solicitante, categoria, descricao, prioridade)
    )
    conn.commit()
    conn.close()

#Função para buscar todos os chamados salvos
def buscar_chamados():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM chamados ORDER BY id DESC", conn)
    conn.close()
    return df

#Função para atualizar o status do chamado
def atualizar_status(chamado_id, novo_status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE chamados SET status = ? WHERE id = ?
    """,
        (novo_status, chamado_id)
    )
    conn.commit()
    conn.close()

#Layout da pagina no streamlit
st.set_page_config(page_title="Helpdesk TI", page_icon=":computer:", layout="wide") 
st.title("Sistema de Helpdesk & Suporte de TI")

#Divisão das abas
aba1, aba2, aba3 = st.tabs([":pushpin: Abrir Chamado", ":hammer_and_wrench: Painel do Técnico (TI)", ":bar_chart: Dashboard e Métricas"])

#Aba 1: visão do usuario
with aba1:
    st.header("Registrar Novo Chamado")

    with st.form("form_chamado", clear_on_submit=True):
        solicitante = st.text_input("Seu Nome / Setor")
        categoria = st.selectbox(
            "Categoria do Problema",
            ["Hardware", "Rede/Internet", "Software/Sistemas", "Acessos", "Outros"]
        )
        prioridade = st.selectbox("Prioridade", ["Baixa", "Média", "Alta"])
        descricao = st.text_area("Descrição detalhada do problema")

        submetido = st.form_submit_button("Enviar Chamado")

        if submetido:
            if solicitante and descricao:
                criar_chamado(solicitante, categoria, descricao, prioridade)
                st.success("Chamado registrado com sucesso!")

                #Disparar a automação se a prioridade for ALTA
                if prioridade == "Alta":
                    disparar_alerta_urgente(solicitante, categoria, descricao)
            else:
                st.error("Por favor, preencha todos os campos obrigatórios.")

#Aba 2: visao da equipe de TI
with aba2:
    st.header("Gerenciamento de Chamados")

    df_chamados = buscar_chamados()

    if df_chamados.empty:
        st.info("Nenhum chamado registrado até o momento.")
    else:
        st.subheader("Lista de Incidentes Registrados")
        st.dataframe(df_chamados, use_container_width=True)

        st.divider()
        st.subheader("Atualizar Status do Chamado")

        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            chamado_id = st.selectbox(
                "ID do Chamado", df_chamados["id"].tolist()
            )
        with col2:
            novo_status = st.selectbox(
                "Novo Status", ["Aberto", "Em andamento", "Concluído"]
            )
        with col3:
            st.write("")
            st.write("")
            if st.button("Salvar Alteração"):
                atualizar_status(chamado_id, novo_status)
                st.success(f"Status do chamado #{chamado_id} atualizado!")
                st.rerun()

#Aba 3: Dashboard e metricas
with aba3:
    st.header(":bar_chart: Painel de Indicadores e Métricas de Suporte")

    df_chamados = buscar_chamados()

    if df_chamados.empty:
        st.info("Nenhum dado disponível para exibir indicadores.")
    else:
        #Cartões de KPI
        total_chamados = len(df_chamados)
        chamados_abertos = len(df_chamados[df_chamados["status"] == "Aberto"])
        chamados_concluidos = len(
            df_chamados[df_chamados["prioridade"] == "Alta"]
        )
        chamados_criticos = len(
            df_chamados[df_chamados["prioridade"] == "Alta"]
        )

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total de Chamados", total_chamados)
        col2.metric("Em Aberto", chamados_abertos)
        col3.metric("Concluídos", chamados_concluidos)
        col4.metric("Incidentes Criticos", chamados_criticos)

        st.divider()

        #GRAFICOS INTERATIVOS
        col_graf1, col_graf2 = st.columns(2)

        with col_graf1:
            st.subheader("Volume por Categoria")
            fig_cat = px.histogram(
                df_chamados,
                x="categoria",
                color="categoria",
                title="Chamados por Categoria de TI",
                labels={"categoria": "Categoria", "count": "Quantidade"}
            )
            #Garante a ordenação e contagem correta no eixo Y
            fig_cat.update_layout(
                yaxis_title="Quantidade", xaxis_title="Categoria"
            )
            st.plotly_chart(fig_cat, use_container_width=True)
        with col_graf2:
            st.subheader("Distribuição por Prioridade")
            fig_prio = px.pie(
                df_chamados,
                names="prioridade",
                title="Proporção de Prioridade",
                hole=0.4,
                color_discrete_map={
                    "Alta": "#FF4B4B",
                    "Média": "#FFAA00",
                    "Baixa": "#00CC96",
                },
            )
            st.plotly_chart(fig_prio, use_container_width=True)

        st.divider()


#Exportação de dados para Power BI / Excel
st.subheader(":inbox_tray: Exportação de Dados")
csv = df_chamados.to_csv(index=False).encode("utf-8")
st.download_button(
    label = "Baixar Relatório em CSV (Para Power BI / Excel",
    data=csv,
    file_name="relatorio_chamados_ti.csv",
    mime="text/csv",
    )
