from abc import ABC, abstractmethod
from datetime import datetime


class Cliente:
    def __init__(self, nome: str, endereco: str):
        self.nome = nome
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta: 'Conta', transacao: 'Transacao'):
        """Realiza uma transação em uma conta específica."""
        transacao.registrar(conta)

    def adicionar_conta(self, conta: 'Conta'):
        """Adiciona uma conta à lista de contas do cliente."""
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome: str, data_nascimento: str, cpf: str, endereco: str):
        super().__init__(nome, endereco)
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Conta:
    def __init__(self, numero: int, cliente: 'Cliente'):
        self._saldo: float = 0.0  # Atributo privado
        self._numero: int = numero  # Atributo privado
        self._agencia: str = "0001"  # Atributo privado
        self._cliente: Cliente = cliente  # Atributo privado (cliente)
        self._historico: Historico = Historico()  # Atributo privado (historico)

    @property
    def saldo(self) -> float:
        """Retorna o saldo da conta."""
        return self._saldo

    @property
    def numero(self) -> int:
        """Retorna o número da conta."""
        return self._numero

    @property
    def agencia(self) -> str:
        """Retorna a agência da conta."""
        return self._agencia

    @property
    def cliente(self) -> 'Cliente':
        """Retorna o cliente associado à conta."""
        return self._cliente

    @property
    def historico(self) -> 'Historico':
        """Retorna o histórico de transações da conta."""
        return self._historico

    @classmethod
    def nova_conta(cls, cliente: 'Cliente', numero: int) -> 'Conta':
        """Cria uma nova conta para o cliente."""
        return cls(numero, cliente)

    def sacar(self, valor: float) -> bool:
        """Saca um valor da conta, se houver saldo suficiente."""
        if valor <= 0:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

        if valor > self._saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
            return False

        self._saldo -= valor
        print("\n=== Saque realizado com sucesso! ===")
        return True

    def depositar(self, valor: float) -> bool:
        """Deposita um valor na conta."""
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False


class ContaCorrente(Conta):
    def __init__(self, numero: int, cliente: 'Cliente', limite: float = 500, limite_saques: int = 3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor: float) -> bool:
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if isinstance(transacao, Saque)]
        )

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
            return False
        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
            return False
        else:
            return super().sacar(valor)

    def __str__(self) -> str:
        return f"""\nAgência: {self.agencia}\nC/C: {self.numero}\nTitular: {self.cliente.nome}\n"""


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self) -> list:
        return self._transacoes

    def adicionar_transacao(self, transacao: 'Transacao'):
        self._transacoes.append(transacao)

    def exibir_transacoes(self):
        for transacao in self._transacoes:
            print(f"Tipo: {transacao.__class__.__name__}, Valor: {transacao.valor}, Data: {transacao.data}")


class Transacao(ABC):
    def __init__(self, valor: float):
        self.valor = valor
        self.data = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    @abstractmethod
    def registrar(self, conta: 'Conta'):
        pass


class Saque(Transacao):
    def registrar(self, conta: 'Conta'):
        sucesso_transacao = conta.sacar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def registrar(self, conta: 'Conta'):
        sucesso_transacao = conta.depositar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


# Testando o sistema bancário
cliente = PessoaFisica(nome="Caique", data_nascimento="31-20-1993", cpf="12345678900", endereco="Rua 1")
conta_corrente = ContaCorrente.nova_conta(cliente, numero=1001)

cliente.adicionar_conta(conta_corrente)

# Realizando depósitos e saques
deposito = Deposito(1000)
cliente.realizar_transacao(conta_corrente, deposito)

saque = Saque(200)
cliente.realizar_transacao(conta_corrente, saque)

# Exibindo o histórico de transações
conta_corrente.historico.exibir_transacoes()
