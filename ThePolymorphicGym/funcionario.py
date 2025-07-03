from pessoa import Pessoa


class Funcionario(Pessoa):

    __slots__ = ('_salario',)

    def __init__(self, nome, idade, endereco, telefone, email, cpf, salario):
        super().__init__(nome, idade, endereco, telefone, email, cpf)
        self._salario = salario
        Pessoa._pessoas_funcionarios[self.nome] = self

    @staticmethod
    def buscar_pessoa(nome):
        return Pessoa._pessoas_funcionarios.get(nome, None)
    
    def exibir_informacoes(self):
        print(f"Funcionário: {self.nome}")
        print(f"Salário: R$ {self.salario:.2f}")
        print(f"Data de Registro: {self.data_registro.strftime('%d/%m/%Y %H:%M:%S')}")

    def calcular_beneficio(self):
        return "Benefício: Bônus mensal de R$ 200,00"

    @staticmethod
    def listar_pessoas():
        for pessoa in Pessoa._pessoas_funcionarios:
            print(pessoa)
        
    @property
    def salario(self):
        return self._salario