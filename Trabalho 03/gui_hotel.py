import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import models as md
import services as sv
import util

class HotelGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Hotel")
        self.root.geometry("400x300")
        self.root.configure(bg='#f0f0f0')
        
        # Inicializar sistema
        self.sistema = sv.Sistema()
        self.checkin = sv.CheckIn()
        self.checkout = sv.CheckOut()
        
        # Criar gerente padrão
        self.gerente = md.Gerente("GERENTE GERAL", "00000000000", "321")
        self.instanciar_funcionarios()
        
        # Variáveis
        self.usuario_atual = None
        self.tipo_usuario = tk.StringVar(value="gerente")
        
        self.criar_tela_login()
        
    def instanciar_funcionarios(self):
        """Instancia funcionários padrão"""
        self.gerente.adicionar_funcionario("FUNCIONARIO P", "11111111111", "123")
        self.gerente.adicionar_funcionario("LUIS", "22222222222", "123")
        self.gerente.adicionar_funcionario("MARIA", "33333333333", "123")
        self.gerente.adicionar_funcionario("ANA", "44444444444", "123")
        self.gerente.adicionar_funcionario("SEU ZÉ", "55555555555", "123")
    
    def limpar_tela(self):
        """Remove todos os widgets da tela"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def criar_tela_login(self):
        """Cria a tela de login"""
        self.limpar_tela()
        self.root.geometry("400x300")
        
        # Título
        titulo = tk.Label(self.root, text="Sistema de Hotel", 
                         font=("Arial", 16, "bold"), bg='#f0f0f0')
        titulo.pack(pady=20)
        
        # Frame principal
        frame_main = tk.Frame(self.root, bg='#f0f0f0')
        frame_main.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Tipo de usuário
        tk.Label(frame_main, text="Tipo de Usuário:", 
                font=("Arial", 10), bg='#f0f0f0').pack(pady=5)
        
        frame_radio = tk.Frame(frame_main, bg='#f0f0f0')
        frame_radio.pack(pady=5)
        
        tk.Radiobutton(frame_radio, text="Gerente", variable=self.tipo_usuario, 
                      value="gerente", bg='#f0f0f0', command=self.atualizar_campos).pack(side='left', padx=10)
        tk.Radiobutton(frame_radio, text="Funcionário", variable=self.tipo_usuario, 
                      value="funcionario", bg='#f0f0f0', command=self.atualizar_campos).pack(side='left', padx=10)
        
        # Campo CPF (apenas para funcionário)
        self.label_cpf = tk.Label(frame_main, text="CPF:", 
                                 font=("Arial", 10), bg='#f0f0f0')
        self.entry_cpf = tk.Entry(frame_main, font=("Arial", 10), width=20)
        
        # Campo Senha
        tk.Label(frame_main, text="Senha:", 
                font=("Arial", 10), bg='#f0f0f0').pack(pady=(10,5))
        self.entry_senha = tk.Entry(frame_main, font=("Arial", 10), 
                                   width=20, show="*")
        self.entry_senha.pack(pady=5)
        
        # Botões
        frame_botoes = tk.Frame(frame_main, bg='#f0f0f0')
        frame_botoes.pack(pady=20)
        
        tk.Button(frame_botoes, text="Login", command=self.fazer_login,
                 bg='#4CAF50', fg='white', font=("Arial", 10), 
                 width=10).pack(side='left', padx=5)
        
        tk.Button(frame_botoes, text="Sair", command=self.root.quit,
                 bg='#f44336', fg='white', font=("Arial", 10), 
                 width=10).pack(side='left', padx=5)
        
        self.atualizar_campos()
    
    def atualizar_campos(self):
        """Atualiza visibilidade dos campos baseado no tipo de usuário"""
        if self.tipo_usuario.get() == "funcionario":
            self.label_cpf.pack(pady=(10,5))
            self.entry_cpf.pack(pady=5)
        else:
            self.label_cpf.pack_forget()
            self.entry_cpf.pack_forget()
    
    def fazer_login(self):
        """Processa o login do usuário"""
        senha = self.entry_senha.get()
        
        if len(senha) < 3:
            messagebox.showerror("Erro", "Senha deve ter pelo menos 3 caracteres!")
            return
        
        if self.tipo_usuario.get() == "gerente":
            if self.sistema.login(self.gerente, senha):
                self.usuario_atual = self.gerente
                self.criar_menu_gerente()
            else:
                messagebox.showerror("Erro", "Senha incorreta!")
        else:
            cpf = self.entry_cpf.get()
            if not cpf.isdigit() or len(cpf) != 11:
                messagebox.showerror("Erro", "CPF deve ter 11 dígitos!")
                return
            
            funcionario = util.existe_funcionario(self.gerente.funcionarios, cpf)
            if funcionario and self.sistema.login(funcionario, senha):
                self.usuario_atual = funcionario
                self.criar_menu_funcionario()
            else:
                if not funcionario:
                    messagebox.showerror("Erro", "Funcionário não encontrado!")
                else:
                    messagebox.showerror("Erro", "Senha incorreta!")
    
    def criar_menu_gerente(self):
        """Cria o menu do gerente"""
        self.limpar_tela()
        self.root.geometry("500x400")
        
        # Título
        titulo = tk.Label(self.root, text=f"Menu do Gerente - {self.usuario_atual.nome}", 
                         font=("Arial", 14, "bold"), bg='#f0f0f0')
        titulo.pack(pady=20)
        
        # Frame dos botões
        frame_botoes = tk.Frame(self.root, bg='#f0f0f0')
        frame_botoes.pack(expand=True, fill='both', padx=50, pady=20)
        
        botoes = [
            ("Adicionar Funcionário", self.adicionar_funcionario),
            ("Remover Funcionário", self.remover_funcionario),
            ("Listar Funcionários", self.listar_funcionarios),
            ("Imprimir Histórico", self.mostrar_historico_gerente),
            ("Logout", self.fazer_logout)
        ]
        
        for i, (texto, comando) in enumerate(botoes):
            cor = '#f44336' if texto == 'Logout' else '#2196F3'
            btn = tk.Button(frame_botoes, text=texto, command=comando,
                           bg=cor, fg='white', font=("Arial", 11), 
                           width=25, height=2)
            btn.pack(pady=10)
    
    def criar_menu_funcionario(self):
        """Cria o menu do funcionário"""
        self.limpar_tela()
        self.root.geometry("500x400")
        
        # Título
        titulo = tk.Label(self.root, text=f"Menu do Funcionário - {self.usuario_atual.nome}", 
                         font=("Arial", 14, "bold"), bg='#f0f0f0')
        titulo.pack(pady=20)
        
        # Frame dos botões
        frame_botoes = tk.Frame(self.root, bg='#f0f0f0')
        frame_botoes.pack(expand=True, fill='both', padx=50, pady=20)
        
        botoes = [
            ("Registrar Hóspede (Check-in)", self.registrar_hospede),
            ("Listar Hóspedes", self.listar_hospedes),
            ("Listar Quartos Disponíveis", self.listar_quartos_disponiveis),
            ("Remover Hóspede (Check-out)", self.remover_hospede),
            ("Imprimir Histórico", self.mostrar_historico_funcionario),
            ("Logout", self.fazer_logout)
        ]
        
        for i, (texto, comando) in enumerate(botoes):
            cor = '#f44336' if texto == 'Logout' else '#4CAF50'
            btn = tk.Button(frame_botoes, text=texto, command=comando,
                           bg=cor, fg='white', font=("Arial", 11), 
                           width=30, height=2)
            btn.pack(pady=8)
    
    def fazer_logout(self):
        """Faz logout e volta para tela de login"""
        self.usuario_atual = None
        self.criar_tela_login()
    
    # Métodos do Gerente
    def adicionar_funcionario(self):
        """Dialog para adicionar funcionário"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Adicionar Funcionário")
        dialog.geometry("350x250")
        dialog.configure(bg='#f0f0f0')
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Campos
        tk.Label(dialog, text="Nome:", bg='#f0f0f0').pack(pady=5)
        entry_nome = tk.Entry(dialog, width=30)
        entry_nome.pack(pady=5)
        
        tk.Label(dialog, text="CPF:", bg='#f0f0f0').pack(pady=5)
        entry_cpf = tk.Entry(dialog, width=30)
        entry_cpf.pack(pady=5)
        
        tk.Label(dialog, text="Senha:", bg='#f0f0f0').pack(pady=5)
        entry_senha = tk.Entry(dialog, width=30, show="*")
        entry_senha.pack(pady=5)
        
        def confirmar():
            nome = entry_nome.get().upper().strip()
            cpf = entry_cpf.get().strip()
            senha = entry_senha.get()
            
            if not nome:
                messagebox.showerror("Erro", "Nome não pode estar vazio!")
                return
            
            if not cpf.isdigit() or len(cpf) != 11:
                messagebox.showerror("Erro", "CPF deve ter 11 dígitos!")
                return
            
            if len(senha) < 3:
                messagebox.showerror("Erro", "Senha deve ter pelo menos 3 caracteres!")
                return
            
            if self.gerente.adicionar_funcionario(nome, cpf, senha):
                messagebox.showinfo("Sucesso", f"Funcionário {nome} adicionado com sucesso!")
                dialog.destroy()
            else:
                messagebox.showerror("Erro", "CPF já cadastrado!")
        
        # Botões
        frame_botoes = tk.Frame(dialog, bg='#f0f0f0')
        frame_botoes.pack(pady=20)
        
        tk.Button(frame_botoes, text="Adicionar", command=confirmar,
                 bg='#4CAF50', fg='white').pack(side='left', padx=5)
        tk.Button(frame_botoes, text="Cancelar", command=dialog.destroy,
                 bg='#f44336', fg='white').pack(side='left', padx=5)
    
    def remover_funcionario(self):
        """Dialog para remover funcionário"""
        cpf = simpledialog.askstring("Remover Funcionário", 
                                    "Digite o CPF do funcionário (11 dígitos):")
        
        if cpf and cpf.isdigit() and len(cpf) == 11:
            if self.gerente.remover_funcionario(cpf):
                messagebox.showinfo("Sucesso", "Funcionário removido com sucesso!")
            else:
                messagebox.showerror("Erro", "Funcionário não encontrado!")
        elif cpf:
            messagebox.showerror("Erro", "CPF deve ter 11 dígitos!")
    
    def listar_funcionarios(self):
        """Mostra lista de funcionários"""
        if not self.gerente.funcionarios:
            messagebox.showinfo("Informação", "Nenhum funcionário cadastrado.")
            return
        
        janela = tk.Toplevel(self.root)
        janela.title("Lista de Funcionários")
        janela.geometry("600x400")
        janela.configure(bg='#f0f0f0')
        
        # Treeview
        tree = ttk.Treeview(janela, columns=('Nome', 'CPF'), show='headings')
        tree.heading('Nome', text='Nome')
        tree.heading('CPF', text='CPF')
        
        for cpf, funcionario in self.gerente.funcionarios.items():
            cpf_formatado = util.imprimir_cpf(funcionario.cpf)
            tree.insert('', 'end', values=(funcionario.nome, cpf_formatado))
        
        tree.pack(expand=True, fill='both', padx=20, pady=20)
        
        tk.Button(janela, text="Fechar", command=janela.destroy,
                 bg='#2196F3', fg='white').pack(pady=10)
    
    def mostrar_historico_gerente(self):
        """Mostra histórico do gerente"""
        if not self.gerente.historico:
            messagebox.showinfo("Informação", "Nenhuma ação realizada.")
            return
        
        janela = tk.Toplevel(self.root)
        janela.title("Histórico do Gerente")
        janela.geometry("600x400")
        janela.configure(bg='#f0f0f0')
        
        # Text widget com scroll
        frame_text = tk.Frame(janela)
        frame_text.pack(expand=True, fill='both', padx=20, pady=20)
        
        text_widget = tk.Text(frame_text, wrap='word')
        scrollbar = tk.Scrollbar(frame_text, orient='vertical', command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        for acao in self.gerente.historico:
            text_widget.insert('end', acao + '\\n')
        
        text_widget.config(state='disabled')
        
        text_widget.pack(side='left', expand=True, fill='both')
        scrollbar.pack(side='right', fill='y')
        
        tk.Button(janela, text="Fechar", command=janela.destroy,
                 bg='#2196F3', fg='white').pack(pady=10)
    
    # Métodos do Funcionário
    def registrar_hospede(self):
        """Dialog para registrar hóspede"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Registrar Hóspede")
        dialog.geometry("350x250")
        dialog.configure(bg='#f0f0f0')
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Campos
        tk.Label(dialog, text="Nome:", bg='#f0f0f0').pack(pady=5)
        entry_nome = tk.Entry(dialog, width=30)
        entry_nome.pack(pady=5)
        
        tk.Label(dialog, text="CPF:", bg='#f0f0f0').pack(pady=5)
        entry_cpf = tk.Entry(dialog, width=30)
        entry_cpf.pack(pady=5)
        
        tk.Label(dialog, text="Número do Quarto (1-10):", bg='#f0f0f0').pack(pady=5)
        spinbox_quarto = tk.Spinbox(dialog, from_=1, to=10, width=28)
        spinbox_quarto.pack(pady=5)
        
        def confirmar():
            nome = entry_nome.get().upper().strip()
            cpf = entry_cpf.get().strip()
            
            if not nome:
                messagebox.showerror("Erro", "Nome não pode estar vazio!")
                return
            
            if not cpf.isdigit() or len(cpf) != 11:
                messagebox.showerror("Erro", "CPF deve ter 11 dígitos!")
                return
            
            try:
                quarto = int(spinbox_quarto.get())
                hospede = md.Hospede(nome, cpf, quarto)
                
                # Verificar se o quarto está disponível antes de tentar registrar
                if quarto not in self.checkin.quartos_disponiveis:
                    messagebox.showerror("Erro", f"O quarto {quarto} não está disponível!")
                    return
                
                if self.usuario_atual.registrar_hospede(self.checkin, hospede):
                    messagebox.showinfo("Sucesso", f"Hóspede {nome} registrado no quarto {quarto}!")
                    dialog.destroy()
                else:
                    messagebox.showerror("Erro", "Erro ao registrar hóspede! Verifique se o CPF já está cadastrado.")
            except ValueError:
                messagebox.showerror("Erro", "Número do quarto inválido!")
        
        # Botões
        frame_botoes = tk.Frame(dialog, bg='#f0f0f0')
        frame_botoes.pack(pady=20)
        
        tk.Button(frame_botoes, text="Registrar", command=confirmar,
                 bg='#4CAF50', fg='white').pack(side='left', padx=5)
        tk.Button(frame_botoes, text="Cancelar", command=dialog.destroy,
                 bg='#f44336', fg='white').pack(side='left', padx=5)
    
    def listar_hospedes(self):
        """Mostra lista de hóspedes"""
        if not self.checkin.hospedes:
            messagebox.showinfo("Informação", "Nenhum hóspede registrado.")
            return
        
        janela = tk.Toplevel(self.root)
        janela.title("Lista de Hóspedes")
        janela.geometry("600x400")
        janela.configure(bg='#f0f0f0')
        
        # Treeview
        tree = ttk.Treeview(janela, columns=('Nome', 'CPF', 'Quarto'), show='headings')
        tree.heading('Nome', text='Nome')
        tree.heading('CPF', text='CPF')
        tree.heading('Quarto', text='Quarto')
        
        for hospede in self.checkin.hospedes.values():
            cpf_formatado = util.imprimir_cpf(hospede.cpf)
            tree.insert('', 'end', values=(hospede.nome, cpf_formatado, hospede.quarto))
        
        tree.pack(expand=True, fill='both', padx=20, pady=20)
        
        tk.Button(janela, text="Fechar", command=janela.destroy,
                 bg='#2196F3', fg='white').pack(pady=10)
    
    def listar_quartos_disponiveis(self):
        """Mostra quartos disponíveis"""
        quartos = util.ordenar_quartos(self.checkin.quartos_disponiveis)
        
        if not quartos:
            messagebox.showinfo("Informação", "Nenhum quarto disponível.")
            return
        
        janela = tk.Toplevel(self.root)
        janela.title("Quartos Disponíveis")
        janela.geometry("300x400")
        janela.configure(bg='#f0f0f0')
        
        tk.Label(janela, text="Quartos Disponíveis:", 
                font=("Arial", 12, "bold"), bg='#f0f0f0').pack(pady=10)
        
        # Listbox
        listbox = tk.Listbox(janela, font=("Arial", 11))
        for quarto in quartos:
            listbox.insert('end', f"Quarto {quarto}")
        
        listbox.pack(expand=True, fill='both', padx=20, pady=10)
        
        tk.Button(janela, text="Fechar", command=janela.destroy,
                 bg='#2196F3', fg='white').pack(pady=10)
    
    def remover_hospede(self):
        """Dialog para remover hóspede"""
        cpf = simpledialog.askstring("Remover Hóspede", 
                                    "Digite o CPF do hóspede (11 dígitos):")
        
        if cpf and cpf.isdigit() and len(cpf) == 11:
            # Buscar nome do hóspede
            nome = ""
            if cpf in self.checkin.hospedes:
                nome = self.checkin.hospedes[cpf].nome
            
            if self.checkout.remover_hospede(cpf, self.checkin, self.usuario_atual, nome):
                messagebox.showinfo("Sucesso", "Hóspede removido com sucesso!")
            else:
                messagebox.showerror("Erro", "Hóspede não encontrado!")
        elif cpf:
            messagebox.showerror("Erro", "CPF deve ter 11 dígitos!")
    
    def mostrar_historico_funcionario(self):
        """Mostra histórico do funcionário"""
        if not self.usuario_atual.historico:
            messagebox.showinfo("Informação", "Nenhuma ação realizada.")
            return
        
        janela = tk.Toplevel(self.root)
        janela.title(f"Histórico - {self.usuario_atual.nome}")
        janela.geometry("600x400")
        janela.configure(bg='#f0f0f0')
        
        # Text widget com scroll
        frame_text = tk.Frame(janela)
        frame_text.pack(expand=True, fill='both', padx=20, pady=20)
        
        text_widget = tk.Text(frame_text, wrap='word')
        scrollbar = tk.Scrollbar(frame_text, orient='vertical', command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        for acao in self.usuario_atual.historico:
            text_widget.insert('end', acao + '\\n')
        
        text_widget.config(state='disabled')
        
        text_widget.pack(side='left', expand=True, fill='both')
        scrollbar.pack(side='right', fill='y')
        
        tk.Button(janela, text="Fechar", command=janela.destroy,
                 bg='#2196F3', fg='white').pack(pady=10)
    
    def executar(self):
        """Inicia a aplicação"""
        self.root.mainloop()

if __name__ == "__main__":
    app = HotelGUI()
    app.executar()

