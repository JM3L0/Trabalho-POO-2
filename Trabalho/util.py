RED = '\033[31m'
GREEN = '\033[32m'
RESET = '\033[0m'

def ordenar_quartos(lista):
    return sorted(lista)

    
def captura_cpf():
    
    cpf = input("Digite o CPF (somente números): ")
    
    while not (cpf.isdigit() and len(cpf) == 11):
        print(RED + "\nCPF inválido. Deve ser um número de 11 caracteres." + RESET)
        cpf = input("Digite o CPF (somente números): ")
        
    return cpf  # Retorna o CPF válido como string

def imprimir_cpf(cpf):
    if cpf.isdigit() and len(cpf) == 11:
        return f"CPF: {cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    else:
        return "CPF inválido."
        
def capturar_senha():
    
    senha = input("Digite a senha (mínimo 3 caracteres): ")
    
    while len(senha) < 3:
        print(RED + "\nSenha inválida. Deve ter pelo menos 3 caracteres." + RESET)
        senha = input("Digite a senha (mínimo 3 caracteres): ")
        
    return senha  # Retorna a senha válida

def existe_funcionario(funcionarios, cpf):
    
    if cpf in funcionarios:
        return funcionarios[cpf]

    return None  # Retorna None se o funcionário não existir