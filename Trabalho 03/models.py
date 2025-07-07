import abc
import util

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
        return (senha == self.senha)
          
class Funcionario_padrao(Funcionario):
    def registrar_hospede(self, checkin, hospede):
        if checkin.registrar_hospede(hospede) == True:
            self.historico.append(f"Funcionário ({self.nome}) fez o checkin do hóspede ({hospede.nome}).")
            return True
        return False
        
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
        self.historico.append(f"Funcionário com cpf ({util.imprimir_cpf(cpf)}) adicionado.")
        print(f"\nFuncionário {nome} adicionado com sucesso.")
        return True

    def remover_funcionario(self, cpf):
        
        if cpf in self.funcionarios:
            del self.funcionarios[cpf]
            self.historico.append(f"Funcionário com CPF ({util.imprimir_cpf(cpf)}) removido.")
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
            print("\nLista de Funcionários:\n")
            for cpf, funcionario in self.funcionarios.items():
                print(f"Nome: {funcionario.nome}\n{util.imprimir_cpf(funcionario.cpf)}\n")
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
        return f"Hóspede: {self.nome}\n{util.imprimir_cpf(self.cpf)}\nQuarto: {self.quarto}"