import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_rectangle(ax, position, width, height, color, edgecolor='black'):
    rectangle = patches.Rectangle(position, width, height, linewidth=2, edgecolor=edgecolor, facecolor=color)
    ax.add_patch(rectangle)

def draw_soccer_field():
    # Criar a figura e os eixos
    fig, ax = plt.subplots(figsize=(10, 6))

    # Desenhar o campo de futebol
    draw_rectangle(ax, (0, 0), 100, 50, '#4CAF50')

    # Área do Goleiro
    goleiro_width, goleiro_height = 16, 30
    draw_rectangle(ax, (0, (50 - goleiro_height) / 2), goleiro_width, goleiro_height, 'none')

    # Área Pequena
    pequena_width = 8
    pequena_height = 14
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

    # Configurações adicionais do gráfico
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 50)
    ax.set_aspect('equal', adjustable='box')  # Para manter proporções corretas

    # Remover eixos
    ax.axis('off')

    # Áreas do Campo
    draw_rectangle(ax, (0, 40), 8, 10, (109/255, 1/255, 111/255, 0.5))
    draw_rectangle(ax, (8, 40), 8, 10, (109/255, 1/255, 111/255, 0.5))
    draw_rectangle(ax, (16, 40), 8, 10, (109/255, 1/255, 111/255, 0.5))
    draw_rectangle(ax, (16, 25), 8, 15, (109/255, 1/255, 111/255, 0.5))
    draw_rectangle(ax, (16, 10), 8, 15, (109/255, 1/255, 111/255, 0.5))
    draw_rectangle(ax, (0, 0), 8, 10, (109/255, 1/255, 111/255, 0.5))
    draw_rectangle(ax, (8, 0), 8, 10, (109/255, 1/255, 111/255, 0.5))
    draw_rectangle(ax, (16, 0), 8, 10, (109/255, 1/255, 111/255, 0.5))
    draw_rectangle(ax, (0, 40), 16, -8, (109/255, 1/255, 111/255, 0.5))
    draw_rectangle(ax, (0, 18), 16, -8, (109/255, 1/255, 111/255, 0.5))

    draw_rectangle(ax, (84, 40), 8, 10, (109/255, 1/255, 111/255, 0.5))
    draw_rectangle(ax, (92, 40), 8, 10, (109/255, 1/255, 111/255, 0.5))
    draw_rectangle(ax, (76, 40), 8, 10, (109/255, 1/255, 111/255, 0.5))
    draw_rectangle(ax, (76, 25), 8, 15, (109/255, 1/255, 111/255, 0.5))
    draw_rectangle(ax, (76, 10), 8, 15, (109/255, 1/255, 111/255, 0.5))
    draw_rectangle(ax, (92, 0), 8, 10, (109/255, 1/255, 111/255, 0.5))
    draw_rectangle(ax, (84, 0), 8, 10, (109/255, 1/255, 111/255, 0.5))
    draw_rectangle(ax, (76, 0), 8, 10, (109/255, 1/255, 111/255, 0.5))
    draw_rectangle(ax, (84, 40), 16, -8, (109/255, 1/255, 111/255, 0.5))
    draw_rectangle(ax, (84, 18), 16, -8, (109/255, 1/255, 111/255, 0.5))

    # Exibir a figura
    st.pyplot(fig)

def main():
    st.title('Campo de Futebol Interativo')

    # Chamar a função para desenhar o campo de futebol
    draw_soccer_field()

if __name__ == "__main__":
    main()
