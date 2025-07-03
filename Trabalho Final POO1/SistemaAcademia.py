import datetime # Importa a biblioteca datetime
import os # Importa a biblioteca que interage com os sistema 
import platform # Importa a biblioteca que indentifica o sistema operacional
from abc import ABC, abstractmethod # Importa a biblioteca que cria classes abstratas

#Interface para o usuário
class Usuario(ABC):
    @abstractmethod
    def mostrar_dados(self):#metodo basico de mostrar dados do usuario
        pass

#Classe base para a pessoa (herda de Usuario)
class Pessoa(Usuario):
    def __init__(self, nome):
        self._nome = nome
        
    @property
    def nome(self):
        return self._nome
    
    def mostrar_dados(self):
        print(f"👤 Nome: {self.nome}")#apenas mostra o nome
        
#Classe gerente que herda de pessoa e implementa mais metodos
class Gerente(Pessoa):
    
    _credenciais = {"admin": "senha123"} #dicionario para armazenar as credenciais de acesso
    
    def __init__(self, nome, nivel):
        super(). __init__ (nome) #chama o construtor da classe mãe (Pessoa)
        self._nivel = nivel #nivel referente ao nivel de acesso do gerente
        
    @property
    def nivel(self):
        return self._nivel
    
    def autenticar(self, usuario, senha):
        #metodo para autenticar um gerente
        if Gerente._credenciais.get(usuario) == senha:#com base no usuario verifica se a senha esta correta
            print("Autenticacao realizada com sucesso!")
            return True#se for campativel retorna verdadeiro
        print("⚠️  Usuario ou senha invalidos!")
        return False#caso a senha ou nome de usuario esteja errado ou nome de usuario nao exista retorna falso
    
    def cadastrar_gerente(self):
        #metodo para cadastrar um novo gerente
        usuario = input("Digite o nome de usuario para o novo gerente: ")
        if usuario in Gerente._credenciais:#verifica se ja existe um gerente com esse nome
            print("Usuario ja existe!")
            return
        #caso nao exista, pede a senha para o novo gerente
        senha = input("Digite a senha para o novo gerente: ")
        Gerente._credenciais[usuario] = senha
        print(f"Gerente {usuario} cadastrado com sucesso!")
        
    def listar_alunos(self, sistema):
        #metodo para listar os alunos cadastrados no sistema
        # print("\n----- LISTA DE ALUNOS -----")
        sistema.listar_alunos()
        
    def registrar_frequencia(self, sistema, aluno_id):
        #metodo para registrar a frequencia de um aluno naquele dia
        aluno = sistema.buscar_aluno_por_id(aluno_id) #busca o aluno com base no id
        if aluno:
            data = datetime.datetime.now()#salva a data atual
            if not aluno.status_matricula:#verifica se a matricula do aluno esta cancelada
                #caso a matricula esteja cancelada, nao e possivel registrar a frequencia
                print(f"⚠️  O aluno {aluno.nome} tem a matrícula cancelada. Não é possível registrar frequência.")
                return
            aluno.frequencia.registrar_presencas(data)#salva essa data no registro de frequencia do aluno
            print(f"Frequencia registrada para o aluno {aluno.nome} no dia {data.strftime('%d/%m/%Y')}.")
            
    
#classe para controle de frequencia
class Frequencia():
    def __init__(self):
        self._presencas = {}#dicionario para armazenar as presencas
        
    @property
    def presencas(self):
        return self._presencas
    
    def registrar_presencas(self,data):
        #metodo para registrar a presenca de um aluno naquela data
        data_str = data.strftime('%d/%m/%Y')#converte a data para string(fica mais facil)
        if data_str not in self._presencas:
            self._presencas[data_str] = 0#se nao tiver nenhuma presenca naquela data, inicializa com 0
        self._presencas[data_str] += 1#mantes o registro de presenca naquela data
        
    def exibir_frequencia(self):
        #metodo para exibir a frequencia do aluno

        for data, count in self._presencas.items():#retorna os pares de chave e valor do dicionario
            print(f"Data: {data} - Presenças: {count}")
        
    
#classe de pagamentos
class Pagamento():
    def __init__(self):
        self._historico = []#lista para armazenar o historico de pagamentos
        
    @property
    def historico(self):
        return self._historico
    
    def registrar_pagamento(self, valor, preco_plano, data = None):
        #metodo para registrar um pagamento
        if abs(valor - preco_plano) > 0.01:#verifica se o valor do pagamento e igual ao preco do plano com 1 centavo de tolerancia
            print(f"⚠️  Erro: O valor do pagamento (R$ {valor:.2f}) nao corresponde ao preco do plano (R$ {preco_plano:.2f}).")
            return False
        
        data = data or datetime.datetime.now()#pega a data atual ou usa a data fornecida
        
        if self._historico:#se ja tiver algum pagamento registrado
            ultimo_pagamento = self._historico[-1]["data"]#pega a data do ultimo pagamento
            dias_desde_ultimo = (data - ultimo_pagamento).days#calcula quantos dias se passaram desde o ultimo pagamento
            if dias_desde_ultimo < 30:
                print(f"⚠️  Erro: O pagamento so pode ser feito apos 30 dias do ultimo pagamento. Faltam {30 - dias_desde_ultimo} dias.")
                return False
        
        # Registrar o pagamento
        self._historico.append({"valor": valor, "data": data})#registra a data e o valor do pagamento
        print(f"Pagamento de R$ {valor:.2f} registrado em {data.strftime('%d/%m/%Y')}.")
        return True
    
    def exibir_historico(self):
        #metodo para exibir o historico de pagamentos

        for pagamento in self._historico:
            print(f"Valor: R$ {pagamento['valor']:.2f} - Data: {pagamento['data'].strftime('%d/%m/%Y')}")#imprime o valor e a data do pagamento
            
    def verificar_inadimplencia(self, dias_tolerancia=30):
        #metodo para verificar se o aluno esta inadimplente
        if not self._historico:#verifica se o historico esta vazio
            return True
        ultimo_pagamento = self._historico[-1]["data"]#pega a data do ultimo pagamento
        return (datetime.datetime.now() - ultimo_pagamento).days > dias_tolerancia#retorna verdadeiro se o aluno esta inadimplente
    
    
#classe para o Plano
class Plano():
    def __init__(self, nome, preco, descricao):
        self._nome = nome
        self._preco = preco
        self._descricao = descricao
        
    @property
    def nome(self):
        return self._nome
    
    @property
    def preco(self):
        return self._preco
    
    @property
    def descricao(self):
        return self._descricao
    
    def mostrar_detalhes(self):
        #metodo para mostrar os detalhes do plano selecionado
        print(f"Nome: {self.nome}")
        print(f"Preço: R$ {self.preco:.2f}")
        print(f"Descrição: {self.descricao}")
        
    
#classe para o aluno
class Aluno(Pessoa):
    ultimo_id = 0#variavel para armazenar o ultimo id de aluno cadastrado
    
    def __init__(self, nome, plano):
        super().__init__(nome)
        Aluno.ultimo_id += 1#incrementa o id do aluno
        self._id = f"{Aluno.ultimo_id:03d}"#cria o id do aluno ja formatado
        self._plano = plano
        self._frequencia = Frequencia()#cria um objeto de frequencia
        self._pagamento = Pagamento()#cria um objeto de pagamento
        self._status_matricula = True#status da matricula do aluno inicia como ativa
        
    @property
    def id(self):
        return self._id
    
    @property
    def plano(self):
        return self._plano
    
    @plano.setter
    def plano(self, novo_plano):
        self._plano = novo_plano
        
    @property
    def frequencia(self):
        return self._frequencia
    
    @property
    def pagamento(self):
        return self._pagamento
    
    @property
    def status_matricula(self):
        return self._status_matricula
    
    @status_matricula.setter
    def status_matricula(self, novo_status):
        self._status_matricula = novo_status
        
    def cancelar_matricula(self):
        #metodo para cancelar a matricula do aluno
        if self._status_matricula:#verifica se a matricula ja esta como True
            self._status_matricula = False
            print("✔️  Matricula cancelada com sucesso.")
        else:
            print("⚠️  Matricula ja esta cancelada.")
    
    def reativar_matricula(self):
        if not self._status_matricula:  # Verifica se a matrícula esta cancelada
            self._status_matricula = True
            print("✔️ Matricula reativada com sucesso.")
        else:  # Caso a matrícula já esteja ativa
            print("⚠️ A matrícula ja esta ativa.")
    
    def mostrar_dados(self):
        print("\n-------------------------")
        print(f"📌 ID: {self.id}")
        super().mostrar_dados()#chama o metodo de mostrar dados da classe mae
        print(f"🎓 Plano: {self.plano.nome} (R$ {self.plano.preco:.2f})")
        print(f"🔄 Status: {'Ativo' if self.status_matricula else 'Cancelado'}")#verifica os estado da matricula antes de printar
        print("-------------------------")
        
# Classe para Relatórios
class Relatorio():
    
    @staticmethod#metodo estatico pois nao precisa de uma instancia da classe para ser chamado, pois nao a atributos a serem usados no metodo
    def gerar_relatorio_inadimplentes(sistema):
        #metodo para gerar um relatorio de inadimplentes
        
        print("\n📊 ----- RELATÓRIO DE INADIMPLENTES ----- 📊")
        inadimplentes = [#cria uma lista com os alunos inadimplentes
            aluno for aluno in sistema.alunos#verifica aluno a aluno
            if aluno.pagamento.verificar_inadimplencia()#se o aluno estiver inadimplente add na lista
        ]
        if inadimplentes:#se tiver algum aluno inadimplente ele printa
            print("\n⚠️  Alunos com pagamentos pendentes:")
            for aluno in inadimplentes:
                print(f"👤 Nome: {aluno.nome} | Plano: {aluno.plano.nome}")
            print(f"\n📌  Total de inadimplentes: {len(inadimplentes)}")#mostra o total de alunos inadimplentes
        else:
            print("\n👌  Nenhum aluno inadimplente encontrado!")
            

#classe para o sistema
class Sistema():
    def __init__ (self):
        self._alunos = []#lista para armazenar os alunos cadastrados
        
    @property
    def alunos(self):
        return self._alunos
    
    def adicionar_aluno(self, nome, plano):
        #metodo para adicionar um aluno
        
        aluno = Aluno(nome, plano)#cria um objeto aluno
        self._alunos.append(aluno)#adiciona o aluno na lista
        print(f"Aluno {aluno.nome} cadastrado com sucesso!")
        
    def buscar_aluno_por_id(self, aluno_id):
        #metodo para buscar um aluno com base no id
        
        for aluno in self._alunos:#percorre a lista de alunos
            if aluno.id == aluno_id:#compara o id do aluno com o id fornecido
                return aluno
        print("⚠️  Aluno não encontrado.")
        return None
    
    def listar_alunos(self):
        #metodo para listar os alunos cadastrados
        
        print("\n📋 ----- LISTA DE ALUNOS ----- 📋")
        if not self._alunos:#verifica se a lista de alunos esta vazia
            print("⚠️  Nenhum aluno cadastrado no sistema.")
        else:
            print(f"\n👥 Total de alunos cadastrados: {len(self._alunos)}")#imprime o total de alunos cadastrados
            for aluno in self._alunos:#percorre a lista de alunos imprimindo os dados de cada um
                aluno.mostrar_dados()
                
    @staticmethod#metodo estatico pois nao precisa de uma instancia da classe para ser chamado, pois nao a atributos a serem usados no metodo
    def selecionar_plano():
        #metodo para selcionar planos
        
        planos = {#dicionario com os planos existentes
            "1": Plano("Economico", 70.0, "3 vezes na semana"),
            "2": Plano("Padrao", 100.0, "5 vezes na semana"),
            "3": Plano("Premium", 200.0, "Todos os dias com acompanhamento")
        }
        
        while True:
            print("\n💼 ----- PLANOS DISPONIVEIS ----- 💼")
            for key, plano in planos.items():#percorre o dicionario de planos imprimindo os dados de cada um
                print(f"{key}. {plano.nome} - R$ {plano.preco:.2f}: {plano.descricao}")
            print("\nℹ️  Escolha um plano digitando o numero correspondente.")
            
            escolha = input("👉 Escolha um plano (1-3): ")
            if escolha in planos:#verifica se a escolha esta dentro das opcoes
                print(f"\n✔️  Voce selecionou o plano '{planos[escolha].nome}'.")
                return planos[escolha]#retorna o plano selecionado
            print("\n❌  Opcao invalida. Por favor, tente novamente.")
            
            
######################  MENUS  ######################
            
#menu principal
def menu_principal(sistema):
    #menu principal do sistema (primeiro menu a ser exibido)
    
    while True:#repete ate o usuario escolher sair
        limpar_terminal()#limpa a tela

        print("\n🏠 ----- MENU PRINCIPAL ----- 🏠")
        print("1️⃣  Login como gerente")
        print("2️⃣  Sair")
        print("\nℹ️  Escolha uma opcao digitando o numero correspondente.\n")

        try:
            opcao = input("👉 Escolha uma opcao: ")

            if opcao == "1":
                print("\n🔒 ----- LOGIN DO GERENTE ----- 🔒")
                usuario = input("👤  Digite o nome de usuario: ")
                senha = input("🔑 Digite a senha: ")
                gerente = Gerente(usuario, "Administrador")#cria uma instancia de gerente
                
                if gerente.autenticar(usuario, senha):#verifica se o gerente esta autenticado
                    print("\n✔️  Acesso autorizado! Bem-vindo ao sistema, gerente!")
                    input("👉 Pressione Enter para acessar o menu do gerente...")
                    menu_gerente(sistema, gerente)#chama o menu do gerente
                    
                else:#tras erro caso as credenciais estejam erradas
                    print("\n❌ Credenciais invalidas. Por favor, tente novamente.")
                    input("👉 Pressione Enter para retornar ao menu principal...")
            elif opcao == "2":
                print("\n🚪 Saindo do sistema. Ate logo! 👋")
                break
            else:
                print("\n⚠️  Opção invalida. Por favor, escolha uma das opcoes disponiveis.")
                input("👉 Pressione Enter para continuar...")

        except Exception as e:#trata qualquer erro inesperado
            print(f"\n❌  Ocorreu um erro inesperado: {e}")
            print("⚠️  Por favor, tente novamente ou contate o suporte.")
            input("👉  Pressione Enter para continuar...")
            
#menu do gerente
def menu_gerente(sistema, gerente):
    #Menu principal para gerenciamento do sistema pelo gerente
    while True:
        limpar_terminal()#limpa a tela
        #opcoes do menu
        print("\n🧑‍💼 ----- MENU DO GERENTE ----- 🧑‍💼")
        print("1️⃣  Listar alunos")
        print("2️⃣  Registrar frequencia do dia")
        print("3️⃣  Adicionar aluno")
        print("4️⃣  Buscar aluno pelo nome")
        print("5️⃣  Gerar relatorio de inadimplentes")
        print("6️⃣  Mostrar alunos com pagamento em dia")
        print("7️⃣  Cadastrar novo gerente")
        print("8️⃣  Sair")
        print("\nℹ️  Escolha uma opcao digitando o numero correspondente.\n")

        opcao = input("👉 Escolha uma opção: ")

        if opcao == "1":#opcao para listar os alunos
            
            gerente.listar_alunos(sistema)#chama o metodo de listar alunos
            input("\n👉 Pressione Enter para continuar...")

        elif opcao == "2":#opcao para registrar a frequencia de um aluno
            
            print("\n🕒 ----- REGISTRAR FREQUENCIA ----- 🕒")
            aluno_id = input("Digite o ID do aluno: ")#pega o id do aluno
            gerente.registrar_frequencia(sistema, aluno_id)#chama o metodo de registrar frequencia
            input("\n👉 Pressione Enter para continuar...")

        elif opcao == "3":#opcao para adicionar um aluno
            
            print("\n✏️ ----- CADASTRAR NOVO ALUNO ----- ✏️")
            nome = input("Digite o nome do aluno: ")
            plano = Sistema.selecionar_plano()#chama o metodo de selecionar plano
            
            if plano:#verifica se o plano foi selecionado
                sistema.adicionar_aluno(nome, plano)#adiciona o aluno
                print(f"\n✔️  Aluno '{nome}' cadastrado com sucesso no plano '{plano.nome}'!")
            else:#caso nao tenha selecionado um plano
                print("\n❌  Plano invalido. Tente novamente.")
            input("\n👉 Pressione Enter para continuar...")

        elif opcao == "4":#opcao para buscar um aluno pelo nome
            
            print("\n🔍 ----- BUSCAR ALUNO ----- 🔍")
            termo = input("Digite o nome ou parte do nome do aluno (ou pressione Enter para listar todos): ").lower()#pega o termo para busca e converte para minusculo
            
            if not termo:#se o nome nao foi fornecido
                #ordena os alunos por ordem alfabetica
                resultados = sorted(sistema.alunos, key=lambda x: x.nome)
            else:#se o nome foi fornecido
                #ordena os alunos por ordem alfabetica
                #filtra os alunos que contem o termo no nome e ordena
                resultados = sorted([a for a in sistema.alunos if termo in a.nome.lower()], key=lambda x: x.nome)

            if resultados:#se tiver algum resultado
                print("\n👥 ----- ALUNOS ENCONTRADOS ----- 👥")
                for aluno in resultados:#imprime os alunos encontrados
                    print(f"📌 ID: {aluno.id} - Nome: {aluno.nome}")
                    
                #pergunta se deseja selecionar um aluno    
                aluno_id = input("👉 Digite o ID do aluno para selecionar ou 0 para voltar: ")
                if aluno_id == "0":#se o usuario deseja voltar
                    print("\n↩️  Voltando ao menu do gerente...")
                else:
                    #busca o aluno com base no id fornecido
                    aluno_selecionado = sistema.buscar_aluno_por_id(aluno_id)
                    if aluno_selecionado:#se o aluno foi encontrado
                        menu_aluno(aluno_selecionado)#chama o menu do aluno
                    else:#se o aluno nao foi encontrado
                        print("\n❌  ID invalido. Tente novamente.")
            else:#se nao tiver nenhum resultado
                print("\n⚠️ Nenhum aluno encontrado com o termo informado.")
            input("\n👉 Pressione Enter para continuar...")

        elif opcao == "5":#opcao para gerar um relatorio de inadimplentes
            
            Relatorio.gerar_relatorio_inadimplentes(sistema)#chama o metodo de gerar relatorio de inadimplentes
            input("\n👉 Pressione Enter para continuar...")

        elif opcao == "6":#opcao para mostrar os alunos com pagamento em dia
            
            print("\n✅ ----- ALUNOS COM PAGAMENTO EM DIA ----- ✅")
            pagamentos_em_dia = [#cria uma lista com os alunos que estao com o pagamento em dia
                aluno for aluno in sistema.alunos
                if not aluno.pagamento.verificar_inadimplencia()
            ]
            if pagamentos_em_dia:#se tiver algum aluno com pagamento em dia
                for aluno in pagamentos_em_dia:#imprime os alunos com pagamento em dia
                    ultimo_pagamento = aluno.pagamento.historico[-1]["data"]
                    print(f"📌  ID: {aluno.id} - Nome: {aluno.nome} - Plano: {aluno.plano.nome} - Último pagamento: {ultimo_pagamento.strftime('%d/%m/%Y')}")
            else:
                print("\n🎉 Nenhum aluno com pagamentos pendentes!")#caso nao tenha alunos com pagamentos pendentes
            input("\n👉 Pressione Enter para continuar...")

        elif opcao == "7":#opcao para cadastrar um novo gerente
            
            print("\n👤 ----- CADASTRAR NOVO GERENTE ----- 👤")
            gerente.cadastrar_gerente()#chama o metodo de cadastrar um novo gerente
            input("\n👉 Pressione Enter para continuar...")

        elif opcao == "8":#opcao para sair do menu do gerente
            
            print("\n🚪 Saindo do menu do gerente. Até logo! 👋")
            break#sai do menu do gerente

        else:#caso a opcao seja invalida
            print("\n⚠️  Opcao invalida. Por favor, tente novamente.")
            input("\n👉 Pressione Enter para continuar...")
            
#menu do aluno (de longe o mais chato ate agora)
def menu_aluno(aluno):
    #Menu do aluno para gerenciar matricula e pagamentos daquele aluno
    while True:
        limpar_terminal()  # Limpa o terminal antes de exibir o menu do aluno
        #opcoes do menu
        print(f"\n🏋️ ----- MENU DO ALUNO: {aluno.nome} ----- 🏋️")
        print("1️⃣  Mudar de plano")
        print("2️⃣  Cancelar matricula")
        print("3️⃣  Reativar matrícula")
        print("4️⃣  Exibir histórico de pagamentos")
        print("5️⃣  Registrar pagamento")
        print("6️⃣  Exibir relatório de frequencia")
        print("7️⃣  Voltar")
        print("\nℹ️  Escolha uma opcao digitando o numero correspondente.\n")

        opcao = input("👉 Escolha uma opcao: ")

        if opcao == "1":#opcao para mudar de plano
            
            print("\n📋 ----- MUDAR DE PLANO ----- 📋")
            novo_plano = Sistema.selecionar_plano()#chama o metodo de selecionar plano para selecionar um novo plano
            if novo_plano:#verifica se o plano foi selecionado
                aluno.plano = novo_plano#muda o plano do aluno
                print(f"\n✔️  Plano alterado para '{novo_plano.nome}' com sucesso!")
            else:#caso nao tenha selecionado um plano
                print("\n❌ Plano invalido. Tente novamente.")
            input("\n👉 Pressione Enter para continuar...")

        elif opcao == "2":#opcao para cancelar a matricula
            
            print("\n🚫 ----- CANCELAR MATRICULA ----- 🚫")
            aluno.cancelar_matricula()#chama o metodo de cancelar a matricula
            input("\n👉 Pressione Enter para continuar...")

        elif opcao == "3":#opcao para reativar a matricula
            
            print("\n🔄 ----- REATIVAR MATRICULA ----- 🔄")
            aluno.reativar_matricula()#chama o metodo de reativar a matricula
            input("\n👉 Pressione Enter para continuar...")

        elif opcao == "4":#opcao para exibir o historico de pagamentos
            
            print("\n💳 ----- HISTORICO DE PAGAMENTOS ----- 💳")
            aluno.pagamento.exibir_historico()#chama o metodo de exibir o historico de pagamentos
            input("\n👉 Pressione Enter para continuar...")

        elif opcao == "5":#opcao para registrar um pagamento
            print("\n💰 ----- REGISTRAR PAGAMENTO ----- 💰")
            while True:#repete ate o pagamento ser registrado
                try:
                    #pede o valor do pagamento
                    #exibe o valor do plano
                    valor = float(input(f"Digite o valor do pagamento para o plano '{aluno.plano.nome}' (R$ {aluno.plano.preco:.2f}): R$ "))
                    if valor > 0:#verifica se o valor e positivo
                        #registra o pagamento
                        if aluno.pagamento.registrar_pagamento(valor, aluno.plano.preco):
                            #caso todas as condicoes sejam atendidas
                            #ja rejistra o pagamento no if e depois sai do loop
                            print("\n✔️  Pagamento registrado com sucesso!")
                            break  # Sai do loop apos o registro dar certo
                        else:#caso o pagamento nao seja registrado
                            print("\n❌ Pagamento nao registrado. Verifique os detalhes e tente novamente.")
                    else:#caso o valor seja negativo
                        print("\n⚠️  O valor deve ser positivo.")
                except ValueError:#caso o valor nao seja um numero
                    print("\n⚠️  Entrada invalida. Digite um numero.")

                # Adicionar uma opcao para sair do loop caso o o ultimo pagamento tenha sido feito a menos de 30 dias
                sair = input("❓ Deseja tentar novamente? (S/N): ").strip().lower()
                if sair == 'n':
                    print("\n↩️  Cancelando registro de pagamento.")
                    break
            input("\n👉 Pressione Enter para continuar...")

        elif opcao == "6":#opcao para exibir o relatorio de frequencia
            
            print("\n🕒 ----- RELATÓRIO DE FREQUÊNCIA ----- 🕒")
            aluno.frequencia.exibir_frequencia()#chama o metodo de exibir a frequencia
            input("\n👉 Pressione Enter para continuar...")

        elif opcao == "7":#opcao para voltar ao menu do gerente
            
            print("\n↩️  Voltando ao menu do gerente...")
            break#sai do menu do aluno

        else:#caso a opcao seja invalida
            print("\n⚠️  Opção invalida. Por favor, escolha uma das opções disponiveis.")
            input("\n👉 Pressione Enter para continuar...")
            
    
#funcao para limpar o terminal            
def limpar_terminal():
    # Verifica o sistema operacional
    sistema = platform.system()
    if sistema == "Windows":
        os.system("cls")  # Comando para limpar o terminal no Windows
    else:
        os.system("clear")  # Comando para limpar o terminal em sistemas Unix (Linux/Mac)
        
        
######################  MAIN  ######################
if __name__ == "__main__":
    sistema = Sistema()

    # Criando gerente inicial
    gerente_inicial = Gerente("admin", "Administrador")
    Gerente._credenciais["admin"] = "senha123"

    # Planos disponiveis
    #instanciando os planos que a academia oferece
    #apenas para instanciar os anulos diretamentes com os planos (para testes)
    plano_economico = Plano("Economico", 70.0, "3 vezes na semana")
    plano_basico = Plano("Basico", 100.0, "5 vezes na semana")
    plano_premium = Plano("Premium", 200.0, "Todos os dias com acompanhamento")

    # Adicionando 10 alunos com planos variados
    sistema.adicionar_aluno("João Silva", plano_economico)
    sistema.adicionar_aluno("Maria Oliveira", plano_basico)
    sistema.adicionar_aluno("Pedro Santos", plano_premium)
    sistema.adicionar_aluno("Ana Souza", plano_basico)
    sistema.adicionar_aluno("Carlos Lima", plano_economico)
    sistema.adicionar_aluno("Fernanda Costa", plano_premium)
    sistema.adicionar_aluno("Juliana Ribeiro", plano_basico)
    sistema.adicionar_aluno("Gustavo Almeida", plano_premium)
    sistema.adicionar_aluno("Mariana Rocha", plano_economico)
    sistema.adicionar_aluno("Rafael Fernandes", plano_basico)
    
    # Mensagem de inicializacao
    limpar_terminal()
    print("🎉 Bem-vindo ao Sistema de Gestao de Alunos da Academia O SUCO(100% Natulal)! 🎉")
    print("✅ O sistema esta pronto para uso com 10 alunos pre-cadastrados (para testes).")
    input("👉 Pressione Enter para acessar o menu principal...")

    # Iniciando o sistema
    menu_principal(sistema)