import pandas as pd
import numpy as np
import scipy.stats as stats
import streamlit as st
import plotly.graph_objects as go
import time

@st.cache_data
def load_data():
    df = pd.read_excel("Mans_clubs.xlsx")
    return df

df = load_data()

# Definir o conteúdo oculto
  # Pequeno atraso para simular digitação


# Garantir que os times sejam strings e remover valores nulos ou vazios
df["time_de_casa"] = df["time_de_casa"].astype(str)
df["time_visitante"] = df["time_visitante"].astype(str)

# Remover valores nulos ou strings vazias
df = df[df["time_de_casa"].str.strip() != ""]
df = df[df["time_visitante"].str.strip() != ""]

# Converter colunas numéricas
df["gols_time_de_casa"] = pd.to_numeric(df["gols_time_de_casa"], errors='coerce')
df["gols_time_visitante"] = pd.to_numeric(df["gols_time_visitante"], errors='coerce')
df["cartoes_amarelos_time_de_casa"] = pd.to_numeric(df["cartoes_amarelos_time_de_casa"], errors='coerce')
df["cartoes_amarelos_time_visitante"] = pd.to_numeric(df["cartoes_amarelos_time_visitante"], errors='coerce')

st.title("Probabilidade de gols na partida e Previsão de Cartões Amarelos")

dist = st.selectbox("Escolha a distribuição:", ["Poisson - Gols", "Binomial - Cartões Amarelo"])

if dist == "Poisson - Gols":
    st.subheader("Distribuição de Poisson para Quantidade de Gols")
    
    # Filtrar apenas os times válidos (sem valores nulos ou strings vazias)
    times_validos = df["time_de_casa"].unique()
    times_validos = [time for time in times_validos if str(time).strip() != ""]  # Remover strings vazias
    
    time = st.selectbox("Selecione o time:", times_validos)
    df_time = df[(df["time_de_casa"] == time) | (df["time_visitante"] == time)]
    
    gols_marcados = df_time[df_time["time_de_casa"] == time]["gols_time_de_casa"].sum() + \
                    df_time[df_time["time_visitante"] == time]["gols_time_visitante"].sum()
    media_gols = gols_marcados / df_time.shape[0]
    
    col1, col2 = st.columns([0.3, 0.7])
    x_min = col1.number_input("Número mínimo de gols", value=0)
    x_max = col1.number_input("Número máximo de gols desejado", value=int(2 * media_gols))
    
    x = np.arange(x_min, x_max)
    y = stats.poisson.pmf(x, media_gols)
    y_cdf = stats.poisson.cdf(x, media_gols)
    
    df_poisson = pd.DataFrame({"X": x, "P(X)": y, "P(X ≤ k) (Acumulado)": np.cumsum(y), "P(X > k) (Cauda Direita)": 1 - np.cumsum(y)}).set_index("X")
    
    col2.write("Tabela de probabilidades:")
    col2.write(df_poisson)
    
    st.subheader(f"Estimativa de λ (Taxa média de Gols por partida): {media_gols:.2f}")
    prob_acum = st.toggle("Probabilidade Acumulada")
    if prob_acum:
        st.write("Probabilidades 'somadas' desde a origem!")
        y_selec = y_cdf
        fig = go.Figure(data=[go.Line(x=x, y=y_selec)])
        fig.update_layout(title="Distribuição de Poisson Acumulada", xaxis_title="Número de Gols", yaxis_title="Probabilidade Acumulada")
        st.plotly_chart(fig)
    else:
        y_selec = y
        fig = go.Figure(data=[go.Bar(x=x, y=y_selec)])
        fig.update_layout(title="Distribuição de Poisson", xaxis_title="Número de Gols", yaxis_title="Probabilidade")
        st.plotly_chart(fig)

elif dist == "Binomial - Cartões Amarelo":
    st.subheader("Distribuição Binomial para Probabilidade de Receber Cartões Amarelos")
    
    # Filtrar apenas os times válidos (sem valores nulos ou strings vazias)
    times_validos = df["time_de_casa"].unique()
    times_validos = [time for time in times_validos if str(time).strip() != ""]  # Remover strings vazias
    
    time = st.selectbox("Selecione o time:", times_validos)
    df_time = df[(df["time_de_casa"] == time) | (df["time_visitante"] == time)]
    
    cartoes = df_time[df_time["time_de_casa"] == time]["cartoes_amarelos_time_de_casa"].sum() + \
    df_time[df_time["time_visitante"] == time]["cartoes_amarelos_time_visitante"].sum()
    total_jogos = df_time.shape[0]
    p_est = cartoes / (total_jogos * 2) 
    
    k = st.slider("Número de cartões amarelos esperados:", min_value=0, max_value=10, value=3)
    valores = np.arange(0, k + 1)
    probabilidades = stats.binom.pmf(valores, k, p_est)
    
    fig = go.Figure(data=[go.Bar(x=valores, y=probabilidades)])
    fig.update_layout(title="Distribuição Binomial", xaxis_title="Número de Cartões Amarelos", yaxis_title="Probabilidade")
    st.plotly_chart(fig)


    