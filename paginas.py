import streamlit as st
import requests



def realizar_login(username, senha):
    dados = {'username': username, 'senha': senha}
    resposta = requests.post('http://127.0.0.1:5000/verificar_login', json=dados)

    if resposta.status_code == 200:
        st.success(resposta.json()['mensagem'])
    else:
        st.warning(resposta.json()['erro'])

def page_login():
    st.title("Página de Login")

    username = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    
    if st.button("Login"):
        realizar_login(username, senha)

