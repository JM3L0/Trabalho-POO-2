import abc

class Autentica(abc.ABC):
    @abc.abstractmethod
    def autentica(self, senha):
        pass

class Pessoa:
    def __init__(self, nome, cpf):
        self._nome = nome
        self._cpf = cpf

    @property
    def nome(self):
        return self._nome
    @nome.setter
    def nome(self, nome):
        self._nome = nome

    @property
    def cpf(self):
        return self._cpf

class Funcionario(Pessoa, Autentica):
    def __init__(self, nome, cpf, senha):
        super().__init__(nome, cpf)
        self._senha = senha
        self._historico = []

    @property
    def senha(self):
        return self._senha
    @senha.setter
    def senha(self, senha):
        self._senha = senha
    
    @property
    def historico(self):
        return self._historico
    @historico.setter
    def historico(self, historico):
        self._historico = historico

    def autentica(self, senha):
        if self.senha == senha:
            return True
        else:
            return False
        
class Funcionario_padrao(Funcionario):
    def registrar_hospede(self, checkin, hospede):
        if checkin.registrar_hospede(hospede) == True:
            self.historico.append(f"Funcionário ({self.nome}) fez o checkin do hóspede ({hospede.nome}).")
            return True
        
    def listar_hospedes(self, checkin):
        checkin.listar_hospedes()

    def listar_quartos_disponiveis(self, checkin):
        checkin.listar_quartos_disponiveis()

    def remover_hospede(self, cpf, checkout):
        checkout.remover_hospede(cpf)
        
class Gerente(Funcionario):
    def __init__(self, nome, cpf, senha):
        super().__init__(nome, cpf, senha)
        self._funcionarios = {}

    @property
    def funcionarios(self):
        return self._funcionarios
    @funcionarios.setter
    def funcionarios(self, funcionarios):
        self._funcionarios = funcionarios

    def adicionar_funcionario(self, nome, cpf, senha):
        if not cpf.isdigit() or len(cpf) != 11:
            print("\nCPF inválido. Deve ser um número de 11 caracteres.")
            return False
        if cpf in self.funcionarios:
            print("\nCPF já cadastrado para outro funcionário.")
            return False
        novo_funcionario = Funcionario_padrao(nome, cpf, senha)
        self.funcionarios[cpf] = novo_funcionario
        self.historico.append(f"Funcionário com cpf ({cpf}) adicionado.")
        print(f"\nFuncionário {nome} adicionado com sucesso.")
        return True

    def remover_funcionario(self, cpf):
        if not cpf.isdigit() or len(cpf) != 11:
            print("\nCPF inválido. Deve ser um número de 11 caracteres.")
            return False
        if cpf in self.funcionarios:
            del self.funcionarios[cpf]
            self.historico.append(f"Funcionário com CPF ({cpf}) removido.")
            print("\nFuncionário removido com sucesso.")
            return True
        else:
            print("\nNenhum funcionário com esse CPF foi encontrado.")
            return False

    def listar_funcionarios(self):
        if not self.funcionarios:
            print("\nNenhum funcionário cadastrado.")
            return False
        else:
            print("\nLista de Funcionários:")
            for cpf, funcionario in self.funcionarios.items():
                print(f"Nome: {funcionario.nome}\nCPF: {funcionario.cpf}\n")
            return True
        
    def imprimir_historico_gerente(self):
        if not self.historico:
            print("\nNenhuma ação realizada.")
            return False
        else:
            print("\nHistórico de ações do gerente:")
            for acao in self.historico:
                print(acao)
            return True

class Hospede(Pessoa):
    def __init__(self, nome, cpf, quarto):
        super().__init__(nome, cpf)
        self._quarto = quarto

    @property
    def quarto(self):
        return self._quarto
    @quarto.setter
    def quarto(self, quarto):
        self._quarto = quarto

    def _str_(self):
        return f"Hóspede: {self.nome}\nCPF: {self.cpf}\nQuarto: {self.quarto}"

class Sistema:
    def login(self, usuario, senha):
        if isinstance(usuario, Autentica):
            return usuario.autentica(senha)
        return False

class CheckIn:
    def __init__(self):
        pass
    
    hospedes = {}
    quartos_disponiveis = list(range(1, 11))

    def registrar_hospede(self, hospede):
        if not hospede.cpf.isdigit() or len(hospede.cpf) != 11:
            print("\nCPF inválido. Deve ser um número de 11 caracteres.")
            return False
        if hospede.cpf in CheckIn.hospedes:
            print("\nCPF já cadastrado para outro hóspede.")
            return False
        if hospede.quarto in CheckIn.quartos_disponiveis:
            CheckIn.hospedes[hospede.cpf] = hospede
            CheckIn.quartos_disponiveis.remove(hospede.quarto)
            print(f"\nHóspede {hospede.nome} registrado no quarto {hospede.quarto}.")
            return True
        else:
            print(f"\nO quarto {hospede.quarto} não está disponível.")
            return False

    def listar_hospedes(self):
        if not CheckIn.hospedes:
            print("\nNenhum hóspede registrado.")
            return False
        else:
            print("\nLista de Hóspedes:")
            for hospede in CheckIn.hospedes.values():
                print(f"Nome: {hospede.nome}\nCPF: {hospede.cpf}\nQuarto: {hospede.quarto}\n")

    def listar_quartos_disponiveis(self):
        quartos_disponiveis = ordenar_quartos(CheckIn.quartos_disponiveis)
        print(f"\nQuartos disponíveis: {quartos_disponiveis}")


class CheckOut:
    def __init__(self):
        pass
    def remover_hospede(self, cpf, checkin, funcionario, nome):
        if not cpf.isdigit() or len(cpf) != 11:
            print("\nCPF inválido. Deve ser um número de 11 caracteres.")
            return False
        if cpf in checkin.hospedes:
            checkin.quartos_disponiveis.append(checkin.hospedes[cpf].quarto)
            del checkin.hospedes[cpf]
            print(f"\nHóspede com CPF {cpf} removido com sucesso.")
            funcionario.historico.append(f"Funcionário ({funcionario.nome}) fez o checkout do hóspede ({nome}).")
            return True
        else:
            print(f"\nNenhum hóspede com CPF {cpf} foi encontrado.")
            return False
        
def ordenar_quartos(lista):
    return sorted(lista)

def verifica_tamanho_senha(senha):
    if len(senha) < 3:
        print("\nSenha muito curta. A senha deve ter no mínimo 3 caracteres.")
        return False
    else:
        return True

def menu_funcionario():
    print("\n=== Menu do Funcionário ===")
    print("[1] - Registrar Hóspede (Check-in)")
    print("[2] - Listar Hóspedes")
    print("[3] - Listar Quartos Disponíveis")
    print("[4] - Remover Hóspede (Check-out)")
    print("[5] - Imprimir Histórico")
    print("[0] - Logout")
    
def menu_inicial():
    print("\n=== Sistema de Hotel ===")
    print("[1] - Login como Gerente")
    print("[2] - Login como Funcionário")
    print("[0] - Sair")
    
def menu_gerente():
    print("\n=== Menu do Gerente ===")
    print("[1] - Adicionar Funcionário")
    print("[2] - Remover Funcionário")
    print("[3] - Listar Funcionários")
    print("[4] - Imprimir Histórico")
    print("[0] - Logout")
        
def menu_principal():
    sistema = Sistema()
    checkin = CheckIn()
    checkout = CheckOut()

    #O Gerente é o núcleo do sistema do gerente. Ele não deve ser removido sob nenhuma circunstância.
    gerente = Gerente("Gerente Geral", "00000000000", "123")    
    gerente.adicionar_funcionario("Funcionário Padrão", "11111111111", "123")

    while True:
        menu_inicial()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            senha = input("Digite a senha do gerente: ")
            
            if verifica_tamanho_senha(senha) == False:
                continue
            if sistema.login(gerente, senha):
                print("\nLogin realizado com sucesso como Gerente!")
                while True:
                    menu_gerente()
                    opcao_gerente = input("Escolha uma opção: ")

                    if opcao_gerente == "1":
                        nome = input("\nNome do funcionário: ")
                        cpf = input("CPF do funcionário: ")
                        senha = input("Senha do funcionário: ")
                        
                        if verifica_tamanho_senha(senha) == False:
                            continue
                        gerente.adicionar_funcionario(nome, cpf, senha)
                    elif opcao_gerente == "2":
                        cpf = input("\nCPF do funcionário a ser removido: ")
                        
                        gerente.remover_funcionario(cpf)
                    elif opcao_gerente == "3":
                        gerente.listar_funcionarios()
                    elif opcao_gerente == "4":
                        gerente.imprimir_historico_gerente()
                    elif opcao_gerente == "0":
                        print("\nLogout do Gerente realizado.")
                        break
                    else:
                        print("\nOpção inválida! Tente novamente.")
            else:
                print("\nSenha incorreta!")
        elif opcao == "2":
            cpf = input("\nDigite o CPF do funcionário: ")
            senha = input("Digite a senha do funcionário: ")
            
            if verifica_tamanho_senha(senha) == False:
                continue
            funcionario = None
            for f in gerente.funcionarios.values():
                if f.cpf == cpf:
                    funcionario = f
                    break
            if funcionario and sistema.login(funcionario, senha):
                print(f"\nLogin realizado com sucesso como {funcionario.nome}!")
                while True:
                    menu_funcionario()
                    opcao_funcionario = input("Escolha uma opção: ")

                    if opcao_funcionario == "1":
                        try:
                            nome = input("\nNome do hóspede: ")
                            cpf = input("CPF do hóspede: ")
                            
                            try:
                                quarto = int(input("Número do quarto (1 a 10): "))
                                
                                if quarto not in range(1, 11):
                                    print("\nNúmero do quarto inválido. Deve estar entre 1 e 10.")
                                    continue
                            except ValueError:
                                print("\nEntrada inválida. O número do quarto deve ser um número inteiro.")
                                continue
                            hospede = Hospede(nome, cpf, quarto)
                            funcionario.registrar_hospede(checkin, hospede)
                        except ValueError:
                            print("\nEntrada inválida. O número do quarto deve ser um número inteiro.")
                    elif opcao_funcionario == "2":
                        funcionario.listar_hospedes(checkin)
                    elif opcao_funcionario == "3":
                        funcionario.listar_quartos_disponiveis(checkin)
                    elif opcao_funcionario == "4":
                        cpf = input("CPF do hóspede a ser removido: ")
                        
                        checkout.remover_hospede(cpf, checkin, funcionario, nome)
                    elif opcao_funcionario == "5":
                        print(f"\nHistórico de ações do funcionário {funcionario.nome}")
                        if not funcionario.historico:
                            print("\nNenhuma ação realizada.")
                        else:
                            for acao in funcionario.historico:
                                print(acao)
                    elif opcao_funcionario == "0":
                        print("\nLogout do Funcionário realizado.")
                        break
                    else:
                        print("\nOpção inválida! Tente novamente.")
            else:
                if not funcionario:
                    print("\nFuncionário não encontrado.")
                else:
                    print("\nSenha incorreta!")
        elif opcao == "0":
            print("\nSaindo do sistema...")
            break
        else:
            print("\nOpção inválida! Tente novamente.")

menu_principal()