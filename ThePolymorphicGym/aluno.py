from pessoa import Pessoa


class Aluno(Pessoa):

    __slots__ = ('_plano')

    def __init__(self, nome, idade, endereco, telefone, email, cpf, plano):
        super().__init__(nome, idade, endereco, telefone, email, cpf)
        self._plano = plano
        Pessoa._pessoas_alunos[self.nome] = self


    @staticmethod
    def buscar_pessoa(nome):
        return Pessoa._pessoas_alunos.get(nome, None)
       

    def exibir_informacoes(self):
        print(f"Aluno: {self.nome}")
        print(f"Plano: {self.plano}")
        print(f"Data de Registro: {self.data_registro.strftime('%d/%m/%Y %H:%M:%S')}")   
   

    def calcular_beneficio(self):
        if self._plano == "Anual":
            print("Desconto de 10% em renovação!")
        else:
            return "Sem desconto aplicado."
    
    @staticmethod
    def listar_pessoas():
        for pessoa in Pessoa._pessoas_alunos:
            print(pessoa)
        
    
        

    @property
    def plano(self):
        return self._plano

    @plano.setter
    def plano(self, novo_plano):
        self._plano = novo_plano