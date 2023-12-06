import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_soccer_field():
    # Criar a figura e os eixos
    fig, ax = plt.subplots(figsize=(10, 6))

    # Desenhar o campo de futebol
    ax.add_patch(patches.Rectangle((0, 0), 100, 50, linewidth=2, edgecolor='black', facecolor='#4CAF50'))

    # Área do Goleiro
    goleiro_width, goleiro_height = 16, 30
    ax.add_patch(patches.Rectangle((0, (50 - goleiro_height) / 2), goleiro_width, goleiro_height, linewidth=2, edgecolor='black', facecolor='none'))
    ax.add_patch(patches.Rectangle((100 - goleiro_width, (50 - goleiro_height) / 2), goleiro_width, goleiro_height, linewidth=2, edgecolor='black', facecolor='none'))

    # Área Pequena
    pequena_width, pequena_height = 8, 14
    ax.add_patch(patches.Rectangle((0, (50 - pequena_height) / 2), pequena_width, pequena_height, linewidth=2, edgecolor='black', facecolor='none'))
    ax.add_patch(patches.Rectangle((100 - pequena_width, (50 - pequena_height) / 2), pequena_width, pequena_height, linewidth=2, edgecolor='black', facecolor='none'))

    # Linha de Gol
    ax.plot([0, 0, 0], [0, 50, 50], color='black', linewidth=2)
    ax.plot([100, 100, 100], [0, 50, 50], color='black', linewidth=2)

    # Ponto Penal
    ax.scatter([50, 88, 12], [25, 25, 25], color='black', s=100)

    # Linhas do Meio de Campo
    ax.plot([50, 50], [0, 50], color='black', linewidth=2)

    # Linha do Fundo
    ax.plot([0, 100], [0, 0], color='black', linewidth=2)

    # Quadrados adicionais
    square_positions = [(0, 50), (16.6666666667, 50), (66.6666666667, 50), (83.3333333333, 50)]
    square_width = 16.6666666667
    square_height = -50
    for position in square_positions:
        ax.add_patch(patches.Rectangle(position, square_width, square_height, linewidth=2, edgecolor='black', facecolor=(109/255, 1/255, 111/255, 0.5)))

    # Configurações adicionais do gráfico
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 50)
    ax.set_aspect('equal', adjustable='box')  # Para manter proporções corretas

    # Remover eixos
    ax.axis('off')

    # Exibir a figura
    st.pyplot(fig)

def main():
    st.title('Campo de Futebol Interativos')

    # Chamar a função para desenhar o campo de futebol
    draw_soccer_field()

if __name__ == "__main__":
    main()
