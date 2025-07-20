import os
import time
from datetime import datetime
from abc import ABC, abstractmethod

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar():
    input("\nPressione Enter para continuar...")

def aguardar():
    time.sleep(1.5)

def pegar_conta_cliente(cliente):
    if not cliente.contas:
        print("\nCliente nao possui conta!")
        return

    # FIXME: nao permite cliente escolher a conta
    return cliente.contas[0]

def validar_cpf(cpf):
    cpf_valido = cpf.strip().replace(".", "").replace("-", "")
    if cpf_valido.isdigit() and len(cpf_valido) == 11:
            return True
    else:
        print("CPF invalido. Deve conter apenas 11 numeros.")
        return False
    
def buscar_cpf(cpf, lista_clientes):
    for cliente in lista_clientes:
        if cliente.cpf == cpf:
            return cliente
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

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)
        
class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\nOperacao falhou! Voce não tem saldo suficiente.")

        elif valor > 0:
            self._saldo -= valor
            timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
            mensagem_saque = f"[{timestamp}] Saque: - R$ {valor:.2f}"
            print(f"{mensagem_saque} realizado com sucesso.")
            aguardar()
            return True

        else:
            print("\nOperacao falhou! O valor informado e invalido.")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
            mensagem_deposito = f"[{timestamp}] Deposito: + R$ {valor:.2f}"
            print(f"{mensagem_deposito} realizado com sucesso.")
            aguardar()
        else:
            print("\n[check] Operacao falhou! O valor informado e invalido.")
            return False

        return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print("\nOperacao falhou! O valor do saque excede o limite.")

        elif excedeu_saques:
            print("\nOperacao falhou! Numero maximo de saques excedido.")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
            Agencia:\t{self.agencia}
            C/C:\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
            }
        )

class Transacao(ABC):
    @property
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Depositar(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

def exibir_extrato(clientes):
    cabecalho_extrato = """
    ======== EXTRATO ========

    """
    limpar_tela()
    print(cabecalho_extrato)
    cpf = input("Informe o CPF do cliente: ")
    cliente = buscar_cpf(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado!")
        return

    conta = pegar_conta_cliente(cliente)
    if not conta:
        return
    
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Nenhuma movimentacao realizada."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\n\nSaldo:\tR$ {conta.saldo:.2f}")
    print("==========================================")
    pausar()

def sacar(clientes):
        # SALDO: {self.saldo:.2f}
        # SAQUES: {numero_saques}
        cabecalho_sacar = f"""
        ======== SACAR ========

        """
        while True:
            limpar_tela()
            print(f"\n{cabecalho_sacar}")
            cpf_cliente = input("Informe o CPF do cliente: ")
            cliente = buscar_cpf(cpf_cliente, clientes)

            if not cliente:
                print("\nCliente nao encontrado!")
                aguardar()
                return
            
            try:
                valor_saque = float(input(f"\n{cliente}, Digite o valor a sacar: "))
                if valor_saque > 0:
                
                    transacao = Saque(valor_saque)

                    conta = pegar_conta_cliente(cliente)
                    if not conta:
                        return

                    cliente.realizar_transacao(conta, transacao)
                    aguardar()
                    return True
            except ValueError:
                print("Entrada invalida. Informe um numero.")
            return False

def listar_contas_corrente(contas):
    cabecalho_listar_contas_corrente = """
    ======== CONTAS CORRENTES ========

    """
    limpar_tela()
    print(cabecalho_listar_contas_corrente)
    if contas:
        for conta in contas:
            print(conta)
            print("=" * 40)
    else:
        print("Nenhuma conta corrente cadastrada.")
        aguardar()
    pausar()

def criar_conta_corrente(numero_conta, clientes, contas):
    cabecalho_criar_conta_corrente = """
    ======== CRIAR CONTA CORRENTE ========

    """
    while True:
        limpar_tela()
        print(cabecalho_criar_conta_corrente)

        while True:
            cpf = "01234567803"
            #cpf = input("Informe o CPF (somente numeros): ").strip()
            if validar_cpf(cpf):
                cliente = buscar_cpf(cpf, clientes)
                if cliente:
                    nova_conta_corrente = True
                    break
            else:
                opcao = input("\nUsuario nao localizado. Deseja tentar novamente? (s para Sim / qualquer tecla para voltar ao menu): ").lower()
                if opcao != 's':
                    nova_conta_corrente = False
                    break
        
        if nova_conta_corrente:
            conta = ContaCorrente.nova_conta(cliente=cliente, numero=str(numero_conta).zfill(4))
            contas.append(conta)
            cliente.contas.append(conta)
            print("\nConta corrente criada com sucesso!")
            aguardar()

        limpar_tela()
        print(cabecalho_criar_conta_corrente)
        opcao = input("\nDeseja criar outra conta corrente? (s para Sim / qualquer tecla para voltar ao menu): ").lower()
        if opcao != 's':
            break

def listar_clientes(clientes):
    cabecalho_listar_usuarios = """
    ======== LISTA DE CLIENTES ========

    """
    limpar_tela()
    print(cabecalho_listar_usuarios)
    if clientes:
        for cliente in clientes:
            print(f"""
Nome: {cliente.nome}
Data de Nascimento: {cliente.data_nascimento}
CPF: {cliente.cpf}
Endereco: {cliente.endereco}
""")
            print("-" * 20)
    else:
        print("Nenhum usuario cadastrado.")
    pausar()

def cadastrar_cliente(clientes):
    cabecalho_cadastrar_clientes = """
    ======== CADASTRAR USUARIOS ========

    """
    while True:
        limpar_tela()
        print(cabecalho_cadastrar_clientes)

        while True:
            cpf = "01234567803"
            #cpf = input("Informe o CPF (somente numeros): ").strip()
            if validar_cpf(cpf) and not buscar_cpf(cpf, clientes):
                novo_cliente = True
                break
            else:
                print("\nJa existe um usuario cadastrado com esse CPF.")
                pausar()
                opcao = input("\nDeseja tentar cadastrar outro usuario? (s para Sim / qualquer tecla para voltar ao menu): ").lower()
                if opcao != 's':
                    novo_cliente = False
                    break
        
        nome = "vini"
        #nome = input("Informe o nome completo: ").strip()

        while True:
            data_nascimento = "09/11/1994"
            #data_nascimento = input("Informe a data de nascimento (DD/MM/AAAA): ").strip()
            if not validar_data_nascimento(data_nascimento):
                print("Data invalida. Utilize o formato DD/MM/AAAA e uma data real.")
                aguardar()
            else:
                break

        while True:    
            endereco = "alcides gomes, 10 - parque dos anjos - gravatai/rs"
            #endereco = input("Informe o endereco (logradouro, nro - bairro - cidade/sigla estado): ").strip()
            if not validar_endereco(endereco):
                print("Endereco invalido. Siga o formato solicitado.")
                aguardar()
            else:
                break

        if novo_cliente:
            cliente = PessoaFisica(nome, data_nascimento, cpf, endereco)
            clientes.append(cliente)
            print("\nUsuario cadastrado com sucesso!")
            aguardar()
        else:
            pass

        limpar_tela()
        print(cabecalho_cadastrar_clientes)
        opcao = input("\nDeseja cadastrar outro usuario? (s para Sim / qualquer tecla para voltar ao menu): ").lower()
        if opcao != 's':
            break

def depositar(clientes):
    cabecalho_depositar = """
    ======== DEPOSITAR ========

    """
    while True:
        limpar_tela
        print(f"\n{cabecalho_depositar}")
        try:
            cpf_cliente = input("Informe o CPF do cliente: ")
            cliente = buscar_cpf(cpf_cliente, clientes)
            if not cliente:
                print("\nCliente nao encontrado!")
                aguardar()
                return
            valor_deposito = float(input(f"\n{cliente}, Digite o valor a depositar: "))
            if valor_deposito > 0:
                
                transacao = Depositar(valor_deposito)
                conta = pegar_conta_cliente(cliente)
                if not conta:
                    return

                cliente.realizar_transacao(conta, transacao)
                return True
            else:
                print("\nValor invalido! Tente novamente.")
                aguardar()
        except ValueError:
            print("\nEntrada invalida! Informe um numero.")
            aguardar()

        return False

def main():
    menu = """
    ======== BANCO PYTHON ========

            [1] Depositar
            [2] Sacar
            [3] Extrato
            [4] Cadastrar Cliente
            [5] Exibir Clientes
            [6] Criar Conta Corrente
            [7] Exibir Contas Corrente
            [0] sair

        => """
    clientes = []
    contas = []

    while True:
        limpar_tela()
        opcao = input(menu)

        if opcao == "1":
            limpar_tela()
            depositar(clientes)
        elif opcao == "2":
            limpar_tela()
            sacar(clientes)
        elif opcao == "3":
            limpar_tela()
            exibir_extrato(clientes)
        elif opcao == "4":
            limpar_tela()
            cadastrar_cliente(clientes)
        elif opcao == "5":
            limpar_tela()
            listar_clientes(clientes)
        elif opcao == "6":
            limpar_tela()
            numero_conta = len(contas) + 1
            criar_conta_corrente(numero_conta, clientes, contas)
        elif opcao == "7":
            limpar_tela()
            listar_contas_corrente(contas)
        elif opcao == "0":
            print("\nObrigado por usar nosso banco. Ate mais!")
            aguardar()
            break
        else:
            print("\nOpcao invalida! Tente novamente.")
            aguardar()

if __name__ == "__main__":
    main()
