from datetime import date

# Classe transacao (interface)
class Transacao:
  def registrar(self, conta):
    pass

#Subclasse de Transacao: Deposito
class Deposito(Transacao):
  def __init__(self, valor):
    self.valor = valor 

  def registrar(self, conta):
    conta.depositar(self.valor)
    conta.historico.adicionar_transacao(self)

#subclasse de transacao: Saque
class Saque(Transacao):
  def __init__(self, valor):
    self.valor = valor

  def registrar(self, conta):
    conta.sacar(self.valor)
    conta.historico.adicionar_transacao(self)

#Historico
class Historico:
  def __init__(self):
    self.transacoes = []

  def adicionar_transacao(self, transacao):
    self.transacoes.append(transacao)

#Cliente
class Cliente:
  def  __init__(self, endereco):
    self.endereco = endereco
    self.contas = []
  def adicionar_contas(self, conta):
    self.contas.append(conta)
  def realizar_transacao(self, conta, transacao):
    transacao.registrar(conta)

#Pessoa fisica - subclasse de cliente
class PessoaFisica(Cliente):
  def __init__(self, nome, cpf, data_nascimento, endereco):
    super().__init__(endereco)
    self.nome = nome
    self.cpf = cpf
    self.data_nascimento = data_nascimento

#Conta - classe
class Conta:
  def __init__(self, cliente, numero, agencia="0001"):
    self.saldo = 0.0
    self.numero = numero
    self.agencia = agencia
    self.cliente = cliente
    self.historico = Historico()

  def sacar(self, valor):
    if valor > self.saldo:
      print ("Saldo insuficiente!")
      return False
    else:
      self.saldo -= valor
      print (f"Saque de R${valor:.2f} realizado com sucesso!")
      return True
    
  def depositar (self, valor):
    if valor <= 0:
      print ("Valor de depósito inválido!")
      return False
    else:
      self.saldo += valor
      print (f"Depósito de R${valor:.2f}realizado com sucesso!")

#ContaCorrente subclasse
class ContaCorrente (Conta):
  def __init__(self, cliente, numero, limite=500.0, limite_saque=3):
    super(). __init__(cliente, numero)
    self.limite = limite
    self.limite_saques = limite_saque

#Uso
if __name__ == "__main__":
  client1 = PessoaFisica("Joao", "12345678900", date(1988, 4, 5), "Rua das Flores")
  conta1 = ContaCorrente(client1, numero=1)
  client1.adicionar_contas(conta1)

  deposito = Deposito(1000.0)
  client1.realizar_transacao(conta1, Saque)
  print (f"Saldo final: R${conta1.saldo:.2f}")

from datetime import date
import sys


#Funções do menu:

def menu():
    print("\n=== MENU ===")
    print("1 - Criar cliente")
    print("2 - Criar conta")
    print("3 - Depositar")
    print("4 - Sacar")
    print("5 - Mostrar extrato")
    print("6 - Sair")
    return input("Escolha uma opção: ")

# Dados em memória
clientes = []
contas = []

def encontrar_cliente_por_cpf(cpf):
    for cliente in clientes:
        if isinstance(cliente, PessoaFisica) and cliente.cpf == cpf:
            return cliente
    return None

def encontrar_conta_por_numero(numero):
    for conta in contas:
        if conta.numero == numero:
            return conta
    return None

def criar_cliente():
    nome = input("Nome: ")
    cpf = input("CPF: ")
    data_nascimento = input("Data de nascimento (DD-MM-AAAA): ")
    endereco = input("Endereço: ")

    cliente = PessoaFisica(nome, cpf, date.fromisoformat(data_nascimento), endereco)
    clientes.append(cliente)
    print("Cliente criado com sucesso!")

def criar_conta():
    cpf = input("CPF do cliente: ")
    cliente = encontrar_cliente_por_cpf(cpf)

    if cliente:
        numero = len(contas) + 1  #lógica para número de conta
        conta = ContaCorrente(cliente, numero)
        cliente.adicionar_contas(conta)
        contas.append(conta)
        print(f"Conta criada com sucesso! Número: {numero}")
    else:
        print("Cliente não encontrado!")

def depositar():
    numero = int(input("Número da conta: "))
    conta = encontrar_conta_por_numero(numero)

    if conta:
        valor = float(input("Valor para depositar: "))
        transacao = Deposito(valor)
        conta.cliente.realizar_transacao(conta, transacao)
    else:
        print("Conta não encontrada.")

def sacar():
    numero = int(input("Número da conta: "))
    conta = encontrar_conta_por_numero(numero)

    if conta:
        valor = float(input("Valor para sacar: "))
        transacao = Saque(valor)
        conta.cliente.realizar_transacao(conta, transacao)
    else:
        print("Conta não encontrada.")

def mostrar_extrato():
    numero = int(input("Número da conta: "))
    conta = encontrar_conta_por_numero(numero)

    if conta:
        print("\n=== Extrato ===")
        for transacao in conta.historico.transacoes:
            tipo = transacao.__class__.__name__
            print(f"{tipo}: R${transacao.valor:.2f}")
        print(f"Saldo atual: R${conta.saldo:.2f}")
    else:
        print("Conta não encontrada.")

# Loop do menu principal
if __name__ == "__main__":
    while True:
        opcao = menu()

        if opcao == "1":
            criar_cliente()
        elif opcao == "2":
            criar_conta()
        elif opcao == "3":
            depositar()
        elif opcao == "4":
            sacar()
        elif opcao == "5":
            mostrar_extrato()
        elif opcao == "6":
            print("Encerrando o sistema.")
            sys.exit()
        else:
            print("Opção inválida!")
