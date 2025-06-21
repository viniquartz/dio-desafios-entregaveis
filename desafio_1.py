import os
import time
from datetime import datetime

saldo = 0
valor_limite_saque = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3
          
menu = """
======== BANCO PYTHON ========

        [1] depositar
        [2] sacar
        [3] extrato
        [0] sair

        => 
"""

menu_depositar = """
======== DEPOSITAR ========

"""

menu_extrato = """
======== EXTRATO ========

"""

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar():
    input("\nPressione Enter para continuar...")

def aguardar():
    time.sleep(1.5)

def depositar_function():
    global saldo, extrato

    while True:
        limpar_tela()
        try:
            valor_deposito = float(input(f"\n{menu_depositar}Digite o valor a depositar: "))
            if valor_deposito > 0:
                saldo += valor_deposito
                timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
                mensagem_deposito = f"[{timestamp}] Deposito: + R$ {valor_deposito:.2f}"
                extrato += f"{mensagem_deposito}\n"
                print(f"{mensagem_deposito} realizado com sucesso.")
                aguardar()
                break
            else:
                print("\nValor invalido! Tente novamente.")
                aguardar()
        except ValueError:
            print("\nEntrada invalida! Informe um numero.")
            aguardar()

def sacar_function():
    global saldo, valor_limite_saque, extrato, numero_saques, LIMITE_SAQUES
    menu_sacar = f"""
    ======== SACAR ========

    SALDO: {saldo:.2f}
    SAQUES: {numero_saques}

    """

    while True:
        limpar_tela()
        print(menu_sacar)
        if saldo > 0 and numero_saques < 3:
            try:
                valor_saque = float(input(f"\nDigite o valor a sacar: "))
                if valor_saque > 0 and valor_saque <= valor_limite_saque and valor_saque <= saldo:
                    saldo -= valor_saque
                    numero_saques = numero_saques + 1
                    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
                    mensagem_saque = f"[{timestamp}] Saque: - R$ {valor_saque:.2f}"
                    extrato += f"{mensagem_saque}\n"
                    print(f"{mensagem_saque} realizado com sucesso.")
                    aguardar()
                    break
                elif valor_saque > valor_limite_saque:
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
        elif numero_saques == LIMITE_SAQUES:
            print("\nLimite de saque! Voce ja executou o numero limite de saques diarios.")
            aguardar()
            break

def extrato_function():
    limpar_tela()
    print(menu_extrato)
    if extrato:
        print(extrato)
    else:
        print("Nenhuma movimentacao realizada.")
    print(f"\nSaldo atual: R$ {saldo:.2f}")
    pausar()

while True:
    limpar_tela()
    opcao = input(menu)

    if opcao == "1":
        limpar_tela()
        depositar_function()
    elif opcao == "2":
        limpar_tela()
        sacar_function()
    elif opcao == "3":
        limpar_tela()
        extrato_function()
    elif opcao == "0":
        print("Obrigado por usar nosso banco. Ate mais!")
        aguardar()
        break
    else:
        print("\nOpcao invalida! Tente novamente.")
        aguardar()