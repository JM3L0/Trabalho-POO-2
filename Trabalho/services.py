import models as md
import util

class Sistema:
    def login(self, usuario, senha):
        if isinstance(usuario, md.Autentica):
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
        quartos_disponiveis = util.ordenar_quartos(CheckIn.quartos_disponiveis)
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