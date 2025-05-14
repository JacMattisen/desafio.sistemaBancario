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