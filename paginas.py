import streamlit as st
import streamlit.components.v1 as components
import requests
import json
from datetime import datetime, timedelta, date
import extra_streamlit_components as stx
from functions import *
import pandas as pd
import altair as alt
st.set_page_config(layout="wide")
#Configuração dos Cookies utilizando a bilbioteca stx
def get_manager():
    return stx.CookieManager()
cookie_manager = get_manager()

all_cookies = cookie_manager.get_all()
try:
    #No logout por algum motivo após deslogar não podemos logar de novo. Ainda falta corrigir isso. Até la, deem refresh após deslogar para logar denovo
    if 'sub_page' not in st.session_state:
        st.session_state['sub_page'] = 'cruzamentos'
    if 'logout' in st.session_state:
        cookie_manager.delete('Authorization')

    elif 'Authorization' not in all_cookies:
        cookie_manager.set('Authorization', st.session_state['Authorization'], expires_at=datetime.utcnow() + timedelta(hours=3))
    else:
        st.session_state['Authorization'] = all_cookies['Authorization']
except:
    pass


# Esta variavel controlara nosso fluxo de telas
# na Funcao main organizamos qual pagina precisa ser mostrada
if 'pagina' not in st.session_state or ('Authorization' not in all_cookies and st.session_state['pagina'] != 'troca_senha'):
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
        dashboard(st.session_state['match_id'])

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
    resposta = requests.post('https://sprint-c82dfd49e88d.herokuapp.com/login/verificar_login', data=dados_json, headers=headers)
    resposta_json = resposta.json()
    if 'token' in resposta_json:
        st.session_state['Authorization'] = resposta_json['token']

    return resposta_json

#Função auxiliar que realiza o logout
def realiza_logout():
    headers = {'Authorization': st.session_state['Authorization']}
    resposta = requests.get('https://sprint-c82dfd49e88d.herokuapp.com/logout', headers=headers)
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

            resposta_usuario = requests.post('https://sprint-c82dfd49e88d.herokuapp.com/login/verificar_time', data=json.dumps(dados), headers=headers)

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
                resposta_senha = requests.post('https://sprint-c82dfd49e88d.herokuapp.com/login/alterar_senha', data=json.dumps(dados), headers=headers)
                # Interpretar a resposta como JSON
                resposta_senha_json = resposta_senha.json()

             
                st.success(resposta_senha_json['mensagem'])

def lista_partidas():
    st.sidebar.image('assets/deltagolalogo.png', width=150, use_column_width=False)
    
    st.sidebar.write('-------')

    if st.sidebar.button("Logout"):
        realiza_logout()

    expander_filtros = st.expander("Filtros")
    with expander_filtros:
        start_date = st.date_input("Selecione a data de início", None)
        end_date = st.date_input("Selecione a data de término", None)
        ligas = st.multiselect("Selecione as Ligas", ["Liga Nacional", "Copa Nacional", "Copa Internacional", "Estadual", "Outros"])

    st.markdown(
        """
        <div style='text-align: center;'>
            <h1>Partidas</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

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

            filtered_games = [game for game in games if start_date <= game["Data"] <= end_date and game["Liga"] in ligas]
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
        resposta = requests.get('https://sprint-c82dfd49e88d.herokuapp.com/historico', headers=headers)
        games = resposta.json()
        
    for index, game_info in enumerate(games['jogos']):
            jogo_box = st.expander(f"{game_info['time']['1']['nome']} vs {game_info['time']['5']['nome']}")
            
            with jogo_box:
                col1, col2, col3 = st.columns([1, 3, 1])

                with col1:
                    st.image("assets/palmeiras.png", width=120, use_column_width=False, caption=game_info['time']['1']['nome'])
                    st.write("Time da Casa")

                with col3:
                    st.image("assets/RedBullBragantino.png", width=120, use_column_width=False, caption=game_info['time']['5']['nome'])
                    st.write("Time Visitante")

                if st.button("Estatísticas"):
                    st.session_state['pagina'] = "dashboard"
                    st.session_state['match_id'] = game_info['_id']

                    st.rerun()

def dashboard(match_id):
    
    info = ['', '', False]

    headers = {'Authorization': st.session_state['Authorization']}
    resposta = requests.get(f'https://sprint-c82dfd49e88d.herokuapp.com/dashboard/{match_id}', headers=headers)
    resposta_quebra = resposta.json()['quebra_linha']
    resposta_cruz = resposta.json()['cruzamento']
    times = resposta_quebra['time']
    id_times = []
    nome_times = []
    for time in times:
        id_times.append(time[0])
    id_times = [int(numero) for numero in id_times]

    #Código que retorna os videos de todas as rupturas em um dict
    todas_rupturas = infos_ruptura(resposta_quebra, id_times)
    rupturas_time_1 = gera_dict_links_time(todas_rupturas[0])
    rupturas_time_2 = gera_dict_links_time(todas_rupturas[1])

    #Mesma coisa, mas para os cruzamentos
    todas_rupturas = infos_cruzamento(resposta_cruz, id_times)
    cruzamentos_time_1 = gera_dict_links_time(todas_rupturas[0])
    cruzamentos_time_2 = gera_dict_links_time(todas_rupturas[1])
    
    
    st.sidebar.header("Análises:")

    st.sidebar.write(' ')
    st.sidebar.write(' ')

    if st.sidebar.button("Cruzamentos"):
        st.session_state['sub_page'] = 'cruzamentos'
    if st.sidebar.button("Quebra de Linhas"):
        st.session_state['sub_page'] = 'quebra'


    if st.session_state['sub_page'] == 'cruzamentos':
        st.header('Cruzamento com Bola em Movimento')
        
        dados_cruzamentos = cruzamentos_por_time(resposta_cruz, id_times)
        for i in range(2):
            nome_times.append(resposta_cruz['time'][f'{id_times[i]}']['nome'])

        time_casa, time_visi = st.tabs([f"{nome_times[0]}",f"{nome_times[1]}"])

        with time_casa:
            info = ['','',False ]
            st.header("Visão Geral")
            st.image('assets/campo.jpeg')

            st.header('Top 5 Cruzamentos')

            top_5_cruz = top_5_cruzamentos(resposta_cruz, id_times[0])
            df_lista = pd.DataFrame(
            {
                "Jogador": list(top_5_cruz.keys())[:5],
                "Nº de Cruzamentos": list(top_5_cruz.values())[:5],

                }
                )


            df_grafico = pd.DataFrame(
                {
                    "Jogador": list(top_5_cruz.keys()),
                    "Nº de Cruzamentos": list(top_5_cruz.values()),

                }
                )

            st.dataframe(data=df_lista, hide_index=True)
                
            st.header('Gráfico de cruzamentos')
            grafico_jogadores_cruzamentos = alt.Chart(df_grafico).mark_bar().encode(
                    x='Jogador',
                    y='Nº de Cruzamentos',
                )
            st.altair_chart(grafico_jogadores_cruzamentos, use_container_width=True)

            st.header('Desfechos')
            grafico_desfechos_cruzamentos_time_1 = grafico_desfechos_cruzamentos(resposta_cruz, id_times[0])
            st.plotly_chart(grafico_desfechos_cruzamentos_time_1, use_container_width=True)
                
            st.header('Lances')
            data = []
            all_data = []
            for key, dados in dados_cruzamentos[0].items():
                data.append(f"{key}------{dados['instante_cruzamento']}-{dados['tempo']} / {dados['desfecho']} / {dados['zona']}")
                all_data.append(dados)

            with st.expander("Lista de Cruzamentos"):
                    selected_box = st.selectbox("Selecione um cruzamento:", data)
                    selected_cruzamento = selected_box.split('-', 1)[0]
                    selected_video = cruzamentos_time_1[selected_cruzamento]
                    index_cruzamento = int(selected_cruzamento.split('_', 1)[1]) - 1



            if selected_video:
                    st.markdown(selected_video, unsafe_allow_html=True)
                    atacantes = all_data[index_cruzamento]['atacantes'].split(',')
                    defensores = all_data[index_cruzamento]['defensores'].split(',')

                    max_len = max(len(atacantes), len(defensores))


                    atacantes += [None] * (max_len - len(atacantes))
                    defensores += [None] * (max_len - len(defensores))

                    data = pd.DataFrame({
                        "Atacando": atacantes,
                        "Defendendo": defensores,
                        "Desfecho": [all_data[index_cruzamento]['desfecho']] + [None] * (max_len - 1),
                        "Zona": [all_data[index_cruzamento]['zona']] + [None] * (max_len - 1)
                    })

                    st.dataframe(data=data, hide_index=True)                

        with time_visi:
            info = ['','',False ]
            st.header("Visão Geral")
            st.image('assets/campo.jpeg')

            st.header('Top 5 Cruzamentos')

            top_5_cruz = top_5_cruzamentos(resposta_cruz, id_times[1])
            df_lista = pd.DataFrame(
                {
                    "Jogador": list(top_5_cruz.keys())[:5],
                    "Nº de Cruzamentos": list(top_5_cruz.values())[:5],

                }
                )

            df_grafico = pd.DataFrame(
                {
                    "Jogador": list(top_5_cruz.keys()),
                    "Nº de Cruzamentos": list(top_5_cruz.values()),

                }
                )

            st.dataframe(data=df_lista, hide_index=True)
                

            st.header('Gráfico de cruzamentos')
            grafico_jogadores_cruzamentos = alt.Chart(df_grafico).mark_bar().encode(
                    x='Jogador',
                    y='Nº de Cruzamentos',
                )
            st.altair_chart(grafico_jogadores_cruzamentos, use_container_width=True)

            st.header('Desfechos')
            grafico_desfechos_cruzamentos_time_2 = grafico_desfechos_cruzamentos(resposta_cruz, id_times[1])
            st.plotly_chart(grafico_desfechos_cruzamentos_time_2, use_container_width=True)
                        
            st.header('Lances')
            data = []
            all_data = []
            for key, dados in dados_cruzamentos[1].items():
                    data.append(f"{key}------{dados['instante_cruzamento']}-{dados['tempo']} / {dados['desfecho']} / {dados['zona']}")
                    all_data.append(dados)

            with st.expander("Lista de Cruzamentos"):
                    selected_box = st.selectbox("Selecione um cruzamento:", data)
                    selected_cruzamento = selected_box.split('-', 1)[0]
                    selected_video = cruzamentos_time_2[selected_cruzamento]
                    index_cruzamento = int(selected_cruzamento.split('_', 1)[1]) - 1



            if selected_video:
                    st.markdown(selected_video, unsafe_allow_html=True)
                    atacantes = all_data[index_cruzamento]['atacantes'].split(',')
                    defensores = all_data[index_cruzamento]['defensores'].split(',')

                    max_len = max(len(atacantes), len(defensores))

                    atacantes += [None] * (max_len - len(atacantes))
                    defensores += [None] * (max_len - len(defensores))

                    data = pd.DataFrame({
                        "Atacando": atacantes,
                        "Defendendo": defensores,
                        "Desfecho": [all_data[index_cruzamento]['desfecho']] + [None] * (max_len - 1),
                        "Zona": [all_data[index_cruzamento]['zona']] + [None] * (max_len - 1)
                    })

                    st.dataframe(data=data, hide_index=True)    


    if st.session_state['sub_page'] == 'quebra':
        st.header('Quebra de Linha de Defesa')
        dados_ruptura_lances = infos_ruptura(resposta_quebra, id_times)

        for i in range(2):
            nome_times.append(resposta_quebra['time'][f'{id_times[i]}']['nome'])

        time_casa, time_visi = st.tabs([f"{nome_times[0]}",f"{nome_times[1]}"])

        with time_casa:
            info = ['','',False ]
            st.header("Visão Geral")
            st.image('assets/campo.jpeg')

            st.header('TOP 5 Rupturas')

            top_5_rupturas_time_1 = top_5_rupturas(resposta_quebra, id_times[0])
            df = pd.DataFrame(
            {
                    "Jogador": list(top_5_rupturas_time_1.keys()),
                    "Nº de Rupturas": list(top_5_rupturas_time_1.values()),

            }
                )
            st.dataframe(data=df, hide_index=True)

            st.header('Desfechos')
            grafico_desfechos_quebra_linha_time_1 = grafico_desfechos_quebra_linha(resposta_quebra, id_times[0])
            st.plotly_chart(grafico_desfechos_quebra_linha_time_1, use_container_width=True)
                
            st.header('Lances')
            data = []
            all_data = []
            for key, dados in dados_ruptura_lances[0].items():
                    data.append(f"{key}------{dados['instante_ruptura']}-{dados['tempo']} / {dados['desfecho']} / {dados['zona']}")
                    all_data.append(dados)
                    
            with st.expander("Lista de Rupturas"):
                    selected_box = st.selectbox("Selecione uma ruptura:", data)
                    selected_ruptura = selected_box.split('-', 1)[0]
                    selected_video = rupturas_time_1[selected_ruptura]
                    index_ruptura = int(selected_ruptura.split('_', 1)[1]) - 1

            if selected_video:
                    st.markdown(selected_video, unsafe_allow_html=True)
                    posse_bola = all_data[index_ruptura]['posse_bola'].split(',') if all_data[index_ruptura].get('posse_bola') else []
                    jogador_ruptura = [all_data[index_ruptura]['jogador_em_ruptura']] if all_data[index_ruptura].get('jogador_em_ruptura') else []
                    defesa = all_data[index_ruptura]['jogadores_defesa'] if all_data[index_ruptura].get('jogadores_defesa') else []

                    max_len = max(len(posse_bola), len(jogador_ruptura), len(defesa))

                    posse_bola += [None] * (max_len - len(posse_bola))
                    jogador_ruptura += [None] * (max_len - len(jogador_ruptura))
                    defesa += [None] * (max_len - len(defesa))

                    data = pd.DataFrame({
                        "Posse de bola": posse_bola,
                        "Jogador em Ruptura": jogador_ruptura,
                        "Linha de Defesa": defesa,
                        "Desfecho": [all_data[index_ruptura]['desfecho']] + [None] * (max_len - 1),
                        "Zona": [all_data[index_ruptura]['zona']] + [None] * (max_len - 1)
                    })
                    st.dataframe(data=data, hide_index=True)    

        with time_visi:
            info = ['','',False ]
            st.header("Visão Geral")
            st.image('assets/campo.jpeg')

            st.header('TOP 5 Rupturas')

            top_5_rupturas_time_2 = top_5_rupturas(resposta_quebra, id_times[1])
            df = pd.DataFrame(
                    {
                        "Jogador": list(top_5_rupturas_time_2.keys()),
                        "Nº de Rupturas": list(top_5_rupturas_time_2.values()),

                    }
                )
            st.dataframe(data=df, hide_index=True)

            st.header('Desfechos')
            grafico_desfechos_quebra_linha_time_2 = grafico_desfechos_quebra_linha(resposta_quebra, id_times[1])
            st.plotly_chart(grafico_desfechos_quebra_linha_time_2, use_container_width=True)
                        

            st.header('Lances')
            data = []
            all_data = []
            for key, dados in dados_ruptura_lances[1].items():
                    data.append(f"{key}------{dados['instante_ruptura']}-{dados['tempo']} / {dados['desfecho']} / {dados['zona']}")
                    all_data.append(dados)
                    
            with st.expander("Lista de Rupturas"):
                    selected_box = st.selectbox("Selecione uma ruptura:", data)
                    selected_ruptura = selected_box.split('-', 1)[0]
                    selected_video = rupturas_time_2[selected_ruptura]
                    index_ruptura = int(selected_ruptura.split('_', 1)[1]) - 1

                
            if selected_video:
                    st.markdown(selected_video, unsafe_allow_html=True)
                    posse_bola = all_data[index_ruptura]['posse_bola'].split(',') if all_data[index_ruptura].get('posse_bola') else []
                    jogador_ruptura = [all_data[index_ruptura]['jogador_em_ruptura']] if all_data[index_ruptura].get('jogador_em_ruptura') else []
                    defesa = all_data[index_ruptura]['jogadores_defesa'] if all_data[index_ruptura].get('jogadores_defesa') else []

                    max_len = max(len(posse_bola), len(jogador_ruptura), len(defesa))

                    posse_bola += [None] * (max_len - len(posse_bola))
                    jogador_ruptura += [None] * (max_len - len(jogador_ruptura))
                    defesa += [None] * (max_len - len(defesa))

                    data = pd.DataFrame({
                        "Posse de bola": posse_bola,
                        "Jogador em Ruptura": jogador_ruptura,
                        "Linha de Defesa": defesa,
                        "Desfecho": [all_data[index_ruptura]['desfecho']] + [None] * (max_len - 1),
                        "Zona": [all_data[index_ruptura]['zona']] + [None] * (max_len - 1)
                    })
                    
                    st.dataframe(data=data, hide_index=True)    

    st.sidebar.markdown("---")
    if st.sidebar.button("Voltar"):
        st.session_state['pagina'] = "lista_partidas"
        st.rerun()
    if st.sidebar.button("Logout"):
        realiza_logout()
    
if __name__ == "__main__":
    main()
