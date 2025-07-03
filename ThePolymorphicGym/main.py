from gym import Gym
from pessoa import Pessoa
from funcionario import Funcionario
from aluno import Aluno
from equipamentos import Equipamento 
from caixa import Caixa

academia = Gym()
caixa = Caixa()
while True:
    print("\n=== Seja muito bem-vindo à ThePolymorphicGym ===")
    print("1. Cadastrar Aluno")
    print("2. Cadastrar Funcionário")
    print("3. Cadastrar novo Equipamento")
    print("4. Realizar Pagamento")
    print("5. Registrar Entrada no Caixa")
    print("6. Registrar Saída no Caixa")
    print("7. Exibir Histórico de Transações")
    print("8. Listar Alunos ou Funcionários")
    print("9. Listar Equipamentos")
    print("10. Exibir Informações de Alunos ou Funcionários")
    print("11. Agendar Manutenção de equipamento")
    print("12. Manutenções agendadas")
    print("13. Registrar manutenção realizada")
    print("14. Consultar o Caixa")
    print("15. Sair")
    opcao = input("\nEscolha uma opção: ")

    if opcao == "1":

        print("\n------------------------------------------------\n")
        nome = input("Nome do Aluno: ")
        while True:
            try:
                idade = int(input("Idade: "))
                break 
            except ValueError:
                print("Entrada inválida. Por favor, digite uma idade válida.")

        endereco = input("Endereço: ")
        telefone = input("Telefone: ")
        email = input("E-mail: ")
        cpf = input("CPF: ")

        print("\n INFORMAÇÕES DOS PLANOS\n")
        print("Mensal: Valor: R$120, deve ser renovada a cada 1 mes")
        print("Trimestral: Valor: R$300, um desconto de R$60, deve ser renovado a cada 3 meses")
        print("Anual: Valor: R$1000, Tem um desconto de R$440, Deve ser renovado a cada 12 meses\n")
        print("\n 1. Mensal\n 2. Trimestral\n 3. Anual\n")
        

        while True:
            planoescolha = input("Escolha o plano: ")
            if planoescolha == '1':
                plano = "Mensal"
                break
            elif planoescolha == '2':
                plano = "Trimestral"
                break
            elif planoescolha == '3':
                plano = "Anual"
                break
            else:
                print("Entrada inválida. Por favor, digite uns dos número acima.")


        if Gym.buscar_planos(plano):
            plano = Gym.buscar_planos(plano)
            aluno = Aluno(nome, idade, endereco, telefone, email, cpf, plano)
            print(f"Aluno {nome} adicionado com sucesso!")
            print("\n------------------------------------------------\n")

        else:
            print("--Plano inválido--.")



    elif opcao == "2":
        # Adicionar Funcionário
        print("\n------------------------------------------------\n")
        nome = input("Nome do Funcionário: ")
        
        while True:
            try:
                idade = int(input("Idade: "))
                break 
            except ValueError:
                print("Entrada inválida. Por favor, digite uma idade válida.")


        endereco = input("Endereço: ")
        telefone = input("Telefone: ")
        email = input("E-mail: ")
        cpf = input("CPF: ")

        while True:
            try:
                salario = float(input("Salário: R$"))
                break
            except ValueError:
                print("Entrada inválida. Por favor, digite um valor válido.")

        funcionario = Funcionario(nome, idade, endereco, telefone, email, cpf, salario)
        print(f"Funcionário {nome} adicionado com sucesso!")
        print("\n------------------------------------------------\n")




    elif opcao == "3":

        # Adicionar Equipamento
        print("\n------------------------------------------------\n")
        nome = input("Nome do Equipamento: ")
        while True:
            try:
                valor = float(input("Valor de compra: R$"))
                break
            except ValueError:
                print("Entrada inválida. Por favor, digite um valor válido.")

        id_equipamento = input("ID do Equipamento: ")
        descricao = input("Descrição (opcional): ")

        equipamento = Equipamento(nome, valor, id_equipamento, descricao)
        print(f"Equipamento {nome} adicionado com sucesso!")

    elif opcao == "4":
        print("\n------------------------------------------------\n")
        aluno = input("Digite o nome do Aluno que deseja realizar o pagamento: ")
        Caixa.realizar_pagamento(aluno)
        print("\n------------------------------------------------\n")


    elif opcao == "5":
        # Registrar Entrada no Caixa
        valor = float(input("Valor da Entrada: R$ "))
        descricao = input("Descrição da Entrada: ")
        Caixa.registrar_entrada(valor, descricao)
        print("Entrada registrada com sucesso!")
        print("\n------------------------------------------------\n")


    elif opcao == "6":
        # Registrar Saída no Caixa
        print("\n------------------------------------------------\n")

        valor = float(input("Valor da Saída: R$ "))
        descricao = input("Descrição da Saída: ")
        Caixa.registrar_saida(valor, descricao)
        print("Saída registrada com sucesso!")
        print("\n------------------------------------------------\n")


    elif opcao == "7":
        # Exibir Histórico de Transações
        print("\n------------------------------------------------\n")
        Caixa.exibir_historico()
        print("\n------------------------------------------------\n")


    elif opcao == "8":
        # Listar Alunos e Funcionários
        tipopessoa = input("Escolha uma opção: \n 1. Alunos\n 2. Funcionários")
        if tipopessoa == '1':
            print("\n------------------------------\n")
            print("\n=== Lista de Alunos ===")
            Aluno.listar_pessoas()
        else: 
            print("\n---------------------------------\n")
            print("\n=== Lista de Funcionarios ===")
            Funcionario.listar_pessoas()

    elif opcao == "9":
        # Listar Equipamentos
        print("\n---------------------------------\n")
        print("\n=== Lista de Equipamentos ===")
        Equipamento.listar_equipamentos()
        print("\n---------------------------------\n")
    
    elif opcao == "10":
        print("\n1. Aluno\n2. Funcionário\n")
        tipopessoa = input("Escolha uma opção: ")
        if tipopessoa == '1':
            nome = input("Digite o nome do Aluno: ")
            print("\n---------------------------------\n")
            aluno = Aluno.buscar_pessoa(nome)
            Aluno.exibir_informacoes(aluno)
        
        if tipopessoa == '2':
            nome = input("Digite o nomde do funcionário: ")
            funcionario = Funcionario.buscar_pessoa(nome)
            print("\n---------------------------------\n")
            Funcionario.exibir_informacoes(funcionario)


    elif opcao == "11":
        id = input("Digite o ID do equipamento que precisa de manutenção: ")
        equipamento = Equipamento.buscar_equipamento(id)
        if equipamento:
            Equipamento.agendar_manutencao(id)
            print("--Agendamento de manutenção realizado com sucesso!--")
        else:
            print("--Equipamento não localizado!--")


    elif opcao == "12":
        Equipamento.listar_manutencoes()

    elif opcao == "13":
        id = input("Digite o ID do Equipameto que foi realizado a manutenção: ")
        Equipamento.apagar_manutencao(id)


    elif opcao == "14":

        Caixa.consultar_caixa()

    elif opcao == "15":
        # Sair
        print("Encerrando o sistema...")
        break

    else:
        print("Opção inválida. Tente novamente.")
