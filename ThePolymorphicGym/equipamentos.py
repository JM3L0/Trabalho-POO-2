from abc import ABC, abstractmethod
from datetime import datetime

class Equipamento:

    __slots__ = ('_nome', '_valor', '_id', '_descricao', '_data_registro')
    _manutencoes = {}
    _equipamentos = {}

    def __init__(self, nome, valor, id, descricao=""):
        self._nome = nome
        self._valor = valor
        self._id = id
        self._descricao = descricao
        self._data_registro = datetime.now()
        Equipamento._equipamentos[self.id] = self

    @staticmethod
    def buscar_equipamento(id):
        return Equipamento._equipamentos.get(id, None)

    @staticmethod
    def agendar_manutencao(id):
        data = input("Digite a data que desseja marcar a manutenção: ")
        descricao = input("Escreva o motivo da manutenção: ")
        Equipamento._manutencoes[id] = {'Data': data, 'Descrição': descricao}
       

    @staticmethod
    def exibir_informacoes(id):
        equipamento = Equipamento.buscar_equipamento(id)
        return (f"Equipamento: {equipamento.nome}, Valor: R$ {equipamento.valor}, ID: {equipamento.id}, "
                f"Data de Registro: {equipamento.data_registro.strftime('%d/%m/%Y %H:%M:%S')}")
    
    @staticmethod
    def listar_equipamentos():
        for equipamentos in Equipamento._equipamentos:
            print(equipamentos)

    
    @staticmethod
    def listar_manutencoes():
        if Equipamento._manutencoes:
            print("Lista de Manutenções:")
            for id, manutencao in Equipamento._manutencoes.items():
                print(f"ID do Equipamento: {id}")
                print(f"Data da Manutenção: {manutencao['Data']}")
                print(f"Descrição: {manutencao['Descrição']}")
                print("-" * 30)
        else:
            print("Nenhuma manutenção registrada.")

    
    @staticmethod
    def apagar_manutencao(id):
        if id in Equipamento._manutencoes:
            del Equipamento._manutencoes[id]
            print(f"Manutenção do equipamento {id} realizado!.")
        else:
            print("Nenhuma manutenção encontrada para o ID fornecido.")


    @property
    def equipamentos(self):
        return self._equipamentos

    @property
    def nome(self):
        return self._nome

    @property
    def valor(self):
        return self._valor

    @property
    def id(self):
        return self._id

    @property
    def descricao(self):
        return self._descricao

    @property
    def data_registro(self):
        return self._data_registro