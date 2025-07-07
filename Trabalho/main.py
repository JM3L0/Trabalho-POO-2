import models as md
import services as sv
import util

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
    
    
def povoar_sistema():
    sistema = sv.Sistema()
    checkin = sv.CheckIn()
    checkout = sv.CheckOut()


    # O Gerente é o núcleo do sistema do gerente. Ele não deve ser removido sob nenhuma circunstância.
    gerente = md.Gerente("Gerente Geral", "00000000000", "123")
        
    gerente.adicionar_funcionario("Funcionário Padrão", "11111111111", "123")
    gerente.adicionar_funcionario("Luis", "22222222222", "123")
    gerente.adicionar_funcionario("Maria", "33333333333", "123")
    gerente.adicionar_funcionario("Ana", "44444444444", "123")
    gerente.adicionar_funcionario("João", "55555555555", "123")

    return sistema, checkin, checkout, gerente


def menu_principal():
    # sistema = sv.Sistema()
    # checkin = sv.CheckIn()
    # checkout = sv.CheckOut()

    # # O Gerente é o núcleo do sistema do gerente. Ele não deve ser removido sob nenhuma circunstância.
    # gerente = md.Gerente("Gerente Geral", "00000000000", "123")    
    # gerente.adicionar_funcionario("Funcionário Padrão", "11111111111", "123")
    
    sistema, checkin, checkout, gerente = povoar_sistema()

    while True:
        menu_inicial()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            
            print("\n=== Login como Gerente ===")
            senha = util.capturar_senha()
            
            if sistema.login(gerente, senha):
                print("\nLogin realizado com sucesso como Gerente!")
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
                        print("\nLogout do Gerente realizado.")
                        break
                    else:
                        print("\nOpção inválida! Tente novamente.")
            else:
                print("\nSenha incorreta!")
                
        elif opcao == "2":
            cpf = util.captura_cpf()
            senha = util.capturar_senha()
            
            print("\n=== Login como Funcionário ===")
            funcionario = util.existe_funcionario(gerente.funcionarios, cpf)
            
            if funcionario and sistema.login(funcionario, senha):
                print(f"\nLogin realizado com sucesso como {funcionario.nome}!")
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
                                    print("\nNúmero do quarto inválido. Deve estar entre 1 e 10.")
                                    continue
                            except ValueError:
                                print("\nEntrada inválida. O número do quarto deve ser um número inteiro.")
                                continue
                            hospede = md.Hospede(nome, cpf, quarto)
                            funcionario.registrar_hospede(checkin, hospede)
                        except ValueError:
                            print("\nEntrada inválida. O número do quarto deve ser um número inteiro.")
                            
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
                        print("\nLogout do Funcionário realizado.")
                        break
                    else:
                        print("\nOpção inválida! Tente novamente.")
            else:
                if not funcionario:
                    print("\nFuncionário não encontrado.")
                else:
                    print("\nSenha incorreta!")
        elif opcao == "0":
            print("\nSaindo do sistema...")
            break
        else:
            print("\nOpção inválida! Tente novamente.")

if __name__ == "__main__":
    menu_principal()