import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
import numpy as np


def gauss_seidel(A, b, tol=1e-10, max_iter=1000, x0=None):
    """
    Implementação do método de Gauss-Seidel.
    """
    n = len(b)
    if x0 is None:
        x = np.zeros(n)
    else:
        x = x0.copy()

    for k in range(max_iter):
        x_old = x.copy()
        for i in range(n):
            sum1 = np.dot(A[i, :i], x[:i])
            sum2 = np.dot(A[i, i + 1:], x_old[i + 1:])

            # A[i, i] é o pivô diagonal
            x[i] = (b[i] - sum1 - sum2) / A[i, i]

        # Critério de parada
        if np.linalg.norm(x - x_old, ord=np.inf) < tol:
            return x, k + 1  # Solução e iterações

    return x, max_iter  # Pode não ter convergido


# --- Classe Base para as Janelas de Solver ---

class JanelaSolver(tk.Toplevel):
    """
    Classe base para uma janela de solver (Toplevel).
    Cria a grade de entradas (A e B) dinamicamente.
    """

    def __init__(self, master, title):
        super().__init__(master)
        self.title(title)
        self.geometry("600x600")

        self.entries_A = []
        self.entries_B = []
        self.n = 0  # Tamanho do sistema

        # Frame para os controles de tamanho
        frame_controles = ttk.Frame(self, padding=10)
        frame_controles.pack(fill=tk.X)

        ttk.Label(frame_controles, text="Tamanho do Sistema (N):").pack(side=tk.LEFT, padx=5)
        self.entry_n = ttk.Entry(frame_controles, width=5)
        self.entry_n.pack(side=tk.LEFT, padx=5)

        btn_atualizar = ttk.Button(frame_controles, text="Criar/Atualizar Grade", command=self.atualizar_grade)
        btn_atualizar.pack(side=tk.LEFT, padx=5)

        # Frame principal para as matrizes (será preenchido por atualizar_grade)
        self.frame_matriz = ttk.Frame(self, padding=10)
        self.frame_matriz.pack(fill=tk.BOTH, expand=True)

        # Frames internos (serão destruídos e recriados)
        self.frame_A = None
        self.frame_B = None

        # Frame para o botão de calcular (específico de cada solver)
        self.frame_botoes = ttk.Frame(self, padding=10)
        self.frame_botoes.pack(fill=tk.X)

        # Frame para os resultados
        frame_resultados = ttk.Frame(self, padding=10)
        frame_resultados.pack(fill=tk.BOTH, expand=True)
        ttk.Label(frame_resultados, text="Resultados:").pack(anchor=tk.W)
        self.text_resultado = ScrolledText(frame_resultados, height=10, font=("Courier New", 10))
        self.text_resultado.pack(fill=tk.BOTH, expand=True)

    def atualizar_grade(self, dados_iniciais=None):
        """
        Destrói e recria a grade de entradas com base no tamanho N.
        """
        try:
            n = int(self.entry_n.get())
            if n <= 0 or n > 10:
                messagebox.showwarning("Tamanho Inválido", "Por favor, insira um N entre 1 e 10.")
                return
            self.n = n
        except ValueError:
            messagebox.showerror("Erro", "Tamanho N inválido.")
            return

        # Limpar frames antigos
        if self.frame_A:
            self.frame_A.destroy()
        if self.frame_B:
            self.frame_B.destroy()

        self.entries_A = []
        self.entries_B = []

        # Criar novos frames
        self.frame_A = ttk.LabelFrame(self.frame_matriz, text=f"Matriz A ({n}x{n})")
        self.frame_A.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.frame_B = ttk.LabelFrame(self.frame_matriz, text=f"Vetor B ({n}x1)")
        self.frame_B.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)

        # Popular Matriz A
        for i in range(n):
            linha_entries = []
            for j in range(n):
                entry = ttk.Entry(self.frame_A, width=8)
                if dados_iniciais:
                    entry.insert(0, str(dados_iniciais["A"][i][j]))
                entry.grid(row=i, column=j, padx=3, pady=3)
                linha_entries.append(entry)
            self.entries_A.append(linha_entries)

        # Popular Vetor B
        for i in range(n):
            entry = ttk.Entry(self.frame_B, width=8)
            if dados_iniciais:
                entry.insert(0, str(dados_iniciais["B"][i]))
            entry.grid(row=i, column=0, padx=3, pady=3)
            self.entries_B.append(entry)

    def ler_dados(self):
        """
        Lê os dados das grades de entrada e os retorna como arrays NumPy.
        """
        if self.n == 0:
            messagebox.showerror("Erro", "Grade não foi criada. Insira N e clique em 'Criar/Atualizar'.")
            return None, None

        try:
            A = np.zeros((self.n, self.n))
            B = np.zeros(self.n)

            for i in range(self.n):
                for j in range(self.n):
                    A[i, j] = float(self.entries_A[i][j].get())

            for i in range(self.n):
                B[i] = float(self.entries_B[i].get())

            return A, B

        except ValueError:
            messagebox.showerror("Erro de Entrada", "Entrada inválida. Verifique se todos os campos são números.")
            return None, None

    def exibir_resultado(self, texto):
        self.text_resultado.delete(1.0, tk.END)
        self.text_resultado.insert(tk.END, texto)


# --- Janela Específica: Método Direto (Gauss) ---

class JanelaGauss(JanelaSolver):
    def __init__(self, master):
        super().__init__(master, "Calculadora: Método Direto (Gauss)")

        # Botão específico
        btn_calc = ttk.Button(self.frame_botoes, text="Calcular (Método Direto)", command=self.resolver)
        btn_calc.pack()

        # Pré-preenche com o problema das Minas
        self.entry_n.insert(0, "3")
        self.dados_minas = {
            "A": [[0.55, 0.25, 0.25], [0.30, 0.45, 0.20], [0.15, 0.30, 0.55]],
            "B": [4800, 5800, 5700]
        }
        self.atualizar_grade(dados_iniciais=self.dados_minas)

    def resolver(self):
        A, B = self.ler_dados()
        if A is None:
            return

        try:
            solucao = np.linalg.solve(A, B)

            resultado_txt = "Solução (Vetor X):\n\n"
            for i in range(self.n):
                resultado_txt += f"  x[{i + 1}] = {solucao[i]:.6f}\n"

            self.exibir_resultado(resultado_txt)

        except np.linalg.LinAlgError:
            messagebox.showerror("Erro de Cálculo", "Matriz singular. O sistema não possui solução única.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")


# --- Janela Específica: Método Iterativo (Gauss-Seidel) ---

class JanelaGaussSeidel(JanelaSolver):
    def __init__(self, master):
        super().__init__(master, "Calculadora: Método Iterativo (Gauss-Seidel)")

        # Controles extras para tolerância e iterações
        frame_extras = ttk.Frame(self.frame_botoes)
        frame_extras.pack(side=tk.LEFT, padx=10)

        ttk.Label(frame_extras, text="Tolerância (ex: 1e-4):").grid(row=0, column=0, sticky=tk.W)
        self.entry_tol = ttk.Entry(frame_extras, width=10)
        self.entry_tol.insert(0, "0.0001")
        self.entry_tol.grid(row=0, column=1, padx=5)

        ttk.Label(frame_extras, text="Max. Iterações:").grid(row=1, column=0, sticky=tk.W)
        self.entry_max_iter = ttk.Entry(frame_extras, width=10)
        self.entry_max_iter.insert(0, "1000")
        self.entry_max_iter.grid(row=1, column=1, padx=5)

        # Botão específico
        btn_calc = ttk.Button(self.frame_botoes, text="Calcular (Gauss-Seidel)", command=self.resolver)
        btn_calc.pack(side=tk.LEFT, padx=20)

        # Começa com N=3, mas em branco
        self.entry_n.insert(0, "3")
        self.atualizar_grade()

    def resolver(self):
        A, B = self.ler_dados()
        if A is None:
            return

        try:
            tol = float(self.entry_tol.get())
            max_iter = int(self.entry_max_iter.get())
        except ValueError:
            messagebox.showerror("Erro", "Tolerância ou Máx. Iterações inválidos.")
            return

        # Verificação crucial para Gauss-Seidel: Divisão por zero
        if np.any(np.diag(A) == 0):
            messagebox.showerror("Erro de Matriz",
                                 "Método de Gauss-Seidel não pode ser aplicado.\n"
                                 "A matriz possui '0' na diagonal principal.\n"
                                 "Reordene as equações (pivoteamento).")
            return

        try:
            solucao, iteracoes = gauss_seidel(A, B, tol, max_iter)

            resultado_txt = f"Convergência alcançada em {iteracoes} iterações.\n"
            if iteracoes == max_iter:
                resultado_txt = f"Atenção: Máximo de {iteracoes} iterações atingido.\n"
                resultado_txt += "A solução pode não ter convergido para a tolerância desejada.\n"

            resultado_txt += "\nSolução (Vetor X):\n\n"
            for i in range(self.n):
                resultado_txt += f"  x[{i + 1}] = {solucao[i]:.6f}\n"

            self.exibir_resultado(resultado_txt)

        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro no cálculo: {e}")


# --- Aplicação Principal (Menu) ---

class AppPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Solucionador de Sistemas Lineares")
        self.geometry("450x200")

        style = ttk.Style(self)
        style.configure("TButton", font=("Arial", 12), padding=15)

        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="Selecione o Método de Resolução:",
                  font=("Arial", 14)).pack(pady=10)

        btn_gauss = ttk.Button(main_frame,
                               text="1. Método Direto (Gauss)",
                               command=self.abrir_gauss)
        btn_gauss.pack(fill=tk.X, pady=5)

        btn_seidel = ttk.Button(main_frame,
                                text="2. Método Iterativo (Gauss-Seidel)",
                                command=self.abrir_gauss_seidel)
        btn_seidel.pack(fill=tk.X, pady=5)

    def abrir_gauss(self):
        # Cria uma nova janela (Toplevel) para o solver de Gauss
        JanelaGauss(self)

    def abrir_gauss_seidel(self):
        # Cria uma nova janela (Toplevel) para o solver de Gauss-Seidel
        JanelaGaussSeidel(self)


# --- Ponto de entrada principal para rodar o app ---
if __name__ == "__main__":
    app = AppPrincipal()
    app.mainloop()