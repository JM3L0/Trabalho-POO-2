import tkinter as tk
import models as md
import services as sv
import util

class InterfaceHotel:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Sistema de Gerenciamento de Hotel")
        self.raiz.geometry("600x400")
        self.raiz.configure(bg='#F0F0F0')

        # Cores
        self.cores = {'bg': '#F0F0F0',
                      'btn': '#4CAF50',
                      'perigo': '#F44336', 
                      'texto': '#333333',
                      'sucesso': '#00FF00',
                      'erro': '#FF0000'}

        # Serviços
        self.sistema = sv.Sistema()
        self.checkin_servico = sv.CheckIn()
        self.checkout_servico = sv.CheckOut()
        self.gerente = md.Gerente("GERENTE GERAL", "00000000000", "321")
        
        # Funcionários padrão
        for nome, cpf in [("FUNCIONARIO P", "11111111111"), ("LUIS", "22222222222"), ("MARIA", "33333333333"), ("ANA", "44444444444"), ("SEU ZÉ", "55555555555")]:
            self.gerente.adicionar_funcionario(nome, cpf, "123")

        self.usuario_atual = None
        self.rotulo_mensagem = None
        self.mostrar_menu_inicial()

    # Limpar frame, se necessário
    def limpar_frame(self):
        for widget in self.raiz.winfo_children():
            widget.destroy()
        self.rotulo_mensagem = None

    # Método para mostrar mensagens de sucesso ou erro
    def mostrar_mensagem(self, texto, tipo_msg, duracao=3000):
        if self.rotulo_mensagem: self.rotulo_mensagem.destroy()
        cor = self.cores['sucesso'] if tipo_msg == 'sucesso' else self.cores['erro']
        self.rotulo_mensagem = tk.Label(self.raiz, text=texto, font=("Arial", 12), bg=self.cores['bg'], fg=cor)
        self.rotulo_mensagem.pack(pady=10)
        self.raiz.after(duracao, lambda: self.rotulo_mensagem.destroy() if self.rotulo_mensagem else None)

    # Métodos para criar diferentes telas, como menus, formulários e listas
    def criar_widgets(self, titulo, itens):
        self.limpar_frame()
        self.raiz.geometry("600x400")
        tk.Label(self.raiz, text=titulo, font=("Arial", 16, "bold"), bg=self.cores['bg'], fg=self.cores['texto']).pack(pady=20)
        
        for item in itens:
            if len(item) == 2:  # Item de menu
                texto, comando = item
                bg = self.cores['btn']
            else:  # Botão com cor
                texto, comando, cor = item
                bg = self.cores[cor]
            
            tk.Button(self.raiz, text=texto, command=comando, bg=bg, fg="white", font=("Arial", 12)).pack(pady=5, padx=20, fill="x")

    # Métodos para criar formulários e listas, permitindo a entrada de dados e exibição de informações
    def criar_formulario(self, titulo, campos, funcao_enviar, funcao_voltar):
        self.limpar_frame()
        self.raiz.geometry("600x400")
        tk.Label(self.raiz, text=titulo, font=("Arial", 16, "bold"), bg=self.cores['bg'], fg=self.cores['texto']).pack(pady=20)

        entradas = {}
        for nome_campo, tipo_campo in campos:
            tk.Label(self.raiz, text=f"{nome_campo}:", bg=self.cores['bg'], font=("Arial", 12)).pack(pady=5)
            mostrar = "*" if tipo_campo == "senha" else None
            entrada = tk.Entry(self.raiz, font=("Arial", 12), show=mostrar)
            entrada.pack(pady=5, padx=20)
            entradas[nome_campo.lower().replace(" ", "_").replace("(", "").replace(")", "")] = entrada

        tk.Button(self.raiz, text="Confirmar", command=lambda: funcao_enviar(entradas), bg=self.cores['btn'], fg="white", font=("Arial", 12)).pack(pady=10)
        tk.Button(self.raiz, text="Voltar", command=funcao_voltar, bg=self.cores['perigo'], fg="white", font=("Arial", 12)).pack(pady=5)

    # Método para criar uma lista de itens
    def criar_lista(self, titulo, dados, funcao_voltar, funcao_formatar=None):
        self.limpar_frame()
        altura = max(400, 100 + len(dados) * 60)
        self.raiz.geometry(f"600x{altura}")
        tk.Label(self.raiz, text=titulo, font=("Arial", 16, "bold"), bg=self.cores['bg'], fg=self.cores['texto']).pack(pady=20)

        if not dados:
            tk.Label(self.raiz, text="Nenhum item encontrado.", bg=self.cores['bg'], fg=self.cores['erro'], font=("Arial", 12)).pack(pady=10)
        else:
            for item in dados:
                texto = funcao_formatar(item) if funcao_formatar else str(item)
                tk.Label(self.raiz, text=texto, bg=self.cores['bg'], font=("Arial", 12), justify="left").pack(pady=5, anchor="w", padx=20)

        tk.Button(self.raiz, text="Voltar", command=funcao_voltar, bg=self.cores['perigo'], fg="white", font=("Arial", 12)).pack(pady=10)

    # Métodos para mostrar diferentes telas do sistema, como menu inicial, login de gerente e funcionário, e menus específicos
    def mostrar_menu_inicial(self):
        self.criar_widgets("Sistema de Hotel", [
            ("Login como Gerente", self.mostrar_login_gerente),
            ("Login como Funcionário", self.mostrar_login_funcionario),
            ("Sair", self.raiz.quit, 'perigo')
        ])

    # Método para mostrar o login do gerente
    def mostrar_login_gerente(self):
        def tentar_login(entradas):
            senha = entradas['senha'].get()
            if len(senha) < 3:
                self.mostrar_mensagem("Senha inválida. Deve ter pelo menos 3 caracteres.", 'erro')
                return
            if self.sistema.login(self.gerente, senha):
                self.usuario_atual = self.gerente
                self.mostrar_mensagem("Login realizado com sucesso como Gerente!", 'sucesso')
                self.raiz.after(2000, self.mostrar_menu_gerente)
            else:
                self.mostrar_mensagem("Senha incorreta!", 'erro')

        self.criar_formulario("Login Gerente", [("Senha", "senha")], tentar_login, self.mostrar_menu_inicial)

    # Método para mostrar o login do funcionário
    def mostrar_login_funcionario(self):
        def tentar_login(entradas):
            cpf, senha = entradas['cpf'].get(), entradas['senha'].get()
            if not (cpf.isdigit() and len(cpf) == 11):
                self.mostrar_mensagem("CPF inválido. Deve ser um número de 11 caracteres.", 'erro')
                return
            if len(senha) < 3:
                self.mostrar_mensagem("Senha inválida. Deve ter pelo menos 3 caracteres.", 'erro')
                return
            funcionario = util.existe_funcionario(self.gerente.funcionarios, cpf)
            if funcionario and self.sistema.login(funcionario, senha):
                self.usuario_atual = funcionario
                self.mostrar_mensagem(f"Login realizado com sucesso como {funcionario.nome}!", 'sucesso')
                self.raiz.after(2000, self.mostrar_menu_funcionario)
            else:
                self.mostrar_mensagem("Funcionário não encontrado ou senha incorreta!", 'erro')

        self.criar_formulario("Login Funcionário", [("CPF", "texto"), ("Senha", "senha")], tentar_login, self.mostrar_menu_inicial)

    # Métodos para mostrar os menus do gerente e do funcionário
    def mostrar_menu_gerente(self):
        self.criar_widgets("Menu do Gerente", [
            ("Adicionar Funcionário", self.adicionar_funcionario),
            ("Remover Funcionário", self.remover_funcionario),
            ("Listar Funcionários", self.listar_funcionarios),
            ("Imprimir Histórico", self.mostrar_historico_gerente),
            ("Logout", self.mostrar_menu_inicial, 'perigo')
        ])

    # Método para mostrar o menu do funcionário
    def mostrar_menu_funcionario(self):
        self.criar_widgets("Menu do Funcionário", [
            ("Registrar Hóspede (Check-in)", self.registrar_hospede),
            ("Listar Hóspedes", self.listar_hospedes),
            ("Listar Quartos Disponíveis", self.listar_quartos),
            ("Remover Hóspede (Check-out)", self.remover_hospede),
            ("Imprimir Histórico", self.mostrar_historico_funcionario),
            ("Logout", self.mostrar_menu_inicial, 'perigo')
        ])

    # Métodos para adicionar, remover e listar funcionários, além de imprimir o histórico do gerente
    def adicionar_funcionario(self):
        def enviar(entradas):
            nome, cpf, senha = entradas['nome'].get().upper(), entradas['cpf'].get(), entradas['senha'].get()
            if not all([nome, cpf, senha]):
                self.mostrar_mensagem("Todos os campos são obrigatórios!", 'erro')
                return
            if self.gerente.adicionar_funcionario(nome, cpf, senha):
                self.mostrar_mensagem(f"Funcionário {nome} adicionado com sucesso.", 'sucesso')
                self.raiz.after(2000, self.mostrar_menu_gerente)
            else:
                self.mostrar_mensagem("Falha ao adicionar funcionário. Verifique o CPF.", 'erro')

        self.criar_formulario("Adicionar Funcionário", [("Nome", "texto"), ("CPF", "texto"), ("Senha", "senha")], enviar, self.mostrar_menu_gerente)

    # Métodos para remover funcionários, listar funcionários e imprimir o histórico do gerente
    def remover_funcionario(self):
        def enviar(entradas):
            cpf = entradas['cpf'].get()
            if self.gerente.remover_funcionario(cpf):
                self.mostrar_mensagem("Funcionário removido com sucesso.", 'sucesso')
                self.raiz.after(2000, self.mostrar_menu_gerente)
            else:
                self.mostrar_mensagem("Nenhum funcionário com esse CPF foi encontrado.", 'erro')

        self.criar_formulario("Remover Funcionário", [("CPF", "texto")], enviar, self.mostrar_menu_gerente)

    # Método para listar funcionários
    def listar_funcionarios(self):
        dados = [(cpf, func) for cpf, func in self.gerente.funcionarios.items()]
        self.criar_lista("Lista de Funcionários", dados, self.mostrar_menu_gerente, lambda x: f"Nome: {x[1].nome}\n{util.imprimir_cpf(x[0])}")

    # Método para mostrar o histórico do gerente
    def mostrar_historico_gerente(self):
        self.criar_lista("Histórico do Gerente", self.gerente.historico, self.mostrar_menu_gerente)

    # Métodos para registrar
    def registrar_hospede(self):
        def enviar(entradas):
            nome, cpf = entradas['nome'].get().upper(), entradas['cpf'].get()
            try:
                quarto = int(entradas['quarto_1_a_10'].get())
                if quarto not in range(1, 11):
                    self.mostrar_mensagem("Número do quarto inválido. Deve estar entre 1 e 10.", 'erro')
                    return
            except ValueError:
                self.mostrar_mensagem("O número do quarto deve ser um número inteiro.", 'erro')
                return
            hospede = md.Hospede(nome, cpf, quarto)
            if self.usuario_atual.registrar_hospede(self.checkin_servico, hospede):
                self.mostrar_mensagem(f"Hóspede {nome} registrado no quarto {quarto}.", 'sucesso')
                self.raiz.after(2000, self.mostrar_menu_funcionario)
            else:
                self.mostrar_mensagem("Falha ao registrar hóspede. Verifique CPF ou quarto.", 'erro')

        self.criar_formulario("Registrar Hóspede", [("Nome", "texto"), ("CPF", "texto"), ("Quarto (1 a 10)", "texto")], enviar, self.mostrar_menu_funcionario)

    # Métodos para listar hóspedes
    def listar_hospedes(self):
        dados = list(self.checkin_servico.hospedes.values())
        self.criar_lista("Lista de Hóspedes", dados, self.mostrar_menu_funcionario, lambda h: f"Nome: {h.nome}\n{util.imprimir_cpf(h.cpf)}\nQuarto: {h.quarto}")

    # Método para listar quartos disponíveis
    def listar_quartos(self):
        self.limpar_frame()
        self.raiz.geometry("600x400")
        tk.Label(self.raiz, text="Quartos Disponíveis", font=("Arial", 16, "bold"), bg=self.cores['bg'], fg=self.cores['texto']).pack(pady=20)
        quartos = util.ordenar_quartos(self.checkin_servico.quartos_disponiveis)
        tk.Label(self.raiz, text=f"Quartos disponíveis: {quartos}", bg=self.cores['bg'], font=("Arial", 12)).pack(pady=10)
        tk.Button(self.raiz, text="Voltar", command=self.mostrar_menu_funcionario, bg=self.cores['perigo'], fg="white", font=("Arial", 12)).pack(pady=10)

    # Método para remover hóspedes
    def remover_hospede(self):
        def enviar(entradas):
            cpf = entradas['cpf'].get()
            nome_hospede = self.checkin_servico.hospedes.get(cpf, md.Hospede("", "", 0)).nome
            if self.checkout_servico.remover_hospede(cpf, self.checkin_servico, self.usuario_atual, nome_hospede):
                self.mostrar_mensagem(f"Hóspede com CPF {cpf} removido com sucesso.", 'sucesso')
                self.raiz.after(2000, self.mostrar_menu_funcionario)
            else:
                self.mostrar_mensagem("Falha ao remover hóspede. Verifique o CPF.", 'erro')

        self.criar_formulario("Remover Hóspede (Check-out)", [("CPF", "texto")], enviar, self.mostrar_menu_funcionario)

    # Método para mostrar o histórico do funcionário
    def mostrar_historico_funcionario(self):
        self.criar_lista(f"Histórico de {self.usuario_atual.nome}", self.usuario_atual.historico, self.mostrar_menu_funcionario)

# Método para iniciar a interface
if __name__ == "__main__":
    raiz = tk.Tk()
    app = InterfaceHotel(raiz)
    raiz.mainloop()