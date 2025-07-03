from abc import ABC, abstractmethod
from datetime import datetime

# Classes
class Pessoa(ABC):

    __slots__ = ('_nome', '_idade', '_endereco', '_telefone', '_email', '_cpf', '_data_registro')
    _pessoas_alunos = {}
    _pessoas_funcionarios = {}

    def __init__(self, nome, idade, endereco, telefone, email, cpf):
        self._nome = nome
        self._idade = idade
        self._endereco = endereco
        self._telefone = telefone
        self._email = email
        self._cpf = cpf
        self._data_registro = datetime.now()

    @property
    def nome(self):
        return self._nome

    @property
    def idade(self):
        return self._idade

    @property
    def endereco(self):
        return self._endereco

    @property
    def telefone(self):
        return self._telefone

    @property
    def email(self):
        return self._email

    @property
    def cpf(self):
        return self._cpf

    @property
    def data_registro(self):
        return self._data_registro
    
    @property
    def pessoas_alunos(self):
        return self._pessoas_alunos

    @property
    def pessoas_funcionarios(self):
        return self._pessoas_funcionarios

    @abstractmethod
    def exibir_informacoes(self):
        pass

    @abstractmethod
    def calcular_beneficio(self):
        pass

    @staticmethod
    @abstractmethod
    def listar_pessoas():
        pass

    @staticmethod
    @abstractmethod
    def buscar_pessoa(nome):
        pass