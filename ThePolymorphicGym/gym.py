from aluno import Aluno
from funcionario import Funcionario
from equipamentos import Equipamento

class Gym:

    _alunos = {}
    _planos_academia = {
            "Mensal": {"valor": 120.00, "duracao": 1},
            "Trimestral": {"valor": 300.00, "duracao": 3},
            "Anual": {"valor": 1000.00, "duracao": 12},
        }
    
    def __init__(self):
        self._alunos
        self._planos_academia 
    
    @staticmethod
    def buscar_planos(nome):
        return Gym._planos_academia.get(nome, None)


    def listar_alunos(self):
        for alunos in self.alunos.keys():
            print(Aluno.exibir_informacoes())
            

    def listar_funcionarios(self):
        for pessoa in self.funcionario:
            print(Funcionario.exibir_informacoes())


    def listar_equipamentos():
        for equipamento in Gym.equipamentos:
            print(Equipamento.exibir_informacoes())
