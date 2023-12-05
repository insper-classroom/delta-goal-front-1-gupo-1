import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_soccer_field():
    # Criar a figura e os eixos
    fig, ax = plt.subplots(figsize=(10, 6))

    # Desenhar o campo de futebol
    ax.add_patch(patches.Rectangle((0, 0), 100, 50, linewidth=2, edgecolor='black', facecolor='#4CAF50'))

    # Área do Goleiro
    goleiro_width = 16
    goleiro_height = 30
    ax.add_patch(patches.Rectangle((0, (50 - goleiro_height) / 2), goleiro_width, goleiro_height, linewidth=2, edgecolor='black', facecolor='none'))
    ax.add_patch(patches.Rectangle((100 - goleiro_width, (50 - goleiro_height) / 2), goleiro_width, goleiro_height, linewidth=2, edgecolor='black', facecolor='none'))

    # Área Pequena
    pequena_width = 8
    pequena_height = 14
    ax.add_patch(patches.Rectangle((0, (50 - pequena_height) / 2), pequena_width, pequena_height, linewidth=2, edgecolor='black', facecolor='none'))
    ax.add_patch(patches.Rectangle((100 - pequena_width, (50 - pequena_height) / 2), pequena_width, pequena_height, linewidth=2, edgecolor='black', facecolor='none'))

    # Linha de Gol
    ax.plot([0, 0, 0], [0, 50, 50], color='black', linewidth=2)
    ax.plot([100, 100, 100], [0, 50, 50], color='black', linewidth=2)

    # Ponto Penal
    ax.scatter([50], [25], color='black', s=100)
    # Pontos Penais adicionais
    ax.scatter([88], [25], color='black', s=100)
    ax.scatter([12], [25], color='black', s=100)

    # Linhas do Meio de Campo
    ax.plot([50, 50], [0, 50], color='black', linewidth=2)

    # Linha do Fundo
    ax.plot([0, 100], [0, 0], color='black', linewidth=2)

  # AREA CAMPO ESQUERDA
    quadrado1 = patches.Rectangle((0, 40), 8, 10, linewidth=2, edgecolor='black', facecolor=(109/255, 1/255, 111/255, 0.5))
    ax.add_patch(quadrado1)

    quadrado3 = patches.Rectangle((8, 40), 8, 10, linewidth=2, edgecolor='black', facecolor=(109/255, 1/255, 111/255, 0.5))
    ax.add_patch(quadrado3)

    quadrado2 = patches.Rectangle((16, 40), 8, 10, linewidth=2, edgecolor='black', facecolor=(109/255, 1/255, 111/255, 0.5))
    ax.add_patch(quadrado2)

    quadrado = patches.Rectangle((16, 25), 8, 15, linewidth=2, edgecolor='black', facecolor=(109/255, 1/255, 111/255, 0.5))
    ax.add_patch(quadrado)

    quadrado = patches.Rectangle((16, 10), 8, 15, linewidth=2, edgecolor='black', facecolor=(109/255, 1/255, 111/255, 0.5))
    ax.add_patch(quadrado)

    quadrado = patches.Rectangle((0, 0), 8, 10, linewidth=2, edgecolor='black', facecolor=(109/255, 1/255, 111/255, 0.5))
    ax.add_patch(quadrado)
 
    quadrado = patches.Rectangle((8, 0), 8, 10, linewidth=2, edgecolor='black', facecolor=(109/255, 1/255, 111/255, 0.5))
    ax.add_patch(quadrado)
 
    quadrado = patches.Rectangle((16, 0), 8, 10, linewidth=2, edgecolor='black', facecolor=(109/255, 1/255, 111/255, 0.5))
    ax.add_patch(quadrado)

    quadrado = patches.Rectangle((0, 40), 16, -8, linewidth=2, edgecolor='black', facecolor=(109/255, 1/255, 111/255, 0.5))
    ax.add_patch(quadrado)

    quadrado = patches.Rectangle((0, 18), 16, -8, linewidth=2, edgecolor='black', facecolor=(109/255, 1/255, 111/255, 0.5))
    ax.add_patch(quadrado)

    #Area Campo direita
    quadrado1 = patches.Rectangle((84, 40), 8, 10, linewidth=2, edgecolor='black', facecolor=(109/255, 1/255, 111/255, 0.5))
    ax.add_patch(quadrado1)

    quadrado3 = patches.Rectangle((92, 40), 8, 10, linewidth=2, edgecolor='black', facecolor=(109/255, 1/255, 111/255, 0.5))
    ax.add_patch(quadrado3)

    quadrado2 = patches.Rectangle((76, 40), 8, 10, linewidth=2, edgecolor='black', facecolor=(109/255, 1/255, 111/255, 0.5))
    ax.add_patch(quadrado2)

    quadrado = patches.Rectangle((76, 25), 8, 15, linewidth=2, edgecolor='black', facecolor=(109/255, 1/255, 111/255, 0.5))
    ax.add_patch(quadrado)

    quadrado = patches.Rectangle((76, 10), 8, 15, linewidth=2, edgecolor='black', facecolor=(109/255, 1/255, 111/255, 0.5))
    ax.add_patch(quadrado)

    quadrado = patches.Rectangle((92, 0), 8, 10, linewidth=2, edgecolor='black', facecolor=(109/255, 1/255, 111/255, 0.5))
    ax.add_patch(quadrado)
 
    quadrado = patches.Rectangle((84, 0), 8, 10, linewidth=2, edgecolor='black', facecolor=(109/255, 1/255, 111/255, 0.5))
    ax.add_patch(quadrado)
 
    quadrado = patches.Rectangle((76, 0), 8, 10, linewidth=2, edgecolor='black', facecolor=(109/255, 1/255, 111/255, 0.5))
    ax.add_patch(quadrado)

    quadrado = patches.Rectangle((84, 40), 16, -8, linewidth=2, edgecolor='black', facecolor=(109/255, 1/255, 111/255, 0.5))
    ax.add_patch(quadrado)

    quadrado = patches.Rectangle((84, 18), 16, -8, linewidth=2, edgecolor='black', facecolor=(109/255, 1/255, 111/255, 0.5))
    ax.add_patch(quadrado)


    # Configurações adicionais do gráfico
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 50)
    ax.set_aspect('equal', adjustable='box')  # Para manter proporções corretas

    # Remover eixos
    ax.axis('off')

    # Exibir a figura
    st.pyplot(fig)

def main():
    st.title('Campo de Futebol Interativo')

    # Chamar a função para desenhar o campo de futebol
    draw_soccer_field()

if __name__ == "__main__":
    main()
