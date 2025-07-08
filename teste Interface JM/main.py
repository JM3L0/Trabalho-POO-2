import models as md
import services as sv
import util

RED = '\033[31m'
GREEN = '\033[32m'
RESET = '\033[0m'

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
    
    
def instacia_funcionarios(gerente):
        
    gerente.adicionar_funcionario("FUNCIONARIO P", "11111111111", "123")
    gerente.adicionar_funcionario("LUIS", "22222222222", "123")
    gerente.adicionar_funcionario("MARIA", "33333333333", "123")
    gerente.adicionar_funcionario("ANA", "44444444444", "123")
    gerente.adicionar_funcionario("SEU ZÉ", "55555555555", "123")

    # return checkin, checkout, gerente


def menu_principal():
    sistema = sv.Sistema()
    checkin = sv.CheckIn()
    checkout = sv.CheckOut()
    
    gerente = md.Gerente("GERENTE GERAL", "00000000000", "321") #nunca, sob nenhuma circunstância apague este cara
    instacia_funcionarios(gerente)

    while True:
        menu_inicial()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            
            print("\n=== Login como Gerente ===")
            senha = util.capturar_senha()
            
            if sistema.login(gerente, senha):
                print(GREEN + "\nLogin realizado com sucesso como Gerente!" + RESET)
                while True:
                    menu_gerente()
                    opcao_gerente = input("Escolha uma opção: ")

                    if opcao_gerente == "1":
                        
                        nome = input("\nNome do funcionário: ").upper()
                        cpf = util.captura_cpf()
                        senha = util.capturar_senha()
                        
                        gerente.adicionar_funcionario(nome, cpf, senha)
                        
                    elif opcao_gerente == "2":
                        cpf = util.captura_cpf()
                        gerente.remover_funcionario(cpf)
                        
                    elif opcao_gerente == "3":
                        gerente.listar_funcionarios()
                        
                    elif opcao_gerente == "4":
                        gerente.imprimir_historico_gerente()
                        
                    elif opcao_gerente == "0":
                        print(GREEN + "\nLogout do Gerente realizado." + RESET)
                        break
                    else:
                        print(RED + "\nOpção inválida! Tente novamente." + RESET)
            else:
                print(RED + "\nSenha incorreta!" + RESET)

        elif opcao == "2":
            cpf = util.captura_cpf()
            senha = util.capturar_senha()
            
            print("\n=== Login como Funcionário ===")
            funcionario = util.existe_funcionario(gerente.funcionarios, cpf)
            
            if funcionario and sistema.login(funcionario, senha):
                print(GREEN + f"\nLogin realizado com sucesso como {funcionario.nome}!" + RESET)
                while True:
                    menu_funcionario()
                    opcao_funcionario = input("Escolha uma opção: ")

                    if opcao_funcionario == "1":
                        try:
                            nome = input("\nNome do hóspede: ").upper()
                            cpf = util.captura_cpf()
                            
                            try:
                                quarto = int(input("Número do quarto (1 a 10): "))
                                
                                if quarto not in range(1, 11):
                                    print(RED + "\nNúmero do quarto inválido. Deve estar entre 1 e 10." + RESET)
                                    continue
                                
                            except ValueError:
                                print(RED + "\nEntrada inválida. O número do quarto deve ser um número inteiro." + RESET)
                                continue
                            
                            hospede = md.Hospede(nome, cpf, quarto)
                            funcionario.registrar_hospede(checkin, hospede)
                            
                        except ValueError:
                            print(RED + "\nEntrada inválida. O número do quarto deve ser um número inteiro." + RESET)

                    elif opcao_funcionario == "2":
                        funcionario.listar_hospedes(checkin)
                        
                    elif opcao_funcionario == "3":
                        funcionario.listar_quartos_disponiveis(checkin)
                        
                    elif opcao_funcionario == "4":
                        cpf = util.captura_cpf()
                        checkout.remover_hospede(cpf, checkin, funcionario, nome)
                        
                    elif opcao_funcionario == "5":
                        
                        print(f"\nHistórico de ações do funcionário {funcionario.nome}")
                        if not funcionario.historico:
                            print("\nNenhuma ação realizada.")
                        else:
                            for acao in funcionario.historico:
                                print(acao)
                                
                    elif opcao_funcionario == "0":
                        print(GREEN + "\nLogout do Funcionário realizado." + RESET)
                        break
                    else:
                        print(RED + "\nOpção inválida! Tente novamente." + RESET)
            else:
                if not funcionario:
                    print(RED + "\nFuncionário não encontrado." + RESET)
                else:
                    print(RED + "\nSenha incorreta!" + RESET)
        elif opcao == "0":
            print(GREEN + "\nSaindo do sistema..." + RESET)
            break
        else:
            print(RED + "\nOpção inválida! Tente novamente." + RESET)

if __name__ == "__main__":
    menu_principal()