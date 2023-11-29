import streamlit as st
import requests
import json
import datetime

# Esta variavel controlara nosso fluxo de telas
# na Funcao main organizamos qual pagina precisa ser mostrada
if 'pagina' not in st.session_state:
    st.session_state['pagina'] = 'login'

# Variavel para controle da interface de redefinir a senha
if 'resposta_troca_senha' not in st.session_state:
    st.session_state['resposta_troca_senha'] = False


st.markdown(
    """
    <style>
    .st-emotion-cache-1pxazr7 {
        display:none
    }
    .st-emotion-cache-6awftf:active, .st-emotion-cache-6awftf:focus-visible, .st-emotion-cache-6awftf:hover {
    display:none
    }
    </style>"""
    , unsafe_allow_html=True
)

# Main
# Aqui contrlaremos as mudancas de paginas caso nescessario
def main():
    if st.session_state['pagina'] == "login":
        login()
    elif st.session_state['pagina'] == "troca_senha":
        troca_senha()
    elif st.session_state['pagina'] == "lista_partidas":
       lista_partidas()

# Pagina de Login
def login():
    dados_existentes = False

    col1, col2, col3 = st.columns([2,1,2])

    with col1:
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.image('assets/deltagolalogo.png')
        st.write('')
        st.markdown(
"""
<h3 style="
    line-height: 40px;
    color: #333333;
    font-family: 'Helvetica Neue', sans-serif;
    ">
    Artificial Intelligence to monitor players <span style="color: #FF69B4;">every</span> instant of <span style="color: #0000FF;">every</span> match.
</h3>
""",
unsafe_allow_html=True
)
    with col2:
        st.write('')

            
    with col3:
        st.markdown('<h1 style="text-align: center">Login</h1>', unsafe_allow_html=True)
        st.write('')
        username = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")


        if st.button("Login"):
            dados_existentes = True
            dados = realizar_login(username, senha)
            if dados['erro'] == False:
                st.session_state['pagina'] = "lista_partidas" 
                st.rerun()

        if st.button("Esqueci a Senha"):
            st.session_state['pagina'] = "troca_senha"
            st.session_state['resposta_troca_senha'] = False
            
            st.rerun()

    if dados_existentes:
        if dados['erro']:
            st.warning(dados['mensagem'])
        else:
            st.success(dados['mensagem'])

# Funcao Auxiliar para Login

def realizar_login(username, senha):
    dados = {'team': username, 'password': senha}
    dados_json = json.dumps(dados)

    headers = {'Content-Type': 'application/json'}
    resposta = requests.post('http://127.0.0.1:5000/login/verificar_login', data=dados_json, headers=headers)
    resposta_json = resposta.json()
    if 'token' in resposta_json:
        st.session_state['Authorization'] = resposta_json['token']

    return resposta_json



# Pagina Troca de Senha

def troca_senha():
    col1, col2, col3 = st.columns([2,1,2])

    with col1:
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.image('assets/deltagolalogo.png')
        st.write('')
        st.markdown(
    """
    <h3 style="
        line-height: 40px;
        color: #333333;
        font-family: 'Helvetica Neue', sans-serif;
        ">
        Artificial Intelligence to monitor players <span style="color: #FF69B4;">every</span> instant of <span style="color: #0000FF;">every</span> match.
    </h3>
    """,
    unsafe_allow_html=True
)

    with col2:
        st.write("")

    with col3:
        st.markdown('<h1 style="text-align: center">Redefinir Senha</h1>', unsafe_allow_html=True)
        st.write('')
        senha_trocada = True
        

        username = st.text_input("Digite o seu username")

        if st.button("Voltar para Login"):
            st.session_state['pagina'] = 'login'
            st.rerun()   

        
        if st.button("Validar"):
            dados = {'team': username}
            headers = {'Content-Type': 'application/json'}

            resposta_usuario = requests.post('http://127.0.0.1:5000/login/verificar_time', data=json.dumps(dados), headers=headers)

            resposta_usuario_json = resposta_usuario.json()

            if resposta_usuario_json['existe']:
                st.session_state['resposta_troca_senha'] = True
                st.success(resposta_usuario_json['mensagem'])
            else:
                st.session_state['resposta_troca_senha'] = False
                st.warning(resposta_usuario_json['mensagem'])
                
        if st.session_state['resposta_troca_senha']:
            nova_senha = st.text_input("Digite sua nova senha", type="password")
            if st.button("Atualizar Senha!"):

                # Criar um dicionário com o nome de usuário e nova senha
                dados = {'team': username, 'nova_senha': nova_senha}
                
                # Configurar o cabeçalho para indicar que estamos enviando JSON
                headers = {'Content-Type': 'application/json'}

                # Enviar a solicitação POST com os dados no corpo
                resposta_senha = requests.post('http://127.0.0.1:5000/login/alterar_senha', data=json.dumps(dados), headers=headers)
                # Interpretar a resposta como JSON
                resposta_senha_json = resposta_senha.json()

             
                st.success(resposta_senha_json['mensagem'])

import streamlit as st
import requests

def lista_partidas():
  # Centralizar a imagem e o título
    st.image('assets/deltagolalogo.png', width=250, use_column_width=False)

    st.markdown(
        """
        <div style='text-align: center;'>
            <h1>Partidas</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    headers = {'Authorization': st.session_state['Authorization']}
    resposta = requests.get('http://127.0.0.1:5000/historico', headers=headers)
    games = resposta.json()
    for index, game_info in enumerate(games['jogos']):
        # Adicione a caixa de fundo para o jogo
        jogo_box = st.expander(f"{game_info['time']['1']['nome']} vs {game_info['time']['5']['nome']}")
        
        # Adicione a caixa com a logo e o nome do time da casa
        with jogo_box:
            col1, col2, col3 = st.columns([1, 3, 1])

            # Adicione a caixa com a logo e o nome do time da casa
            with col1:
                st.image("assets/palmeiras.png", width=100, use_column_width=False, caption=game_info['time']['1']['nome'])
                st.write("Time da Casa")

            # Adicione a caixa com a logo e o nome do time visitante
            with col3:
                st.image("assets/RedBullBragantino.png", width=100, use_column_width=False, caption=game_info['time']['5']['nome'])
                st.write("Time Visitante")

            # Adicione o botão de estatísticas
            if st.button(f"Estatísticas"):
                # Lógica para redirecionar para a tela de estatísticas do jogo
                st.write(f"Redirecionando para estatísticas do jogo {game_info['_id']}")
    
    
if __name__ == "__main__":
    main()
