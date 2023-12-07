import json
import plotly.express as px
import pandas as pd


# Função para verificar em qual tempo o jogo está
def minutos_segundos(lista):
    segundos = (int(lista[0]) * 3600) + int(lista[1] * 60) + int(lista[2])
    return segundos


# Rupturas da quebra de linha de defesa
def infos_ruptura(json, times_id):
    dict_rupturas_time_x = {}
    dict_rupturas_time_y = {}

    for id in times_id:
        n_ruptura = 0
        rupturas = json["time"][f"{id}"]["rupturas"]

        for ruptura in rupturas:
            n_ruptura += 1
            instante_ruptura = ruptura["instante_ruptura"]

            # Verifica em qual tempo do jogo a ruptura ocorreu
            lista_instante_ruptura = instante_ruptura.split(":")
            segundos = minutos_segundos(lista_instante_ruptura)
            if segundos <= 2700:
                tempo = "1º T"
            else:
                tempo = "2º T"

            # Informações sobre a ruptura
            infos = {
                "logo": json["time"][f"{id}"]["logo"],
                "instante_ruptura": ruptura["instante_ruptura"],
                "tempo": tempo,
                "desfecho": ruptura["desfecho"],
                "zona": ruptura["zona_defesa"],
                "posse_bola": ruptura["nome_jogador_posse_bola"],
                "jogador_em_ruptura": ruptura["nome_jogador_ruptura"],
                "jogadores_defesa": ruptura["nomes_jogadores_defesa"],
            }

            # Adiciona as informações no dicionário
            if id == 1:
                dict_rupturas_time_x[f"ruptura_{n_ruptura}"] = infos
            else:
                dict_rupturas_time_y[f"ruptura_{n_ruptura}"] = infos

    return dict_rupturas_time_x, dict_rupturas_time_y


# Jogadores com maior número de rupturas
def top_5_rupturas(json, time_id):
    dict_top_5 = {}
    top_5 = json["time"][f"{time_id}"]["top_5"]

    for jogador in top_5:
        nome = jogador["nome"]
        n_rupturas = jogador["rupturas"]

        dict_top_5[nome] = n_rupturas
    
    return dict_top_5    


# Gráfico de desfechos das rupturas de quebra de linha
def grafico_desfechos_quebra_linha(json, time_id):
    desfechos = json["time"][f"{time_id}"]["desfechos"]
    desfecho = []
    n_rupturas = []

    for tipo, quantidade in desfechos.items():
        desfecho.append(tipo)
        n_rupturas.append(quantidade)

    # Fazendo o gráfico com o Plotly
    df = pd.DataFrame(dict(
        desfecho=desfecho,
        n_rupturas=n_rupturas
        ))
    
    fig = px.pie(df, values='n_rupturas', names='desfecho')
    fig.update_layout(legend=dict(orientation="h", y=-0.2))

    return fig


# Cruzamentos de cada time
def cruzamentos_por_time(json, times_id):
    dict_cruzamentos_time_x = {}
    dict_cruzamentos_time_y = {}

    for id in times_id:
        n_cruzamento = 0
        cruzamentos = json["time"][f"{id}"]["rupturas"]

        for cruzamento in cruzamentos:
            n_cruzamento += 1

            instante_cruzamento = cruzamento["instante_cruzamento"]

            # Verifica em qual tempo do jogo o cruzamento ocorreu
            lista_instante_cruzamento = instante_cruzamento.split(":")
            segundos = minutos_segundos(lista_instante_cruzamento)
            if segundos <= 2700:
                tempo = "1º T"
            else:
                tempo = "2º T"

            # Informações sobre o cruzamento
            infos = {
                "logo": json["time"][f"{id}"]["logo"],
                "instante_cruzamento": cruzamento["instante_cruzamento"],
                "tempo": tempo,
                "desfecho": cruzamento["desfecho"],
                "zona": cruzamento["zona"],
                "atacantes": cruzamento["nome_jogadores_time_cruzando"],
                "defensores": cruzamento["nome_jogadores_time_defendendo"],
            }

            # Adiciona as informações no dicionário
            if id == 1:
                dict_cruzamentos_time_x[f"cruzamento_{n_cruzamento}"] = infos
            else:
                dict_cruzamentos_time_y[f"cruzamento_{n_cruzamento}"] = infos
            print(dict_cruzamentos_time_x)

    return dict_cruzamentos_time_x, dict_cruzamentos_time_y


# Frequência nas sub-zonas
def frequencia_subzonas(json, times_id):
    dict_zonas_time_x = {}
    dict_zonas_time_y = {}

    for id in times_id:
        cruzamentos = json["time"][f"{id}"]["rupturas"]

        if id == times_id[0]:
            for zona in cruzamentos:
                if zona["zona"] not in dict_zonas_time_x:
                    dict_zonas_time_x[zona["zona"]] = 1
                else:
                    dict_zonas_time_x[zona["zona"]] += 1
        else:
            for zona in cruzamentos:
                if zona["zona"] not in dict_zonas_time_y:
                    dict_zonas_time_y[zona["zona"]] = 1
                else:
                    dict_zonas_time_y[zona["zona"]] += 1

    return dict_zonas_time_x, dict_zonas_time_y


# Gráfico de desfechos dos cruzamentos
def grafico_desfechos_cruzamentos(json, time_id):
    desfecho = json["time"][f"{time_id}"]["rupturas"]
    desfechos = []
    n_cruzamentos = []

    for ruptura in desfecho:
        if ruptura["desfecho"] not in desfechos:
            desfechos.append(ruptura["desfecho"])
            n_cruzamentos.append(1)
        else:
            n_cruzamentos[desfechos.index(ruptura["desfecho"])] += 1

    # Fazendo o gráfico com o Plotly
    df = pd.DataFrame(dict(
        desfecho=desfechos,
        n_cruzamentos=n_cruzamentos
        ))
    
    fig = px.pie(df, values='n_cruzamentos', names='desfecho')

    return fig

# Top 5 jogadores com mais cruzamentos
def top_5_cruzamentos(json, time_id):
    cruzamentos = json["time"][f"{time_id}"]["rupturas"]
    top_cruzamentos = {}
    for cruzamento in cruzamentos:
        nomes = (cruzamento["nome_jogadores_time_cruzando"].split(","))
        numeros = (cruzamento["numero_jogadores_time_cruzando"].split(","))
        for nome, numero in zip(nomes, numeros):
            nome = nome.strip()
            numero = numero.strip()
            if f"{numero} - {nome}" not in top_cruzamentos:
                top_cruzamentos[f"{numero} - {nome}"] = 1
            else:
                top_cruzamentos[f"{numero} - {nome}"] += 1

    dicionario_crescente = {}
    for i in sorted(top_cruzamentos, key=top_cruzamentos.get, reverse=True):
        dicionario_crescente[i] = top_cruzamentos[i]

    return dicionario_crescente

# Rupturas do cruzamento de linha de defesa
def infos_cruzamento(json, times_id):
    dict_cruzamentos_time_x = {}
    dict_cruzamentos_time_y = {}

    for id in times_id:
        n_cruzamento = 0
        rupturas = json["time"][f"{id}"]["rupturas"]

        for ruptura in rupturas:
            print(ruptura)
            n_cruzamento += 1
            instante_cruzamento = ruptura["instante_cruzamento"]

            # Verifica em qual tempo do jogo a ruptura ocorreu
            lista_instante_cruzamento = instante_cruzamento.split(":")
            segundos = minutos_segundos(lista_instante_cruzamento)
            if segundos <= 2700:
                tempo = "1º T"
            else:
                tempo = "2º T"

            # Informações sobre a ruptura
            infos = {
                "logo": json["time"][f"{id}"]["logo"],
                "instante_cruzamento": ruptura["instante_cruzamento"],
                "tempo": tempo,
                "desfecho": ruptura["desfecho"],
                "zona": ruptura["zona"],
                "jogadores_atacando": ruptura["nome_jogadores_time_cruzando"],
                "jogadores_defendendo": ruptura["nome_jogadores_time_defendendo"],
            }

            # Adiciona as informações no dicionário
            if id == 1:
                dict_cruzamentos_time_x[f"cruzamento_{n_cruzamento}"] = infos
            else:
                dict_cruzamentos_time_y[f"cruzamento_{n_cruzamento}"] = infos

    return dict_cruzamentos_time_x, dict_cruzamentos_time_y


#Função que gera o link do video, auxiliar à função de links
def gera_link(tempo):
    hora = int(tempo[:2])
    minutos = int(tempo[3:5])
    segundos = int(tempo[6:]) + (minutos * 60) + (hora * 60 * 60)

    link = f'<iframe width="640" height="512" src="https://www.youtube.com/embed/vqguX62PKFg?start={segundos - 5}&amp;end={segundos + 5};controls=0" frameborder="0" allowfullscreen></iframe>'
    return link

#Função que retorna um dict com todo os cruzamentos e os videos de onde estes aconteceram
def gera_dict_links_time(dict_rupturas):
    links = {}
    for ruptura in dict_rupturas:
        if 'instante_ruptura' in dict_rupturas[ruptura]:
            tempo = dict_rupturas[ruptura]['instante_ruptura']
            link = gera_link(tempo)
            links[ruptura] = link
        else:
            tempo = dict_rupturas[ruptura]['instante_cruzamento']
            link = gera_link(tempo)
            links[ruptura] = link
    return links