import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io
import base64


st.set_page_config(page_title="JobTrends Dashboard", layout="wide", page_icon="📊")


st.markdown("""
    <style>
    /* Fundo e fonte geral */
    .stApp {
        background-color: #f5f7fa;
        font-family: 'Arial', sans-serif;
    }
    /* Título principal */
    h1 {
        color: #1e3a8a;
        font-size: 2.5em;
        text-align: center;
        margin-bottom: 0.5em;
    }
    /* Subtítulos */
    h3 {
        color: #3b82f6;
        font-size: 1.5em;
        margin-top: 1em;
    }
    /* Barra lateral */
    .css-1d391kg {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }
    /* Estilo dos seletores */
    .stSelectbox label {
        color: #1e3a8a;
        font-weight: bold;
    }
    /* Botões e texto */
    .stButton>button {
        background-color: #3b82f6;
        color: white;
        border-radius: 5px;
    }
    /* Container dos gráficos */
    .stPlotlyChart {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    </style>
""", unsafe_allow_html=True)


def get_logo():

    try:
        with open("JobTrends.png", "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode()
            return f"data:image/png;base64,{encoded}"
    except FileNotFoundError:
        st.error("Erro: Arquivo 'JobsTrends.png' não encontrado no diretório. Usando placeholder.")
        return "https://via.placeholder.com/150x50.png?text=JobTrends+Logo"  # Fallback


st.image(get_logo(), width=200)


st.title("📊 JobTrends: Análise de Vagas de TI no Brasil")


@st.cache_data
def load_data():
    df = pd.read_csv('vagas_ti_limpo_realistas.csv')
    df['Tecnologias'] = df['Tecnologias'].apply(eval)
    df['Benefícios'] = df['Benefícios'].apply(eval)
    df['Salário'] = pd.to_numeric(df['Salário'], errors='coerce')
    return df

df = load_data()


st.sidebar.markdown("### 🔍 Filtros")
cidade = st.sidebar.selectbox("Cidade", ['Todas'] + sorted(df['Localização'].unique()))
nivel = st.sidebar.selectbox("Nível", ['Todos'] + ['Júnior', 'Pleno', 'Sênior'])
cargo = st.sidebar.selectbox("Cargo", ['Todos'] + sorted(df['Título'].unique()))


df_filtrado = df.copy()
if cidade != 'Todas':
    df_filtrado = df_filtrado[df_filtrado['Localização'] == cidade]
if nivel != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['Nível'] == nivel]
if cargo != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['Título'] == cargo]


st.markdown(f"**Número de vagas filtradas**: {len(df_filtrado)}", unsafe_allow_html=True)


col1, col2 = st.columns(2)


with col1:
    st.subheader("Top 10 Tecnologias Mais Exigidas")
    todas_tecnologias = [tec for sublist in df_filtrado['Tecnologias'] for tec in sublist]
    contagem_tecnologias = pd.Series(todas_tecnologias).value_counts().head(10)
    if not contagem_tecnologias.empty:
        fig1 = px.bar(x=contagem_tecnologias.values, y=contagem_tecnologias.index, orientation='h',
                      labels={'x': 'Número de Vagas', 'y': 'Tecnologia'}, title='',
                      color_discrete_sequence=['#3b82f6'])
        fig1.update_layout(showlegend=False, height=400, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.markdown("⚠️ Nenhuma tecnologia encontrada para os filtros selecionados.")


with col2:
    st.subheader("Distribuição por Localização")
    contagem_localizacao = df_filtrado['Localização'].value_counts().head(10)
    if not contagem_localizacao.empty:
        fig2 = px.bar(x=contagem_localizacao.index, y=contagem_localizacao.values,
                      labels={'x': 'Cidade/Estado', 'y': 'Número de Vagas'}, title='',
                      color_discrete_sequence=['#1e3a8a'])
        fig2.update_layout(xaxis_tickangle=45, height=400, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.markdown("⚠️ Nenhuma vaga encontrada para os filtros selecionados.")


st.subheader("Nuvem de Palavras - Tecnologias")
if todas_tecnologias:
    texto_tecnologias = ' '.join(todas_tecnologias)
    wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='Blues').generate(texto_tecnologias)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    st.image(buf.getvalue())
else:
    st.markdown("⚠️ Nenhuma tecnologia para gerar a nuvem de palavras.")


st.subheader("Distribuição Salarial")
salarios = df_filtrado[df_filtrado['Salário'].notna()]['Salário']
if not salarios.empty:
    fig4 = px.histogram(salarios, nbins=20, labels={'value': 'Salário (R$)', 'count': 'Frequência'}, title='',
                        color_discrete_sequence=['#60a5fa'])
    fig4.update_layout(showlegend=False, height=400, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig4, use_container_width=True)
else:
    st.markdown("� ratear salário informado para os filtros selecionados.")


st.subheader("Salário Médio por Nível")
salarios_por_nivel = df_filtrado[df_filtrado['Salário'].notna()].groupby('Nível')['Salário'].mean().reindex(['Júnior', 'Pleno', 'Sênior'])
if not salarios_por_nivel.dropna().empty:
    fig5 = px.bar(x=salarios_por_nivel.index, y=salarios_por_nivel.values,
                  labels={'x': 'Nível', 'y': 'Salário Médio (R$)'}, title='',
                  color_discrete_sequence=['#1e3a8a'])
    fig5.update_layout(height=400, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig5, use_container_width=True)
else:
    st.markdown("⚠️ Nenhum salário informado para os níveis selecionados.")


st.subheader("Top 10 Benefícios Mais Oferecidos")
todos_beneficios = [ben for sublist in df_filtrado['Benefícios'] for ben in sublist]
contagem_beneficios = pd.Series(todos_beneficios).value_counts().head(10)
if not contagem_beneficios.empty:
    fig6 = px.bar(x=contagem_beneficios.values, y=contagem_beneficios.index, orientation='h',
                  labels={'x': 'Número de Vagas', 'y': 'Benefício'}, title='',
                  color_discrete_sequence=['#3b82f6'])
    fig6.update_layout(showlegend=False, height=400, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig6, use_container_width=True)
else:
    st.markdown("⚠️ Nenhum benefício encontrado para os filtros selecionados.")