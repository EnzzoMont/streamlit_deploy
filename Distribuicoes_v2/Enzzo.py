import time
import streamlit as st
import pandas as pd
import numpy as np
from streamlit_extras.app_logo import add_logo 
from PIL import Image, ImageOps
from PIL import Image

st.set_page_config(page_title="Dashboard de Distribuições Probabilísticas", layout="wide")
st.sidebar.markdown("Desenvolvido por um futuro Dev que será referencia na área graças ao Tiago Marum")
st.sidebar.markdown("(https://www.instagram.com/enzzomont/)")


st.title("Enzzo Monteiro Barros Silva")

st.subheader("Objetivo")

st.write("Estagiário de Dados")

st.subheader("Quem sou eu?")
st.write("Prazer, sou Enzzo! Atualmente, estou no quarto semestre de Engenharia de Software na FIAP e tenho um grande interesse na área de dados. Desde pequeno, sempre fui fascinado por tomar decisões baseadas em números, pois acredito que tudo faz mais sentido quando há comprovações numéricas. Essa paixão me levou a escolher o caminho da Engenharia de Dados.")

st.subheader("Formação e experiência")
st.write("Uma experiência marcante na minha trajetória foi a participação no NEXT, onde tive a oportunidade de trabalhar em equipe e explorar ideias que antes eu nem imaginava serem possíveis. Durante esse projeto, aprimorei habilidades em diversas tecnologias, desde design, utilizando Figma, até visualização de dados com Power BI. Além disso, trabalhei com JavaScript e Python, utilizando React para desenvolver uma solução inovadora: um sistema de avatares para conteúdos educacionais voltado para crianças do ICR (Instituto da Criança e do Adolescente do Hospital das Clínicas). Essa experiência não só expandiu meus conhecimentos técnicos, como também fortaleceu minha maturidade educacional e profissional, reafirmando minha vontade de seguir na área de dados.")

st.subheader("Aqui está um resumo das minhas habilidades!")

col1, col2 = st.columns(2)

with col1:

    st.subheader("Soft Skills")
    st.markdown(
        """
        <ul style="font-size:20px; font-weight:bold;">
            <li>Comunicação eficaz</li>
            <li>Trabalho em equipe</li>
            <li>Pensamento crítico</li>
            <li>Resolução de problemas</li>
            <li>Adaptabilidade</li>
            <li>Liderança</li>
        </ul>
        """,
        unsafe_allow_html=True
    )


with col2:
    hard_skills = {
    "Python": "assets/python.gif",
    "JavaScript": "assets/js.gif",
    "SQL": "assets/sql.gif",
    "HTML/CSS": "assets/code.gif",
    "Machine Learning": "assets/machine.gif",
    "Git": "assets/git.gif",
    }

    st.subheader("Hard Skills")

    for skill, gif_path in hard_skills.items():
        col1, col2 = st.columns([0.15, 0.85])
        with col1:
            st.image(gif_path, width=50)  # Aumentei o tamanho para 50px
        with col2:
            st.markdown(f'<span style="font-size:20px; font-weight:bold;">{skill}</span>', unsafe_allow_html=True)
            

