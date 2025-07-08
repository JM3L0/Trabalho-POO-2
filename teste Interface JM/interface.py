import tkinter as tk
from tkinter import ttk
import models as md
import services as sv
import util

# Cores para a interface (inspiradas no estilo do terminal)
RED = '#FF0000'
GREEN = '#00FF00'
BG_COLOR = '#F0F0F0'
BUTTON_COLOR = '#4CAF50'
TEXT_COLOR = '#333333'

class HotelGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gerenciamento de Hotel")
        self.root.geometry("600x400")
        self.root.configure(bg=BG_COLOR)

        self.sistema = sv.Sistema()
        self.checkin = sv.CheckIn()
        self.checkout = sv.CheckOut()
        self.gerente = md.Gerente("GERENTE GERAL", "00000000000", "321")
        self.instancia_funcionarios()

        self.current_user = None
        self.message_label = None  # Para mensagens temporárias
        self.show_initial_menu()

    def instancia_funcionarios(self):
        """Inicializa funcionários padrão, como no main.py."""
        self.gerente.adicionar_funcionario("FUNCIONARIO P", "11111111111", "123")
        self.gerente.adicionar_funcionario("LUIS", "22222222222", "123")
        self.gerente.adicionar_funcionario("MARIA", "33333333333", "123")
        self.gerente.adicionar_funcionario("ANA", "44444444444", "123")
        self.gerente.adicionar_funcionario("SEU ZÉ", "55555555555", "123")

    def clear_frame(self):
        """Limpa o conteúdo da janela para exibir uma nova tela."""
        for widget in self.root.winfo_children():
            widget.destroy()
        self.message_label = None

    def show_message(self, text, color, duration=3000):
        """Exibe uma mensagem temporária na janela atual."""
        if self.message_label:
            self.message_label.destroy()
        self.message_label = tk.Label(self.root, text=text, font=("Arial", 12), bg=BG_COLOR, fg=color)
        self.message_label.pack(pady=10)
        self.root.after(duration, lambda: self.message_label.destroy() if self.message_label else None)

    def show_initial_menu(self):
        """Exibe o menu inicial."""
        self.clear_frame()
        self.root.geometry("600x400")
        self.root.configure(bg=BG_COLOR)

        tk.Label(self.root, text="Sistema de Hotel", font=("Arial", 20, "bold"), bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=20)

        tk.Button(self.root, text="Login como Gerente", command=self.show_gerente_login, bg=BUTTON_COLOR, fg="white", font=("Arial", 12)).pack(pady=10, padx=20, fill="x")
        tk.Button(self.root, text="Login como Funcionário", command=self.show_funcionario_login, bg=BUTTON_COLOR, fg="white", font=("Arial", 12)).pack(pady=10, padx=20, fill="x")
        tk.Button(self.root, text="Sair", command=self.root.quit, bg="#F44336", fg="white", font=("Arial", 12)).pack(pady=10, padx=20, fill="x")

    def show_gerente_login(self):
        """Exibe a tela de login do gerente."""
        self.clear_frame()
        self.root.geometry("600x400")
        tk.Label(self.root, text="Login Gerente", font=("Arial", 16, "bold"), bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=20)

        tk.Label(self.root, text="Senha:", bg=BG_COLOR, font=("Arial", 12)).pack(pady=5)
        senha_entry = tk.Entry(self.root, show="*", font=("Arial", 12))
        senha_entry.pack(pady=5, padx=20)

        def try_login():
            senha = senha_entry.get()
            if not senha or len(senha) < 3:
                self.show_message("Senha inválida. Deve ter pelo menos 3 caracteres.", RED)
                return
            if self.sistema.login(self.gerente, senha):
                self.current_user = self.gerente
                self.show_message("Login realizado com sucesso como Gerente!", GREEN)
                self.root.after(2000, self.show_gerente_menu)
            else:
                self.show_message("Senha incorreta!", RED)

        tk.Button(self.root, text="Entrar", command=try_login, bg=BUTTON_COLOR, fg="white", font=("Arial", 12)).pack(pady=10)
        tk.Button(self.root, text="Voltar", command=self.show_initial_menu, bg="#F44336", fg="white", font=("Arial", 12)).pack(pady=5)

    def show_funcionario_login(self):
        """Exibe a tela de login do funcionário."""
        self.clear_frame()
        self.root.geometry("600x400")
        tk.Label(self.root, text="Login Funcionário", font=("Arial", 16, "bold"), bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=20)

        tk.Label(self.root, text="CPF:", bg=BG_COLOR, font=("Arial", 12)).pack(pady=5)
        cpf_entry = tk.Entry(self.root, font=("Arial", 12))
        cpf_entry.pack(pady=5, padx=20)

        tk.Label(self.root, text="Senha:", bg=BG_COLOR, font=("Arial", 12)).pack(pady=5)
        senha_entry = tk.Entry(self.root, show="*", font=("Arial", 12))
        senha_entry.pack(pady=5, padx=20)

        def try_login():
            cpf = cpf_entry.get()
            senha = senha_entry.get()
            if not (cpf.isdigit() and len(cpf) == 11):
                self.show_message("CPF inválido. Deve ser um número de 11 caracteres.", RED)
                return
            if not senha or len(senha) < 3:
                self.show_message("Senha inválida. Deve ter pelo menos 3 caracteres.", RED)
                return
            funcionario = util.existe_funcionario(self.gerente.funcionarios, cpf)
            if funcionario and self.sistema.login(funcionario, senha):
                self.current_user = funcionario
                self.show_message(f"Login realizado com sucesso como {funcionario.nome}!", GREEN)
                self.root.after(2000, self.show_funcionario_menu)
            else:
                self.show_message("Funcionário não encontrado ou senha incorreta!", RED)

        tk.Button(self.root, text="Entrar", command=try_login, bg=BUTTON_COLOR, fg="white", font=("Arial", 12)).pack(pady=10)
        tk.Button(self.root, text="Voltar", command=self.show_initial_menu, bg="#F44336", fg="white", font=("Arial", 12)).pack(pady=5)

    def show_gerente_menu(self):
        """Exibe o menu do gerente."""
        self.clear_frame()
        self.root.geometry("600x400")
        tk.Label(self.root, text="Menu do Gerente", font=("Arial", 16, "bold"), bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=20)

        tk.Button(self.root, text="Adicionar Funcionário", command=self.add_funcionario, bg=BUTTON_COLOR, fg="white", font=("Arial", 12)).pack(pady=5, padx=20, fill="x")
        tk.Button(self.root, text="Remover Funcionário", command=self.remove_funcionario, bg=BUTTON_COLOR, fg="white", font=("Arial", 12)).pack(pady=5, padx=20, fill="x")
        tk.Button(self.root, text="Listar Funcionários", command=self.list_funcionarios, bg=BUTTON_COLOR, fg="white", font=("Arial", 12)).pack(pady=5, padx=20, fill="x")
        tk.Button(self.root, text="Imprimir Histórico", command=self.show_historico_gerente, bg=BUTTON_COLOR, fg="white", font=("Arial", 12)).pack(pady=5, padx=20, fill="x")
        tk.Button(self.root, text="Logout", command=self.show_initial_menu, bg="#F44336", fg="white", font=("Arial", 12)).pack(pady=5, padx=20, fill="x")

    def show_funcionario_menu(self):
        """Exibe o menu do funcionário."""
        self.clear_frame()
        self.root.geometry("600x400")
        tk.Label(self.root, text="Menu do Funcionário", font=("Arial", 16, "bold"), bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=20)

        tk.Button(self.root, text="Registrar Hóspede (Check-in)", command=self.registrar_hospede, bg=BUTTON_COLOR, fg="white", font=("Arial", 12)).pack(pady=5, padx=20, fill="x")
        tk.Button(self.root, text="Listar Hóspedes", command=self.list_hospedes, bg=BUTTON_COLOR, fg="white", font=("Arial", 12)).pack(pady=5, padx=20, fill="x")
        tk.Button(self.root, text="Listar Quartos Disponíveis", command=self.list_quartos, bg=BUTTON_COLOR, fg="white", font=("Arial", 12)).pack(pady=5, padx=20, fill="x")
        tk.Button(self.root, text="Remover Hóspede (Check-out)", command=self.remover_hospede, bg=BUTTON_COLOR, fg="white", font=("Arial", 12)).pack(pady=5, padx=20, fill="x")
        tk.Button(self.root, text="Imprimir Histórico", command=self.show_historico_funcionario, bg=BUTTON_COLOR, fg="white", font=("Arial", 12)).pack(pady=5, padx=20, fill="x")
        tk.Button(self.root, text="Logout", command=self.show_initial_menu, bg="#F44336", fg="white", font=("Arial", 12)).pack(pady=5, padx=20, fill="x")

    def add_funcionario(self):
        """Tela para adicionar funcionário."""
        self.clear_frame()
        self.root.geometry("600x400")
        tk.Label(self.root, text="Adicionar Funcionário", font=("Arial", 16, "bold"), bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=20)

        tk.Label(self.root, text="Nome:", bg=BG_COLOR, font=("Arial", 12)).pack(pady=5)
        nome_entry = tk.Entry(self.root, font=("Arial", 12))
        nome_entry.pack(pady=5, padx=20)

        tk.Label(self.root, text="CPF:", bg=BG_COLOR, font=("Arial", 12)).pack(pady=5)
        cpf_entry = tk.Entry(self.root, font=("Arial", 12))
        cpf_entry.pack(pady=5, padx=20)

        tk.Label(self.root, text="Senha:", bg=BG_COLOR, font=("Arial", 12)).pack(pady=5)
        senha_entry = tk.Entry(self.root, show="*", font=("Arial", 12))
        senha_entry.pack(pady=5, padx=20)

        def submit():
            nome = nome_entry.get().upper()
            cpf = cpf_entry.get()
            senha = senha_entry.get()
            if not nome or not cpf or not senha:
                self.show_message("Todos os campos são obrigatórios!", RED)
                return
            if self.gerente.adicionar_funcionario(nome, cpf, senha):
                self.show_message(f"Funcionário {nome} adicionado com sucesso.", GREEN)
                self.root.after(2000, self.show_gerente_menu)
            else:
                self.show_message("Falha ao adicionar funcionário. Verifique o CPF.", RED)

        tk.Button(self.root, text="Adicionar", command=submit, bg=BUTTON_COLOR, fg="white", font=("Arial", 12)).pack(pady=10)
        tk.Button(self.root, text="Voltar", command=self.show_gerente_menu, bg="#F44336", fg="white", font=("Arial", 12)).pack(pady=5)

    def remove_funcionario(self):
        """Tela para remover funcionário."""
        self.clear_frame()
        self.root.geometry("600x400")
        tk.Label(self.root, text="Remover Funcionário", font=("Arial", 16, "bold"), bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=20)

        tk.Label(self.root, text="CPF:", bg=BG_COLOR, font=("Arial", 12)).pack(pady=5)
        cpf_entry = tk.Entry(self.root, font=("Arial", 12))
        cpf_entry.pack(pady=5, padx=20)

        def submit():
            cpf = cpf_entry.get()
            if self.gerente.remover_funcionario(cpf):
                self.show_message("Funcionário removido com sucesso.", GREEN)
                self.root.after(2000, self.show_gerente_menu)
            else:
                self.show_message("Nenhum funcionário com esse CPF foi encontrado.", RED)

        tk.Button(self.root, text="Remover", command=submit, bg=BUTTON_COLOR, fg="white", font=("Arial", 12)).pack(pady=10)
        tk.Button(self.root, text="Voltar", command=self.show_gerente_menu, bg="#F44336", fg="white", font=("Arial", 12)).pack(pady=5)

    def list_funcionarios(self):
        """Exibe a lista de funcionários sem rolagem."""
        self.clear_frame()
        # Calcula a altura da janela com base no número de funcionários
        num_funcionarios = len(self.gerente.funcionarios)
        altura = 100 + num_funcionarios * 60  # 60px por funcionário + margem
        self.root.geometry(f"600x{max(400, altura)}")
        tk.Label(self.root, text="Lista de Funcionários", font=("Arial", 16, "bold"), bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=20)

        if not self.gerente.funcionarios:
            tk.Label(self.root, text="Nenhum funcionário cadastrado.", bg=BG_COLOR, fg=RED, font=("Arial", 12)).pack(pady=10)
        else:
            for cpf, funcionario in self.gerente.funcionarios.items():
                tk.Label(self.root, text=f"Nome: {funcionario.nome}\n{util.imprimir_cpf(cpf)}", bg=BG_COLOR, font=("Arial", 12), justify="left").pack(pady=5, anchor="w", padx=20)

        tk.Button(self.root, text="Voltar", command=self.show_gerente_menu, bg="#F44336", fg="white", font=("Arial", 12)).pack(pady=10)

    def show_historico_gerente(self):
        """Exibe o histórico do gerente sem rolagem."""
        self.clear_frame()
        # Calcula a altura da janela com base no número de ações
        num_acoes = len(self.gerente.historico)
        altura = 100 + num_acoes * 30  # 30px por ação + margem
        self.root.geometry(f"600x{max(400, altura)}")
        tk.Label(self.root, text="Histórico do Gerente", font=("Arial", 16, "bold"), bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=20)

        if not self.gerente.historico:
            tk.Label(self.root, text="Nenhuma ação realizada.", bg=BG_COLOR, fg=RED, font=("Arial", 12)).pack(pady=10)
        else:
            for acao in self.gerente.historico:
                tk.Label(self.root, text=acao, bg=BG_COLOR, font=("Arial", 12), justify="left").pack(pady=2, anchor="w", padx=20)

        tk.Button(self.root, text="Voltar", command=self.show_gerente_menu, bg="#F44336", fg="white", font=("Arial", 12)).pack(pady=10)

    def registrar_hospede(self):
        """Tela para registrar hóspede."""
        self.clear_frame()
        self.root.geometry("600x400")
        tk.Label(self.root, text="Registrar Hóspede", font=("Arial", 16, "bold"), bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=20)

        tk.Label(self.root, text="Nome:", bg=BG_COLOR, font=("Arial", 12)).pack(pady=5)
        nome_entry = tk.Entry(self.root, font=("Arial", 12))
        nome_entry.pack(pady=5, padx=20)

        tk.Label(self.root, text="CPF:", bg=BG_COLOR, font=("Arial", 12)).pack(pady=5)
        cpf_entry = tk.Entry(self.root, font=("Arial", 12))
        cpf_entry.pack(pady=5, padx=20)

        tk.Label(self.root, text="Quarto (1 a 10):", bg=BG_COLOR, font=("Arial", 12)).pack(pady=5)
        quarto_entry = tk.Entry(self.root, font=("Arial", 12))
        quarto_entry.pack(pady=5, padx=20)

        def submit():
            nome = nome_entry.get().upper()
            cpf = cpf_entry.get()
            try:
                quarto = int(quarto_entry.get())
                if quarto not in range(1, 11):
                    self.show_message("Número do quarto inválido. Deve estar entre 1 e 10.", RED)
                    return
            except ValueError:
                self.show_message("O número do quarto deve ser um número inteiro.", RED)
                return
            hospede = md.Hospede(nome, cpf, quarto)
            if self.current_user.registrar_hospede(self.checkin, hospede):
                self.show_message(f"Hóspede {nome} registrado no quarto {quarto}.", GREEN)
                self.root.after(2000, self.show_funcionario_menu)
            else:
                self.show_message("Falha ao registrar hóspede. Verifique CPF ou quarto.", RED)

        tk.Button(self.root, text="Registrar", command=submit, bg=BUTTON_COLOR, fg="white", font=("Arial", 12)).pack(pady=10)
        tk.Button(self.root, text="Voltar", command=self.show_funcionario_menu, bg="#F44336", fg="white", font=("Arial", 12)).pack(pady=5)

    def list_hospedes(self):
        """Exibe a lista de hóspedes sem rolagem."""
        self.clear_frame()
        # Calcula a altura da janela com base no número de hóspedes
        num_hospedes = len(self.checkin.hospedes)
        altura = 100 + num_hospedes * 80  # 80px por hóspede + margem
        self.root.geometry(f"600x{max(400, altura)}")
        tk.Label(self.root, text="Lista de Hóspedes", font=("Arial", 16, "bold"), bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=20)

        if not self.checkin.hospedes:
            tk.Label(self.root, text="Nenhum hóspede registrado.", bg=BG_COLOR, fg=RED, font=("Arial", 12)).pack(pady=10)
        else:
            for hospede in self.checkin.hospedes.values():
                tk.Label(self.root, text=f"Nome: {hospede.nome}\n{util.imprimir_cpf(hospede.cpf)}\nQuarto: {hospede.quarto}", bg=BG_COLOR, font=("Arial", 12), justify="left").pack(pady=5, anchor="w", padx=20)

        tk.Button(self.root, text="Voltar", command=self.show_funcionario_menu, bg="#F44336", fg="white", font=("Arial", 12)).pack(pady=10)

    def list_quartos(self):
        """Exibe a lista de quartos disponíveis sem rolagem."""
        self.clear_frame()
        self.root.geometry("600x400")
        tk.Label(self.root, text="Quartos Disponíveis", font=("Arial", 16, "bold"), bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=20)

        quartos = util.ordenar_quartos(self.checkin.quartos_disponiveis)
        tk.Label(self.root, text=f"Quartos disponíveis: {quartos}", bg=BG_COLOR, font=("Arial", 12)).pack(pady=10)

        tk.Button(self.root, text="Voltar", command=self.show_funcionario_menu, bg="#F44336", fg="white", font=("Arial", 12)).pack(pady=10)

    def remover_hospede(self):
        """Tela para remover hóspede (check-out)."""
        self.clear_frame()
        self.root.geometry("600x400")
        tk.Label(self.root, text="Remover Hóspede (Check-out)", font=("Arial", 16, "bold"), bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=20)

        tk.Label(self.root, text="CPF:", bg=BG_COLOR, font=("Arial", 12)).pack(pady=5)
        cpf_entry = tk.Entry(self.root, font=("Arial", 12))
        cpf_entry.pack(pady=5, padx=20)

        def submit():
            cpf = cpf_entry.get()
            nome = self.checkin.hospedes.get(cpf, md.Hospede("", "", 0)).nome
            if self.checkout.remover_hospede(cpf, self.checkin, self.current_user, nome):
                self.show_message(f"Hóspede com CPF {cpf} removido com sucesso.", GREEN)
                self.root.after(2000, self.show_funcionario_menu)
            else:
                self.show_message("Falha ao remover hóspede. Verifique o CPF.", RED)

        tk.Button(self.root, text="Remover", command=submit, bg=BUTTON_COLOR, fg="white", font=("Arial", 12)).pack(pady=10)
        tk.Button(self.root, text="Voltar", command=self.show_funcionario_menu, bg="#F44336", fg="white", font=("Arial", 12)).pack(pady=5)

    def show_historico_funcionario(self):
        """Exibe o histórico do funcionário sem rolagem."""
        self.clear_frame()
        # Calculando a altura da janela com base no número de ações
        num_acoes = len(self.current_user.historico)
        altura = 100 + num_acoes * 30  # 30px por ação + margem
        self.root.geometry(f"600x{max(400, altura)}")
        tk.Label(self.root, text=f"Histórico de {self.current_user.nome}", font=("Arial", 16, "bold"), bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=20)

        if not self.current_user.historico:
            tk.Label(self.root, text="Nenhuma ação realizada.", bg=BG_COLOR, fg=RED, font=("Arial", 12)).pack(pady=10)
        else:
            for acao in self.current_user.historico:
                tk.Label(self.root, text=acao, bg=BG_COLOR, font=("Arial", 12), justify="left").pack(pady=2, anchor="w", padx=20)

        tk.Button(self.root, text="Voltar", command=self.show_funcionario_menu, bg="#F44336", fg="white", font=("Arial", 12)).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = HotelGUI(root)
    root.mainloop()