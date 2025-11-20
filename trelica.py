import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math


def desenhar_trelica():
    fig, ax = plt.subplots(figsize=(10, 6))

    # --- 1. Definindo as Coordenadas dos Nós (Geometria) ---
    # Assumindo altura h = 1 metro para facilitar a proporção
    h = 1.0

    # Nó 1: Origem (0,0)
    n1 = (0, 0)

    # Nó 4: Sobe a 45 graus. Se h=1, x=1 (tan 45 = 1)
    n4 = (1, 1)

    # Nó 2: Base do triângulo esquerdo. Simétrico ao eixo Y do triângulo se fosse isósceles,
    # mas aqui desce de N4 a 45 graus para a direita? Não, a imagem mostra geometria.
    # N1->N4 (45deg). N4->N2 (45deg). Então N2 está em x=2.
    n2 = (2, 0)

    # Nó 5: Topo direita. Conectado ao N2 a 60 graus.
    # dx = h / tan(60) = 1 / 1.732 = 0.577
    # x_n5 = x_n2 + 0.577 = 2.577
    n5 = (2 + 1 / math.tan(math.radians(60)), 1)

    # Nó 3: Base direita. Conectado ao N5 a 30 graus.
    # dx = h / tan(30) = 1 / 0.577 = 1.732
    # x_n3 = x_n5 + 1.732
    n3 = (n5[0] + 1 / math.tan(math.radians(30)), 0)

    nodes = {1: n1, 2: n2, 3: n3, 4: n4, 5: n5}

    # --- 2. Definindo as Barras (Conexões) e Labels das Forças ---
    # Formato: (Nó_Inicio, Nó_Fim, Nome_Força, Cor)
    bars = [
        (1, 4, "F1", "blue"),
        (1, 2, "F2", "green"),
        (4, 2, "F3", "purple"),
        (4, 5, "F4", "orange"),
        (2, 5, "F5", "brown"),
        (2, 3, "F6", "green"),
        (5, 3, "F7", "blue")
    ]

    # --- 3. Desenhando as Barras ---
    for start, end, label, color in bars:
        x_vals = [nodes[start][0], nodes[end][0]]
        y_vals = [nodes[start][1], nodes[end][1]]

        # Linha da barra
        ax.plot(x_vals, y_vals, color='black', linewidth=2, zorder=1)

        # Texto da Força (no meio da barra)
        mid_x = sum(x_vals) / 2
        mid_y = sum(y_vals) / 2

        # Ajuste fino para o texto não ficar em cima da linha
        offset = 0.15
        ax.text(mid_x, mid_y + 0.05, label, color=color, fontsize=12, fontweight='bold',
                bbox=dict(facecolor='white', edgecolor='none', alpha=0.7), ha='center')

    # --- 4. Desenhando os Nós ---
    for n_id, (nx, ny) in nodes.items():
        ax.plot(nx, ny, 'ko', markersize=10, zorder=2)  # Bolinha preta
        ax.text(nx, ny - 0.2, f"Nó {n_id}", ha='center', fontsize=9)

    # --- 5. Desenhando as Cargas (Setas) ---
    # Carga 500 no Nó 4
    ax.arrow(n4[0], n4[1] + 0.8, 0, -0.6, head_width=0.1, head_length=0.2, fc='red', ec='red', width=0.02)
    ax.text(n4[0], n4[1] + 0.9, "500", color='red', ha='center', fontweight='bold')

    # Carga 100 no Nó 5
    ax.arrow(n5[0], n5[1] + 0.8, 0, -0.6, head_width=0.1, head_length=0.2, fc='red', ec='red', width=0.02)
    ax.text(n5[0], n5[1] + 0.9, "100", color='red', ha='center', fontweight='bold')

    # --- 6. Apoios (Representação Simplificada) ---
    # Apoio Fixo (Nó 1) - Triângulo
    ax.plot([n1[0], n1[0] - 0.2, n1[0] + 0.2, n1[0]], [n1[1], n1[1] - 0.2, n1[1] - 0.2, n1[1]], 'k-', linewidth=1)
    # Apoio Móvel (Nó 3) - Triângulo + Bolinhas
    ax.plot([n3[0], n3[0] - 0.2, n3[0] + 0.2, n3[0]], [n3[1], n3[1] - 0.2, n3[1] - 0.2, n3[1]], 'k-', linewidth=1)
    ax.plot(n3[0] - 0.1, n3[1] - 0.25, 'ko', markersize=4)
    ax.plot(n3[0] + 0.1, n3[1] - 0.25, 'ko', markersize=4)

    # Configurações do Gráfico
    ax.set_aspect('equal')
    ax.set_title("Mapa de Forças da Treliça", fontsize=16)
    ax.axis('off')  # Esconde eixos x/y numéricos
    plt.tight_layout()
    plt.show()


# Executa
if __name__ == "__main__":
    desenhar_trelica()