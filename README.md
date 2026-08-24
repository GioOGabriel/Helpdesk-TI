# 🖥️ Sistema de Helpdesk & Suporte de TI

> 🔗 **Acesse o sistema online:** [Clique aqui para testar a aplicação no Streamlit Cloud](https://SEU_LINK_DO_STREAMLIT_CLOUD.streamlit.app)

Aplicação web interativa desenvolvida em Python para gestão de incidentes de TI, automação de alertas urgentes e acompanhamento de métricas de suporte em tempo real.

---

## 🚀 Tecnologias Utilizadas
* **Linguagem:** Python
* **Interface Web & Deploy:** Streamlit & Streamlit Cloud
* **Banco de Dados:** SQLite
* **Análise de Dados:** Pandas
* **Visualização:** Plotly

---

## ⚙️ Funcionalidades Principais
1. **📌 Abertura de Chamados:** Formulário intuitivo para usuários registrarem incidentes categorizados por Hardware, Rede, Software ou Acessos.
2. **🛠️ Painel do Técnico:** Interface para acompanhamento, filtragem e atualização de status (*Aberto*, *Em Andamento*, *Concluído*) em tempo real.
3. **🚨 Automação de Alertas:** Regra de negócio que identifica incidentes críticos (Prioridade Alta), emitindo alertas visuais na tela e registrando auditoria em arquivo de log (`alertas_urgentes.log`).
4. **📊 Dashboard & Métricas:** Painel gerencial com indicadores (KPIs) de volume total, pendências e gráficos interativos de distribuição por categoria e prioridade.
5. **📥 Exportação de Dados:** Download da base de chamados em formato `.csv` para integração com Power BI ou Excel.

---

## 🔧 Como Executar Localmente

```bash
# Clone o repositório
git clone [https://github.com/GioOGabriel/Helpdesk-TI.git](https://github.com/GioOGabriel/Helpdesk-TI.git)

# Entre na pasta do projeto
cd Helpdesk-TI

# Instale as dependências
pip install -r requirements.txt

# Execute a aplicação
python -m streamlit run app.py
