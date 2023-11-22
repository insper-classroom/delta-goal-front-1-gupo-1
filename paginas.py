import streamlit as st
import requests

# Variaveis "Globais"

# Esta variavel controlara nosso fluxo de telas
# na Funcao main organizamos qual pagina precisa ser mostrada
if 'pagina' not in st.session_state:
    st.session_state['pagina'] = 'login'

# Variavel para controle da interface de redefinir a senha
if 'resposta_troca_senha' not in st.session_state:
    st.session_state['resposta_troca_senha'] = False



# Pagina de Login

def login():
    entra = False
    try:
        st.title("Página de Login")

        username = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Login"):
                entra = True
                mensagem, erro = realizar_login(username, senha)
                
        with col2:
            if st.button("Esqueci a Senha"):
                st.session_state['pagina'] = "troca_senha"
                st.rerun()
        if entra:
            if erro:
                st.warning(mensagem)
            else:

                st.success(mensagem)
    except:
        st.warning("Preencha os campos corretamente!")

# Funcao Auxiliar para Login

def realizar_login(username, senha):
    resposta = requests.post(f'http://127.0.0.1:5000/verificar_login/{username}/{senha}')
    resposta = resposta.json()
    return resposta[1]['mensagem'] , resposta[0]['erro']



# Pagina Troca de Senha

def troca_senha():
    st.title("Troca de Senha")

    username = st.text_input("Digite o seu username")

    if st.button("Validar"):
        resposta_usuario = requests.get(f'http://127.0.0.1:5000/verificar_usuario/{username}')
        resposta_usuario = resposta_usuario.json()

        if resposta_usuario['existe']:
            st.session_state['resposta_troca_senha']= True
            st.success(resposta_usuario['mensagem'])
        else:
            st.session_state['resposta_troca_senha'] = False
            st.warning(resposta_usuario['mensagem'])
    if st.session_state['resposta_troca_senha']:
        nova_senha = st.text_input("Digite sua nova senha", type="password")
        if st.button("Atualizar Senha!"):
            resposta_senha = requests.post(f'http://127.0.0.1:5000/alterar_senha/{username}/{nova_senha}')
            resposta_senha = resposta_senha.json()
            st.success(resposta_senha['mensagem'])
        if st.button("Voltar para Login"):
            st.session_state['pagina'] = 'login'
            st.rerun()


# Main
# Aqui contrlaremos as mudancas de paginas caso nescessario
def main():
    if st.session_state['pagina'] == "login":
        login()
    elif st.session_state['pagina'] == "troca_senha":
        troca_senha()
if __name__ == "__main__":
    main()