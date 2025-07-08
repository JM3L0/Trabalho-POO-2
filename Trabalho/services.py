import models as md
import util

RED = '\033[31m'
GREEN = '\033[32m'
RESET = '\033[0m'

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
            print(RED + "\nCPF inválido. Deve ser um número de 11 caracteres." + RESET)
            return False
        if hospede.cpf in CheckIn.hospedes:
            print(RED + "\nCPF já cadastrado para outro hóspede." + RESET)
            return False
        if hospede.quarto in CheckIn.quartos_disponiveis:
            CheckIn.hospedes[hospede.cpf] = hospede
            CheckIn.quartos_disponiveis.remove(hospede.quarto)
            print(GREEN + f"\nHóspede {hospede.nome} registrado no quarto {hospede.quarto}." + RESET)
            return True
        else:
            print(RED + f"\nO quarto {hospede.quarto} não está disponível." + RESET)
            return False

    def listar_hospedes(self):
        if not CheckIn.hospedes:
            print(RED + "\nNenhum hóspede registrado." + RESET)
            return False
        else:
            print("\nLista de Hóspedes:")
            for hospede in CheckIn.hospedes.values():
                print(f"Nome: {hospede.nome}\n{util.imprimir_cpf(hospede.cpf)}\nQuarto: {hospede.quarto}\n")

    def listar_quartos_disponiveis(self):
        quartos_disponiveis = util.ordenar_quartos(CheckIn.quartos_disponiveis)
        print(f"\nQuartos disponíveis: {quartos_disponiveis}")

class CheckOut:
    def __init__(self):
        pass
    
    def remover_hospede(self, cpf, checkin, funcionario, nome):
        if not cpf.isdigit() or len(cpf) != 11:
            print(RED + "\nCPF inválido. Deve ser um número de 11 caracteres." + RESET)
            return False
        if cpf in checkin.hospedes:
            checkin.quartos_disponiveis.append(checkin.hospedes[cpf].quarto)
            del checkin.hospedes[cpf]
            print(GREEN + f"\nHóspede com CPF {cpf} removido com sucesso." + RESET)
            funcionario.historico.append(f"Funcionário ({funcionario.nome}) fez o checkout do hóspede ({nome}).")
            return True
        else:
            print(RED + f"\nNenhum hóspede com CPF {cpf} foi encontrado." + RESET)
            return False