import streamlit as st
import pandas as pd
import time

@st.cache_data
def load_data():
    df = pd.read_excel("Mans_clubs.xlsx")
    return df

df = load_data()

times = ['Man_City', 'Man_United']
times_formatados = ['Manchester City', 'Manchester United']
df_filtrado = df[df['time_de_casa'].isin(times) | df['time_visitante'].isin(times)].copy()

medias_gols = {}
for time in times:
    jogos_casa = df_filtrado[df_filtrado['time_de_casa'] == time]
    media_gols_marcados = jogos_casa['gols_time_de_casa'].mean()
    media_gols_sofridos = jogos_casa['gols_time_visitante'].mean()
    medias_gols[time] = {
        'Média de Gols marcados em Casa': media_gols_marcados,
        'Média de Gols sofridos em Casa': media_gols_sofridos
    }

def resultado_partida(row):
    if row['gols_time_de_casa'] > row['gols_time_visitante']:
        return row['time_de_casa'], row['time_visitante']
    elif row['gols_time_de_casa'] < row['gols_time_visitante']:
        return row['time_visitante'], row['time_de_casa']
    else:
        return None, None

df_filtrado[['Vencedor', 'Perdedor']] = df_filtrado.apply(resultado_partida, axis=1, result_type='expand')

vitorias = {}
derrotas = {}
for time in times:
    vitorias[time] = df_filtrado[df_filtrado['Vencedor'] == time].shape[0]
    derrotas[time] = df_filtrado[df_filtrado['Perdedor'] == time].shape[0]

time_mais_vitorias = max(vitorias, key=vitorias.get)
time_mais_derrotas = max(derrotas, key=derrotas.get)

cartoes_amarelos = {}
for time in times:
    cartoes_casa = df_filtrado[df_filtrado['time_de_casa'] == time]['cartoes_amarelos_time_de_casa'].sum()
    cartoes_fora = df_filtrado[df_filtrado['time_visitante'] == time]['cartoes_amarelos_time_visitante'].sum()
    total_jogos = df_filtrado[(df_filtrado['time_de_casa'] == time) | (df_filtrado['time_visitante'] == time)].shape[0]
    media_cartoes = (cartoes_casa + cartoes_fora) / total_jogos if total_jogos > 0 else 0
    cartoes_amarelos[time] = media_cartoes

st.title("Caso os Rivais se enfrentassem, quem ganharia? E como eu sei disso?")

st.image('briga_boa.jpg', caption="Machester's se enfrentando hipoteticamente", width=450)

import time

# Inicializa a variável de estado para controlar o texto exibido
if "displayed_text" not in st.session_state:
    st.session_state.displayed_text = ""

text_placeholder = st.empty()

hidden_text = "Meu objetivo aqui é analisar os jogos de dois rivais que se enfrentam há décadas, então em cima dessa base de dados, filtrei para ser apenas jogos em casa, são todos os jogos em casa do Manchester City e do Manchester United. Usarei 3 variáveis, vitórias, gols e cartões amarelos. Gols, vitória e cartões amarelos são variáveis discretas. Em um confronto hipotético, quem venceria dentro de casa e fora de casa? Que time ganhou e marcou mais gols? Qual time é mais agressivo? Foi eficaz? Utilizarei a Distribuição de Poisson para prever a quantidade de gols esperado em uma partida a partir dos outros jogos e o Binominal para estimar a probabilidade de vitória para algum dos times."

if st.button("Antes de descer, clique aqui!"):
    # Reinicia o texto exibido ao clicar no botão
    st.session_state.displayed_text = ""
    for char in hidden_text:
        st.session_state.displayed_text += char
        text_placeholder.text(st.session_state.displayed_text + "|")  # Adiciona o cursor
        time.sleep(0.035)  # Atraso de 0.05 segundos
    text_placeholder.text(st.session_state.displayed_text)  # Remove o cursor no final
else:
    # Exibe o texto atual (se houver)
    text_placeholder.text(st.session_state.displayed_text)

st.header("Vamos levantar algumas informações para embasar nosso palpite...")

st.subheader("As médias de gols de cada time são essas, o que acha?")

dados_tabela_gols = []
for i, time in enumerate(times):
    dados_tabela_gols.append({'Time': times_formatados[i], **medias_gols[time]})
df_tabela_gols = pd.DataFrame(dados_tabela_gols)
st.table(df_tabela_gols.set_index('Time'))

st.write ("Assim, só entre nós mas só vendo isso parece uma competição meia injusta, não acha?") 

st.subheader("Agora, demonstrarei apenas as vitórias e derrotas de cada time dentro de casa. Foi um ano em tanto ein!?")

dados_tabela_resultados = []
for i, time in enumerate(times):
    dados_tabela_resultados.append({'Time': times_formatados[i], 'Vitórias': vitorias[time], 'Derrotas': derrotas[time]})
df_tabela_resultados = pd.DataFrame(dados_tabela_resultados)
st.table(df_tabela_resultados.set_index('Time'))

st.write(f"Mesmo repetindo o óbvio, o time com mais vitória foi: **{times_formatados[times.index(time_mais_vitorias)]}**")
st.write(f"E o com mais derrota infelizmente foi: **{times_formatados[times.index(time_mais_derrotas)]}**")

st.subheader("Olhando com outros olhos, será que adotar uma postura mais agressiva durante os jogos é eficaz?")

dados_tabela_cartoes = []
for i, time in enumerate(times):
    dados_tabela_cartoes.append({'Time': times_formatados[i], 'Média de Cartões Amarelos': cartoes_amarelos[time]})
df_tabela_cartoes = pd.DataFrame(dados_tabela_cartoes)
st.table(df_tabela_cartoes.set_index('Time'))

st.write("Aparentemente não é tão eficaz marcar faltas mais duras durante os jogos, ou é?")

