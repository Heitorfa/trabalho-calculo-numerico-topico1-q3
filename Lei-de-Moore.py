import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# --- LÓGICA MATEMÁTICA OTIMIZADA (Novos Dados) ---

def calcular_mmq_detalhado():
    """
    Realiza o MMQ usando um conjunto de dados clássico da Lei de Moore
    para que o modelo MMQ (N = alpha * 10^(beta * Ano)) se ajuste
    mais precisamente à curva exponencial esperada.
    """
    # 1. Dados OTIMIZADOS da Lei de Moore (Mais próximos de uma curva perfeita)
    # A curva MMQ deve se ajustar perfeitamente a estes dados.
    x_ano = np.array([1971, 1974, 1978, 1982, 1985, 1989, 1993, 1997, 2000, 2003, 2006], dtype=np.float64)
    N = np.array([2300, 5000, 29000, 120000, 275000, 1200000, 3100000, 7500000, 42000000, 100000000, 200000000],
                 dtype=np.float64)
    n_pontos = len(x_ano)

    # 2. Linearização e Centralização (Mantida para precisão numérica)
    y_log = np.log10(N)

    x_medio = np.mean(x_ano)
    t = x_ano - x_medio

    # 3. Cálculo dos Somatórios (Usando 't' e 'y')
    sum_t = np.sum(t)
    sum_t2 = np.sum(t ** 2)
    sum_y = np.sum(y_log)
    sum_ty = np.sum(t * y_log)

    # 4. Solução do Sistema Simplificado
    A_angular = sum_ty / sum_t2  # beta (inclinação)
    B_t_linear = sum_y / n_pontos  # média(y_log)

    # 5. Parâmetros MMQ:
    beta = A_angular
    B_linear = B_t_linear - (A_angular * x_medio)
    alpha = 10 ** B_linear

    # Retorna string de memória de cálculo
    detalhes_calculo = (
        f"PASSO 1: CENTRALIZAÇÃO DE TEMPO (Novos Dados)\n"
        f"--------------------------------------------\n"
        f"Média dos Anos (x_medio) = {x_medio:.6f}\n"
        f"Nova variável: t = Ano - {x_medio:.6f}\n\n"
        f"PASSO 2: TABELA DE SOMATÓRIOS (n={n_pontos})\n"
        f"--------------------------------------------\n"
        f"Σ t    = {sum_t:.6f} (~0)\n"
        f"Σ t²   = {sum_t2:,.4f}\n"
        f"Σ y    = {sum_y:.6f}  (onde y = log10(N))\n"
        f"Σ t·y  = {sum_ty:,.6f}\n\n"
        f"PASSO 3: SOLUÇÃO DO SISTEMA SIMPLIFICADO\n"
        f"--------------------------------------------\n"
        f"A (Angular/Inclinação) = Σ t·y / Σ t² = {A_angular:.6f}\n"
        f"B_t (Intercepto em t=0) = Σ y / n = {B_t_linear:.6f}\n\n"
        f"PASSO 4: MODELO FINAL\n"
        f"--------------------------------------------\n"
        f"Intercepto original (B) = B_t - A * x_medio = {B_linear:.6f}\n"
        f"alpha = 10^B = {alpha:.4e}\n"
        f"Equação: N = {alpha:.4e} * 10^({A_angular:.5f} * Ano)"
    )

    return x_ano, N, y_log, alpha, beta, B_linear, detalhes_calculo


def prever(ano, alpha, beta):
    """Calcula o valor de N a partir do modelo MMQ."""
    return alpha * (10 ** (beta * ano))


# --- INTERFACE GRÁFICA (MooreAppStepByStep - Sem Alterações) ---

class MooreAppStepByStep:
    def __init__(self, root):
        self.root = root
        self.root.title("Lei de Moore - Método MMQ Passo a Passo (Dados Clássicos)")
        self.root.state('zoomed')

        style = ttk.Style()
        style.configure("Big.TLabel", font=("Arial", 16))
        style.configure("Header.TLabel", font=("Arial", 24, "bold"))
        style.configure("Mono.TLabel", font=("Courier New", 14), background="#f0f0f0")

        self.x, self.y_real, self.y_log, self.alpha, self.beta, self.B_linear, self.texto_detalhes = calcular_mmq_detalhado()

        self.criar_abas()

    def criar_abas(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        tab_graph = ttk.Frame(notebook)
        notebook.add(tab_graph, text="  GRÁFICOS E PREVISÃO  ")
        self.setup_tab_graficos(tab_graph)

        tab_calc = ttk.Frame(notebook)
        notebook.add(tab_calc, text="  MEMÓRIA DE CÁLCULO (Passo a Passo)  ")
        self.setup_tab_calculo(tab_calc)

    def setup_tab_graficos(self, parent):
        frame_top = ttk.Frame(parent)
        frame_top.pack(fill="x", pady=10, padx=20)

        ttk.Label(frame_top, text="Lei de Moore: Resultado Visual", style="Header.TLabel").pack()

        frame_input = ttk.LabelFrame(frame_top, text="Simulação", padding=10)
        frame_input.pack(pady=10)

        ttk.Label(frame_input, text="Ano para prever:", style="Big.TLabel").pack(side="left")
        self.ent_ano = ttk.Entry(frame_input, font=("Arial", 16), width=10)
        self.ent_ano.pack(side="left", padx=10)

        btn = ttk.Button(frame_input, text="CALCULAR", command=self.calcular_custom)
        btn.pack(side="left")

        self.lbl_res = ttk.Label(frame_top, text="Insira um ano acima", style="Big.TLabel", foreground="blue")
        self.lbl_res.pack(pady=5)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

        x_line = np.linspace(1970, 2025, 100)
        y_line_log = self.beta * x_line + self.B_linear

        ax1.scatter(self.x, self.y_log, color='red', s=80, label='Dados Originais (Log)')
        ax1.plot(x_line, y_line_log, color='blue', linewidth=3, label='Reta MMQ')
        ax1.set_title("Linearização (Log10)", fontsize=14)
        ax1.grid(True)
        ax1.legend()

        y_line_exp = prever(x_line, self.alpha, self.beta)
        ax2.scatter(self.x, self.y_real, color='red', s=80, label='Dados Reais')
        ax2.plot(x_line, y_line_exp, color='green', linewidth=3, label='Curva Ajustada')
        ax2.set_title("Curva Exponencial Final", fontsize=14)
        ax2.set_yscale('log')
        ax2.grid(True)
        ax2.legend()

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def setup_tab_calculo(self, parent):
        ttk.Label(parent, text="Detalhamento do Método dos Mínimos Quadrados", style="Header.TLabel").pack(pady=20)

        text_area = tk.Text(parent, font=("Courier New", 18), bg="#f5f5f5", padx=20, pady=20)
        text_area.pack(fill="both", expand=True, padx=40, pady=20)

        text_area.insert(tk.END, self.texto_detalhes)
        text_area.config(state="disabled")

    def calcular_custom(self):
        try:
            ano = float(self.ent_ano.get())
            res = prever(ano, self.alpha, self.beta)
            self.lbl_res.config(text=f"Em {int(ano)}: {res:.2e} transistores")
        except ValueError:
            messagebox.showerror("Erro", "Ano inválido")


if __name__ == "__main__":
    root = tk.Tk()
    app = MooreAppStepByStep(root)
    root.mainloop()

