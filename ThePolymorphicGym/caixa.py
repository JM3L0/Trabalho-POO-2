from datetime import datetime
from aluno import Aluno


class Caixa:

    
    _montante = 0.0
    _transacoes = []

    def __init__(self):
        self._transacoes 
        self._montante


    @staticmethod
    def registrar_entrada(valor, descricao=""):
        data_hora = datetime.now()
        Caixa._transacoes.append({"tipo": "entrada", "valor": valor, "descricao": descricao, "data": data_hora})
        Caixa._montante += valor
        print(f"Entrada de R$ {valor:.2f} registrada com sucesso. Montante atual: R$ {Caixa._montante:.2f}")



    @staticmethod
    def registrar_saida(valor, descricao=""):
        data_hora = datetime.now()
        Caixa._transacoes.append({"tipo": "saida", "valor": valor, "descricao": descricao, "data": data_hora})
        Caixa._montante -= valor
        print(f"Saída de R$ {valor:.2f} registrada com sucesso. Montante atual: R$ {Caixa._montante:.2f}")


    @staticmethod
    def exibir_historico():
        print("\n=== Histórico de Transações ===")
        for transacao in Caixa._transacoes:
            print(f"Tipo: {transacao['tipo'].capitalize()}, Valor: R$ {transacao['valor']:.2f}, "
                  f"Descrição: {transacao['descricao']}, Data: {transacao['data'].strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"\nMontante atual: R$ {Caixa._montante:.2f}")



    def realizar_pagamento(nome_aluno):
        aluno = Aluno.buscar_pessoa(nome_aluno)
        if not aluno:
            print("Aluno não encontrado! Certifique-se de que o cadastro foi realizado.")
            return
        
        plano = aluno.plano
        valor_plano = plano.get("valor")
        duracao = plano.get("duracao")

        if not valor_plano:
            print("Plano inválido ou não configurado.")
            return
        
        print(f"Plano selecionado: {duracao} meses - Valor: R$ {valor_plano:.2f}")
        forma_pagamento = input("Escolha a forma de pagamento:\n1. Cartão\n2. Pix\n3. Dinheiro\nOpção: ")

        if forma_pagamento in {"1", "2", "3"}:
            confirmacao = input("Deseja confirmar o pagamento? (s/n): ").strip().lower()
            if confirmacao == "s":
                Caixa.registrar_entrada(valor_plano, f"Pagamento de plano {duracao} meses - Aluno: {nome_aluno}")
                print("Pagamento realizado com sucesso!")
            else:
                print("Pagamento não realizado. Está pendente.")
        else:
            print("Forma de pagamento inválida.")



    def consultar_caixa():
        total_entradas = sum(transacao["valor"] for transacao in Caixa._transacoes if transacao["tipo"] == "entrada")
        total_saidas = sum(transacao["valor"] for transacao in Caixa._transacoes if transacao["tipo"] == "saida")

        print("\n=== Consulta do Caixa ===")
        print(f"Montante atual: R$ {Caixa._montante:.2f}")
        print(f"Total de entradas: R$ {total_entradas:.2f}")
        print(f"Total de saídas: R$ {total_saidas:.2f}")
        print("==========================\n")