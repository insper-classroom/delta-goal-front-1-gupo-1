import streamlit as st
import plotly.express as px
from PIL import Image, ImageDraw, ImageFont
from functions import *

frequencia_cada_time = {'D2.1': 2, 'D2.2': 7, 'D1.2': 1, 'E2.2': 8, 'E1.1': 1, 'D3': 1, 'E1.2': 1}, {'D2.1': 2, 'D2.2': 7, 'D1.2': 1, 'E2.2': 8, 'E1.1': 1, 'D3': 1, 'E1.2': 1}

sub_zonas = {
    "zona_1": {
            "D1.1": (262 , 126),
            "D1.2": (261 ,  0 ),
            "D2.1": (131 ,  0 ),
            "D2.2": ( 0  ,  0 ),
            "D3":   ( 0  , 126),
            "E1.1": (262, 378),
            "E1.2": (262, 634),
            "E2.1": (131, 634),
            "E2.2": (0, 634),
            "E3": (0, 504)
    },
    "zona_3": {
            "D1.1": (786, 126),
            "D1.2": (786, 0),
            "D2.1": (917, 0),
            "D2.2": (1048, 0),
            "D3": (917, 126),
            "E1.1": (786, 378),
            "E1.2": (786, 634),
            "E2.1": (917, 634),
            "E2.2": (1048, 634),
            "E3": (917 , 504),
        }}

campo = Image.open('assets\campo1.png')
campo_cruzamentos = campo.resize((1190, 800))
draw = ImageDraw.Draw(campo_cruzamentos)

base = 1
for frequencia in frequencia_cada_time:
    if base == 1:
        for zona in frequencia:
            if zona == "D3" or zona == "E3":
                posicao = (sub_zonas["zona_3"][zona][0] + 65, sub_zonas["zona_1"][zona][1] + 75)
                draw.text(posicao, f"{(frequencia[zona] / sum(frequencia.values())):.2f}%", (255, 255, 255), font_size=35)
            else:
                posicao = (sub_zonas["zona_3"][zona][0] + 15, sub_zonas["zona_3"][zona][1] + 80)
                draw.text(posicao, f"{(frequencia[zona] / sum(frequencia.values())):.2f}%", (255, 255, 255), font_size=35)
        base += 1
    else:
        for zona in frequencia:
            if zona == "D3" or zona == "E3":
                posicao = (sub_zonas["zona_1"][zona][0] + 121, sub_zonas["zona_1"][zona][1] + 75)
                draw.text(posicao, f"{(frequencia[zona] / sum(frequencia.values())):.2f}%", (255, 255, 255), font_size=35)
            else:
                posicao = (sub_zonas["zona_1"][zona][0] + 40, sub_zonas["zona_1"][zona][1] + 70)
                draw.text(posicao, f"{(frequencia[zona] / sum(frequencia.values())):.2f}%", (255, 255, 255), font_size=35)
        
st.image(campo_cruzamentos)

        

def main():
    st.title('Campo de Futebol Interativos')

if __name__ == "__main__":
    main()
