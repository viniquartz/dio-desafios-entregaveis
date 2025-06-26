import os
import time
from datetime import datetime

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar():
    input("\nPressione Enter para continuar...")

def aguardar():
    time.sleep(1.5)

def validar_cpf(cpf):
    cpf_valido = cpf.strip().replace(".", "").replace("-", "")
    if cpf_valido.isdigit() and len(cpf_valido) == 11:
            return True
    else:
        print("CPF invalido. Deve conter apenas 11 numeros.")
        return False
    
def buscar_cpf(cpf, lista_usuarios):
    for usuario in lista_usuarios:
        if usuario['cpf'] == cpf:
            return usuario
        else:
            return False

def validar_endereco(endereco):
    try:
        logradouro, restante = endereco.split(",", 1)
        nro, restante = restante.split("-", 1)
        bairro, cidade_estado = restante.split("-", 1)
        
        return all(part.strip() for part in [logradouro, nro, bairro, cidade_estado])
    except ValueError:
        return False

def validar_data_nascimento(data):
    try:
        datetime.strptime(data, "%d/%m/%Y")
        return True
    except ValueError:
        return False

def cadastrar_usuario(lista_usuarios):
    cabecalho_cadastrar_usuarios = """
    ======== CADASTRAR USUARIOS ========

    """
    while True:
        limpar_tela()
        print(cabecalho_cadastrar_usuarios)

        while True:
            # cpf = "01234567803"
            cpf = input("Informe o CPF (somente numeros): ").strip()
            if validar_cpf(cpf) and not buscar_cpf(cpf, lista_usuarios):
                novo_usuario = True
                break
            else:
                print("\nJa existe um usuario cadastrado com esse CPF.")
                pausar()
                opcao = input("\nDeseja tentar cadastrar outro usuario? (s para Sim / qualquer tecla para voltar ao menu): ").lower()
                if opcao != 's':
                    novo_usuario = False
                    break
        
        # nome = "vini"
        nome = input("Informe o nome completo: ").strip()

        while True:
            # data_nascimento = "09/11/1994"
            data_nascimento = input("Informe a data de nascimento (DD/MM/AAAA): ").strip()
            if not validar_data_nascimento(data_nascimento):
                print("Data invalida. Utilize o formato DD/MM/AAAA e uma data real.")
                aguardar()
            else:
                break

        while True:    
            # endereco = "alcides gomes, 10 - parque dos anjos - gravatai/rs"
            endereco = input("Informe o endereco (logradouro, nro - bairro - cidade/sigla estado): ").strip()
            if not validar_endereco(endereco):
                print("Endereco invalido. Siga o formato solicitado.")
                aguardar()
            else:
                break

        if novo_usuario:
            usuario = {
                "nome": nome,
                "data_nascimento": data_nascimento,
                "cpf": cpf,
                "endereco": endereco
            }
            lista_usuarios.append(usuario)
            print("\nUsuario cadastrado com sucesso!")
            aguardar()
        else:
            pass

        limpar_tela()
        print(cabecalho_cadastrar_usuarios)
        opcao = input("\nDeseja cadastrar outro usuario? (s para Sim / qualquer tecla para voltar ao menu): ").lower()
        if opcao != 's':
            break
    
    return lista_usuarios

def listar_usuarios(lista_usuarios):
    cabecalho_listar_usuarios = """
    ======== LISTA USUARIOS ========

    """
    limpar_tela()
    print(cabecalho_listar_usuarios)
    if lista_usuarios:
        for usuarios in lista_usuarios:
            print(f"""
Nome: {usuarios['nome']}
Data de Nascimento: {usuarios['data_nascimento']}
CPF: {usuarios['cpf']}
Endereco: {usuarios['endereco']}
""")
            print("-" * 20)
    else:
        print("Nenhum usuario cadastrado.")
    pausar()

def criar_conta_corrente(lista_conta_corrente, lista_usuarios):
    cabecalho_criar_conta_corrente = """
    ======== CRIAR CONTA CORRENTE ========

    """
    while True:
        limpar_tela()
        print(cabecalho_criar_conta_corrente)

        while True:
            # cpf = "01234567803"
            cpf = input("Informe o CPF (somente numeros): ").strip()
            if validar_cpf(cpf):
                usuario = buscar_cpf(cpf, lista_usuarios)
                if usuario:
                    nova_conta_corrente = True
                    break
            else:
                opcao = input("\nUsuario nao localizado. Deseja tentar novamente? (s para Sim / qualquer tecla para voltar ao menu): ").lower()
                if opcao != 's':
                    nova_conta_corrente = False
                    break
        

        if nova_conta_corrente:
            numero_conta = len(lista_conta_corrente) + 1
            conta_corrente = {
                "agencia": "0001",
                "numero_conta": str(numero_conta).zfill(4),
                "usuario": usuario
            }
            lista_conta_corrente.append(conta_corrente)
            print("\nConta corrente criada com sucesso!")
            aguardar()
        else:
            pass

        limpar_tela()
        print(cabecalho_criar_conta_corrente)
        opcao = input("\nDeseja criar outra conta corrente? (s para Sim / qualquer tecla para voltar ao menu): ").lower()
        if opcao != 's':
            break

def listar_contas_corrente(lista_conta_corrente):
    cabecalho_listar_contas_corrente = """
    ======== CONTAS CORRENTES ========

    """
    limpar_tela()
    print(cabecalho_listar_contas_corrente)
    if lista_conta_corrente:
        for contas in lista_conta_corrente:
            print(f"""
Agencia: {contas['agencia']}
C/C: {contas['numero_conta']}
NOME TITULAR: {contas['usuario']['nome']}
""")
            print("-" * 20)
    else:
        print("Nenhuma conta corrente cadastrada.")
    pausar()

def depositar_function(saldo, extrato, /):
    cabecalho_depositar = """
    ======== DEPOSITAR ========

    """
    while True:
        limpar_tela()
        try:
            valor_deposito = float(input(f"\n{cabecalho_depositar}Digite o valor a depositar: "))
            if valor_deposito > 0:
                saldo += valor_deposito
                timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
                mensagem_deposito = f"[{timestamp}] Deposito: + R$ {valor_deposito:.2f}"
                extrato += f"{mensagem_deposito}\n"
                print(f"{mensagem_deposito} realizado com sucesso.")
                aguardar()
                return saldo, extrato
            else:
                print("\nValor invalido! Tente novamente.")
                aguardar()
        except ValueError:
            print("\nEntrada invalida! Informe um numero.")
            aguardar()

def sacar_function(*, saldo, valor, extrato, numero_saques, limite_saques):
    cabecalho_sacar = f"""
    ======== SACAR ========

    SALDO: {saldo:.2f}
    SAQUES: {numero_saques}

    """

    while True:
        limpar_tela()
        print(cabecalho_sacar)
        if saldo > 0 and numero_saques < 3:
            try:
                valor_saque = float(input(f"\nDigite o valor a sacar: "))
                if valor_saque > 0 and valor_saque <= valor and valor_saque <= saldo:
                    saldo -= valor_saque
                    numero_saques = numero_saques + 1
                    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
                    mensagem_saque = f"[{timestamp}] Saque: - R$ {valor_saque:.2f}"
                    extrato += f"{mensagem_saque}\n"
                    print(f"{mensagem_saque} realizado com sucesso.")
                    aguardar()
                    return saldo, extrato, numero_saques
                elif valor_saque > valor:
                     print("Valor excedeu seu valor limite maximo de saque. Tente novamente.")
                     aguardar()
                elif valor_saque > saldo:
                     print("Valor desejado e superior ao saldo. Tente novamente.")
                     aguardar()
            except ValueError:
                print("Entrada invalida. Informe um numero.")
        elif saldo == 0:
            print("\nSaldo zerado! Voce nao pode realizar saques.")
            aguardar()
            break
        elif numero_saques == limite_saques:
            print("\nLimite de saque! Voce ja executou o numero limite de saques diarios.")
            aguardar()
            break

def extrato_function(saldo, /, *, extrato):
    cabecalho_extrato = """
    ======== EXTRATO ========

    """
    limpar_tela()
    print(cabecalho_extrato)
    if extrato:
        print(extrato)
    else:
        print("Nenhuma movimentacao realizada.")
    print(f"\nSaldo atual: R$ {saldo:.2f}")
    pausar()

def main():
    menu = """
    ======== BANCO PYTHON ========

            [1] depositar
            [2] sacar
            [3] extrato
            [4] Cadastrar usuario
            [5] listar usuarios
            [6] criar conta corrente
            [7] listar contas corrente
            [0] sair

        => """
    saldo = 0
    valor_limite_saque = 500
    extrato = ""
    numero_saques = 0
    LIMITE_SAQUES = 3
    lista_usuarios = []
    lista_conta_corrente = []

    while True:
        limpar_tela()
        opcao = input(menu)

        if opcao == "1":
            limpar_tela()
            saldo, extrato = depositar_function(saldo, extrato)
        elif opcao == "2":
            limpar_tela()
            saldo, extrato, numero_saques = sacar_function(saldo=saldo, valor=valor_limite_saque, extrato=extrato, numero_saques=numero_saques, limite_saques=LIMITE_SAQUES)
        elif opcao == "3":
            limpar_tela()
            extrato_function(saldo, extrato=extrato)
        elif opcao == "4":
            limpar_tela()
            lista_usuarios = cadastrar_usuario(lista_usuarios)
        elif opcao == "5":
            limpar_tela()
            listar_usuarios(lista_usuarios)
        elif opcao == "6":
            limpar_tela()
            criar_conta_corrente(lista_conta_corrente, lista_usuarios)
        elif opcao == "7":
            limpar_tela()
            listar_contas_corrente(lista_conta_corrente)
        elif opcao == "0":
            print("\nObrigado por usar nosso banco. Ate mais!")
            aguardar()
            break
        else:
            print("\nOpcao invalida! Tente novamente.")
            aguardar()

if __name__ == "__main__":
    main()
