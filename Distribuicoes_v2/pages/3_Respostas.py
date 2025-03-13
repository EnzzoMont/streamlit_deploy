import streamlit as st
import time

# Título da aplicação
st.title("Talvez você esteja esperando a tão aguardada resposta, quem será o vencedor?")

# Criar um espaço vazio para o texto dinâmico
text_placeholder = st.empty()

# Texto que será exibido com o efeito de digitação
hidden_text = "Em nossa análise percebemos quem teve maior média de vitória, gols, menos perdeu e sofreu gols. Percebemos que em um confronto quem teria mais possibilidade de fazer gol, se foi eficaz de verdade ser mais duro nos jogos e sofrer cartão amarelo. E eu até falaria meu palpite, mas não sei, vai se dá zebra, me fale você o que acha disso tudo...."

# Criar o botão "Show More"
if st.button("Saiba aqui"):
    displayed_text = ""  # Inicia com texto vazio
    for char in hidden_text:
        displayed_text += char  # Adiciona um caractere por vez
        text_placeholder.text(displayed_text + "|")  # Adiciona um cursor piscando
        time.sleep(0.04)  # Atraso para simular a digitação
    text_placeholder.text(displayed_text) 