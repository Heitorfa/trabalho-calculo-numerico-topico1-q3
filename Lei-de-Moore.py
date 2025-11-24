import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# --- LÓGICA MATEMÁTICA (Inalterada) ---

def calcular_mmq():
    """
    Realiza o Ajuste de Curvas pelo Método dos Mínimos Quadrados (MMQ).
    """
    # 1. Dados de Entrada
    anos = np.array([1971, 1972, 1974, 1978, 1982, 1986, 1989, 1993, 1997, 1999, 2000])
    transistores = np.array([2250, 3300, 6000, 29000, 134000, 275000, 1200000, 3100000, 7500000, 9500000, 42000000])

    # 2. Linearização (Log10)
    log_transistores = np.log10(transistores)

    # 3. Resolução do Sistema (MMQ)
    coeficientes = np.polyfit(anos, log_transistores, 1)

    beta = coeficientes[0]  # Inclinação (A)
    log_alpha = coeficientes[1]  # Intercepto (B)

    # 4. Deslinearização
    alpha = 10 ** log_alpha

    return anos, transistores, log_transistores, alpha, beta, log_alpha


def prever(ano, alpha, beta):
    return alpha * (10 ** (beta * ano))


# --- INTERFACE GRÁFICA (Ajustada para Projetor) ---

class MooreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ajuste de Curvas - Lei de Moore (Modo Apresentação)")
        # Janela maximizada ou bem grande
        self.root.state('zoomed')

        # Configuração de Estilo para Fontes Grandes
        style = ttk.Style()
        style.configure("TLabel", font=("Arial", 16))
        style.configure("TButton", font=("Arial", 14, "bold"))
        style.configure("TLabelframe.Label", font=("Arial", 14, "bold"))

        # Realiza os cálculos
        self.anos, self.N_real, self.log_N, self.alpha, self.beta, self.log_alpha = calcular_mmq()

        self.criar_widgets()
        self.plotar_graficos()

    def criar_widgets(self):
        # Frame Principal com padding maior
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill="both", expand=True)

        # Título Gigante
        lbl_titulo = ttk.Label(main_frame, text="Lei de Moore: Ajuste via MMQ", font=("Arial", 28, "bold"))
        lbl_titulo.pack(pady=20)

        # Explicação Matemática (Fonte Grande)
        txt_expl = (
            f"Modelo Linearizado: log10(N) = {self.beta:.5f} * Ano + ({self.log_alpha:.2f})\n"
            f"Modelo Exponencial: N = {self.alpha:.2e} * 10^({self.beta:.5f} * t)"
        )
        lbl_info = ttk.Label(main_frame, text=txt_expl, font=("Courier New", 18, "bold"), background="#e0e0e0",
                             padding=15)
        lbl_info.pack(pady=10, fill="x")

        # Container horizontal para Previsões e Input
        top_container = ttk.Frame(main_frame)
        top_container.pack(fill="x", pady=20)

        # Previsões Solicitadas (Esquerda)
        frame_prev = ttk.LabelFrame(top_container, text="Previsões Fixas", padding=15)
        frame_prev.pack(side="left", fill="both", expand=True, padx=(0, 10))

        p2010 = prever(2010, self.alpha, self.beta)
        p2020 = prever(2020, self.alpha, self.beta)

        ttk.Label(frame_prev, text=f"• 2010: {p2010:.2e} transistores", font=("Arial", 16)).pack(anchor="w")
        ttk.Label(frame_prev, text=f"• 2020: {p2020:.2e} transistores", font=("Arial", 16)).pack(anchor="w")

        # Input do Usuário (Direita)
        frame_input = ttk.LabelFrame(top_container, text="Simulação Interativa", padding=15)
        frame_input.pack(side="left", fill="both", expand=True, padx=(10, 0))

        input_inner = ttk.Frame(frame_input)
        input_inner.pack(pady=5)

        ttk.Label(input_inner, text="Ano: ", font=("Arial", 18)).pack(side="left")
        self.ent_ano = ttk.Entry(input_inner, width=10, font=("Arial", 18))
        self.ent_ano.pack(side="left", padx=10)

        # Botão maior
        btn = ttk.Button(input_inner, text="CALCULAR", command=self.calcular_custom)
        btn.pack(side="left", padx=10)

        self.lbl_res_custom = ttk.Label(frame_input, text="Resultado aparecerá aqui", foreground="blue",
                                        font=("Arial", 16, "bold"))
        self.lbl_res_custom.pack(pady=10)

        # Container para Gráficos
        self.frame_graph = ttk.Frame(main_frame)
        self.frame_graph.pack(fill="both", expand=True)

    def calcular_custom(self):
        try:
            ano = float(self.ent_ano.get())
            res = prever(ano, self.alpha, self.beta)
            self.lbl_res_custom.config(text=f"Em {int(ano)}: {res:.2e} transistores")
        except ValueError:
            messagebox.showerror("Erro", "Digite um ano válido numérico.")

    def plotar_graficos(self):
        # Aumentar fonte global do Matplotlib para projetor
        plt.rcParams.update({'font.size': 14})
        plt.rcParams.update({'axes.titlesize': 18})
        plt.rcParams.update({'axes.labelsize': 16})
        plt.rcParams.update({'xtick.labelsize': 14})
        plt.rcParams.update({'ytick.labelsize': 14})
        plt.rcParams.update({'legend.fontsize': 14})

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

        x_linha = np.linspace(1970, 2025, 100)

        # GRÁFICO 1: LINEARIZADO
        y_linha_log = self.beta * x_linha + self.log_alpha

        # Aumentei 's' (tamanho pontos) e 'linewidth' (espessura linha)
        ax1.scatter(self.anos, self.log_N, color='red', s=100, label='Dados (Log)')
        ax1.plot(x_linha, y_linha_log, color='blue', linewidth=3, label='Reta MMQ')

        ax1.set_title("1. Linearização (Log10)")
        ax1.set_xlabel("Ano")
        ax1.set_ylabel("Log(N)")
        ax1.grid(True, linestyle='--', alpha=0.6, linewidth=1.5)
        ax1.legend()

        # GRÁFICO 2: EXPONENCIAL
        y_linha_exp = prever(x_linha, self.alpha, self.beta)

        ax2.scatter(self.anos, self.N_real, color='red', s=100, label='Dados Reais')
        ax2.plot(x_linha, y_linha_exp, color='green', linewidth=3, label='Curva Ajustada')

        # Destaque maior para os pontos de previsão
        ax2.scatter([2010, 2020], [prever(2010, self.alpha, self.beta), prever(2020, self.alpha, self.beta)],
                    color='purple', s=150, zorder=5, label='Prev. 2010/2020')

        ax2.set_title("2. Curva Exponencial Final")
        ax2.set_xlabel("Ano")
        ax2.set_ylabel("Nº Transistores")
        ax2.set_yscale("log")
        ax2.grid(True, linestyle='--', alpha=0.6, linewidth=1.5)
        ax2.legend()

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.frame_graph)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = MooreApp(root)
    root.mainloop()