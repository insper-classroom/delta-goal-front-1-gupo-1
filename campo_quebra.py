import streamlit as st
import plotly.express as px
from PIL import Image, ImageDraw, ImageFont
from functions import *

dict_quebra = {'Ruptura 1':
                {'logo': 'https://api.deltagoal.ai/1/logo.png',
                'instante_ruptura': '00:04:57',
                'tempo': '1º Tempo',
                'desfecho': 'ForÃ§ou a saÃ\xadda de bola adversÃ¡ria',
                'zona': 'Zona 2',
                'posse_bola': 'G. Gomez',
                'jogador_em_ruptura': 'Vanderlan',
                'jogadores_defesa': ['Helinho', 'J. Hurtado', 'Natan']},
                'Ruptura 2': 
                {'logo': 'https://api.deltagoal.ai/1/logo.png',
                 'instante_ruptura': '00:10:12',
                  'tempo': '1º Tempo',
                   'desfecho': 'Passe nÃ£o concluÃ\xaddo',
                    'zona': 'Zona 1 - B',
                    'posse_bola': 'R. Veiga',
                    'jogador_em_ruptura': 'Rony',
                    'jogadores_defesa': ['Natan', 'Eric Ramires']},
                    'Ruptura 3': 
                {'logo': 'https://api.deltagoal.ai/1/logo.png',
                 'instante_ruptura': '00:15:02',
                  'tempo': '1º Tempo',
                   'desfecho': 'Passou a bola',
                    'zona': 'Zona 1 - B',
                    'posse_bola': 'Artur',
                    'jogador_em_ruptura': 'R. Veiga',
                    'jogadores_defesa': ['Eric Ramires', 'B. Goncalves']},
                    'Ruptura 4': 
                {'logo': 'https://api.deltagoal.ai/1/logo.png',
                 'instante_ruptura': '00:51:02',
                  'tempo': '2º Tempo',
                   'desfecho': 'Passou a bola',
                    'zona': 'Zona 2',
                    'posse_bola': 'R. Veiga',
                    'jogador_em_ruptura': 'Rony',
                    'jogadores_defesa': ['E. Santos', 'Juninho Capixaba']},
                    'Ruptura 5': 
                {'logo': 'https://api.deltagoal.ai/1/logo.png',
                 'instante_ruptura': '00:52:28',
                  'tempo': '2º Tempo',
                   'desfecho': 'Passou a bola',
                    'zona': 'Zona 2',
                    'posse_bola': 'Artur',
                    'jogador_em_ruptura': 'Mayke',
                    'jogadores_defesa': ['Juninho Capixaba', 'B. Goncalves']},
                    'Ruptura 6': 
                {'logo': 'https://api.deltagoal.ai/1/logo.png',
                 'instante_ruptura': '00:52:57',
                  'tempo': '2º Tempo',
                   'desfecho': 'Foi desarmado',
                    'zona': 'Zona 1 - B',
                    'posse_bola': 'Dudu',
                    'jogador_em_ruptura': 'Vanderlan',
                    'jogadores_defesa': ['Helinho', 'J. Hurtado']},
                    'Ruptura 7': 
                {'logo': 'https://api.deltagoal.ai/1/logo.png',
                 'instante_ruptura': '01:32:37',
                  'tempo': '2º Tempo',
                   'desfecho': 'NÃ£o recebeu a bola',
                    'zona': 'Zona 1 - B',
                    'posse_bola': 'Tabata',
                    'jogador_em_ruptura': 'Richard Rios',
                    'jogadores_defesa': ['Vitor Hugo', 'Juninho Capixaba', 'E. Santos']}}

campo = Image.open('assets\campo2.png')
campo_cruzamentos = campo.resize((1200, 800))
draw = ImageDraw.Draw(campo_cruzamentos)


zonas = {
    "Zona 1 - B": ( 0 , 0),
    "Zona 1 - A": (200, 0),
    "Zona 2":     (400, 0),
    "Zona 3 - A": (800, 0),
    "Zona 3 - B": (1000, 0)
}

dict_porcentagem = {}

# calcular a porcentagem de presença em cada zona
for quebra in dict_quebra.values():
    for info, valor in quebra.items():
        if info == "zona":
            zona = valor
            if zona in dict_porcentagem:
                dict_porcentagem[zona] += 1
            else:
                dict_porcentagem[zona] = 1

# desenhar as porcentagens no campo

for zona, valor in dict_porcentagem.items():
    if zona == "Zona 2":
        posicao = (zonas[zona][0] + 65, zonas[zona][1] + 170)
        draw.text(posicao, f"{(valor / sum(dict_porcentagem.values())):.2f}%", (255, 255, 255), font_size=35)
    else:
        posicao = (zonas[zona][0] + 80, zonas[zona][1] + 170)
        draw.text(posicao, f"{(valor / sum(dict_porcentagem.values())):.2f}%", (255, 255, 255), font_size=35)

    # posicao = (zonas["zona_1"]["D1.1"][0] + 40, zonas["zona_1"]["D1.1"][1] + 70)
    # draw.text(posicao, f"{(dict_porcentagem[zona] / len(dict_quebra.values())):.2f}%", (255, 255, 255), font_size=35)



        
st.image(campo_cruzamentos)

        

def main():
    st.title('Campo de Futebol Interativos')

if __name__ == "__main__":
    main()
