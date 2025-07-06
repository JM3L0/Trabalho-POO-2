def ordenar_quartos(lista):
    return sorted(lista)

def verifica_tamanho_senha(senha):
    if len(senha) < 3:
        print("\nSenha muito curta. A senha deve ter no mínimo 3 caracteres.")
        return False
    else:
        return True
    
