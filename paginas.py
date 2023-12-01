import streamlit as st
import streamlit.components.v1 as components
import requests
import json
<<<<<<< HEAD
import datetime
from moviepy.editor import VideoFileClip
from io import BytesIO
=======
from datetime import datetime, timedelta, date
import extra_streamlit_components as stx


#Configuração dos Cookies utilizando a bilbioteca stx
def get_manager():
    return stx.CookieManager()
cookie_manager = get_manager()

all_cookies = cookie_manager.get_all()
try:
    #No logout por algum motivo após deslogar não podemos logar de novo. Ainda falta corrigir isso. Até la, deem refresh após deslogar para logar denovo
    if 'logout' in st.session_state:
        cookie_manager.delete('Authorization')

    elif 'Authorization' not in all_cookies:
        cookie_manager.set('Authorization', st.session_state['Authorization'], expires_at=datetime.utcnow() + timedelta(hours=3))
    else:
        st.session_state['Authorization'] = all_cookies['Authorization']
except:
    pass

>>>>>>> 73bef46a6a57881c7c305e9fb2c65f8af5e7191b

# Esta variavel controlara nosso fluxo de telas
# na Funcao main organizamos qual pagina precisa ser mostrada
if 'pagina' not in st.session_state or 'Authorization' not in all_cookies:
    st.session_state['pagina'] = 'login'
elif 'Authorization' in all_cookies and st.session_state['pagina'] == 'login':
    st.session_state['pagina'] = 'lista_partidas'

# Variavel para controle da interface de redefinir a senha
if 'resposta_troca_senha' not in st.session_state:
    st.session_state['resposta_troca_senha'] = False

st.markdown(
    """
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f8f9fa;
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        .logo {
            max-width: 80%;  /* Alterado para 80% */
            height: auto;
            display: block;
            margin: 20px auto;
        }
        h1 {
            color: #000000;  /* Alterado para preto (#000000) */
            text-align: center;
        }
        .login-container {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        .sidebar {
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
        }
        .sidebar-button {
            width: 100%;
            padding: 10px;
            margin-bottom: 10px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
        }
        .button-primary {
            background-color: #007BFF;
            color: #ffffff;
            font-weight: bold;
        }
        .button-secondary {
            background-color: #6c757d;
            color: #ffffff;
            font-weight: bold;
        }
        .button-logout {
            background-color: #dc3545;
            color: #ffffff;
            font-weight: bold;
        }
        .expander {
            background-color: #ffffff;
            border: 1px solid #dee2e6;
            border-radius: 10px;
            margin-bottom: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True
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
    elif st.session_state['pagina'] == "dashboard":
        dashboard()
<<<<<<< HEAD

=======
>>>>>>> 73bef46a6a57881c7c305e9fb2c65f8af5e7191b

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
                st.session_state['pagina'] = "dashboard" 
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

#Função auxiliar que realiza o logout
def realiza_logout():
    headers = {'Authorization': st.session_state['Authorization']}
    resposta = requests.get('http://127.0.0.1:5000/logout', headers=headers)
    st.session_state['logout'] = resposta.json()['logout']
    st.rerun()



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

def lista_partidas():
# Centralizar a imagem e o título
    st.sidebar.image('assets/deltagolalogo.png', width=150, use_column_width=False)

    st.markdown(
        """
        <div style='text-align: center;'>
            <h1>Partidas</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

#sidebar para filtros (ficticio)
    st.sidebar.markdown(
    """
    <style>
        .sidebar .sidebar-content {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Adiciona cabeçalho centralizado e botões centralizados na barra lateral
    st.sidebar.header("Filtros:")
    st.sidebar.button("Liga Nacional")
    st.sidebar.button("Copa Nacional")
    st.sidebar.button("Copa Internacional")
    st.sidebar.button("Pré Temporada")
    st.sidebar.button("Outros")

    start_date = st.sidebar.date_input("Selecione a data de início", None)
    end_date = st.sidebar.date_input("Selecione a data de término", None)

    st.sidebar.markdown("---")
    if st.sidebar.button("Logout"):
        realiza_logout()
    if start_date and end_date:
        if start_date <= end_date:
            st.success(f'Selecionado intervalo de {start_date} a {end_date}')
            games = [
                {"Jogo": "Palmeiras X São Paulo", "Data": date.today() + timedelta(days=1),
                 "Detalhes": "Detalhes do jogo Palmeiras X São Paulo"},
                {"Jogo": "Palmeiras x Corinthians", "Data": date.today() + timedelta(days=3),
                 "Detalhes": "Detalhes do jogo Palmeiras x Corinthians"},
                {"Jogo": "Santos X Palmeiras", "Data": date.today() + timedelta(days=5),
                 "Detalhes": "Detalhes do jogo Santos X Palmeiras"},
                {"Jogo": "Coritiba X Palmeiras", "Data": date.today() + timedelta(days=7),
                 "Detalhes": "Detalhes do jogo Coritiba X Palmeiras"},
                {"Jogo": "Palmeiras X Goias", "Data": date.today() + timedelta(days=9),
                 "Detalhes": "Detalhes do jogo Palmeiras X Goias"}
            ]

            filtered_games = [game for game in games if start_date <= game["Data"] <= end_date]
            if filtered_games:
                st.write("Jogos dentro do intervalo selecionado:")
                for game in filtered_games:
                    expander = st.expander(game["Jogo"])
                    with expander:
                        st.write(game["Detalhes"])
        else:
            st.error("Erro: A data de início deve ser anterior à data de término.")
    else:
        games = [
            {"Jogo": "Palmeiras X São Paulo", "Data": date.today() + timedelta(days=1),
             "Detalhes": "Detalhes do jogo Palmeiras X São Paulo"},
            {"Jogo": "Palmeiras x Corinthians", "Data": date.today() + timedelta(days=3),
             "Detalhes": "Detalhes do jogo Palmeiras x Corinthians"},
            {"Jogo": "Santos X Palmeiras", "Data": date.today() + timedelta(days=5),
             "Detalhes": "Detalhes do jogo Santos X Palmeiras"},
            {"Jogo": "Coritiba X Palmeiras", "Data": date.today() + timedelta(days=7),
             "Detalhes": "Detalhes do jogo Coritiba X Palmeiras"},
            {"Jogo": "Palmeiras X Goias", "Data": date.today() + timedelta(days=9),
             "Detalhes": "Detalhes do jogo Palmeiras X Goias"}
        ]
        
        for game in games:
            expander = st.expander(game["Jogo"])
            with expander:
                st.write(game["Detalhes"])

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
                    st.image("assets/palmeiras.png", width=120, use_column_width=False, caption=game_info['time']['1']['nome'])
                    st.write("Time da Casa")

                # Adicione a caixa com a logo e o nome do time visitante
                with col3:
                    st.image("assets/RedBullBragantino.png", width=120, use_column_width=False, caption=game_info['time']['5']['nome'])
                    st.write("Time Visitante")

                # Adicione o botão de estatísticas
                if st.button("Estatísticas"):
                    st.session_state['pagina'] = "dashboard"
                    st.rerun()

def dashboard():
    st.title('Clipe de Vídeo Incorporado')

    
        # Exibir o código de incorporação
        st.markdown(embed_code, unsafe_allow_html=True)


def dashboard():
# Centralizar a imagem e o título
    st.sidebar.image('assets/deltagolalogo.png', width=150, use_column_width=False)

    st.markdown(
        """
        <div style='text-align: center;'>
            <h1>Dashboard</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

#sidebar para filtros (ficticio)
    st.sidebar.header("Análises:")
    if st.sidebar.button("Cruzamentos"):
        st.header('Cruzamento')

    if st.sidebar.button("Quebra de Linhas"):
        st.header('Quebra')

    st.sidebar.markdown("---")
    if st.sidebar.button("Voltar"):
        st.session_state['pagina'] = "lista_partidas"
        st.rerun()
    if st.sidebar.button("Logout"):
        realiza_logout()
    
    
if __name__ == "__main__":
    main()
