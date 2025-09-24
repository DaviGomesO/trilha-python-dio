from models_with_POO import *
from decorator import log_transaction
from iterator import AccountIterator

def menu():
  menu = """
    ======== MENU ========

        [1] - Depositar
        [2] - Sacar
        [3] - Extrato
        [4] - Cadastrar Cliente
        [5] - Criar Conta
        [6] - Listar Contas
        [0] - Sair
    
    Digite a opção desejada: 
=> """
  opcao = int(input(menu))
  return opcao

@log_transaction
def deposito(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = buscar_cliente(cpf, clientes)
    if not cliente:
      print("Cliente não encontrado.")
      return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
      return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposit(valor)

    cliente.carry_out_transaction(transacao, conta)
    return True

@log_transaction
def saque(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = buscar_cliente(cpf, clientes)
    if not cliente:
      print("Cliente não encontrado.")
      return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
      return

    valor = float(input("Informe o valor do saque: "))
    transacao = Withdrawal(valor)

    cliente.carry_out_transaction(transacao, conta)
    return True

@log_transaction
def mostrar_extrato(clientes):
  cpf = input("Informe o CPF do cliente para ver o extrato: ")
  cliente = buscar_cliente(cpf, clientes)
  if not cliente:
    print("Cliente não encontrado.")
    return

  conta = recuperar_conta_cliente(cliente)
  if not conta:
    return

  type_transaction = input("Informe o tipo de transação para o extrato (D-Depósito, S-Saque ou Enter para todos): ").upper()
  
  report = conta.history.generate_report(type_transaction if type_transaction in ["D", "S"] else None)

  for line in report:
    print(line)
  
  print(f"\nSaldo: R$ {conta.balance:.2f}")
  print("==========================================")
  return True

@log_transaction
def cadastrar_cliente(clientes):
  cpf = input("Informe o CPF (apenas números): ")
  usuario_cadastrado = buscar_cliente(cpf, clientes)
    
  if usuario_cadastrado:
    print("Cliente já cadastrado com esse CPF.")
    return
  
  nome = input("Informe o nome do cliente: ")
  data_nascimento = input("Informe a data de nascimento (DD/MM/AAAA): ")
  endereco = input("Informe o endereço: ")
    
  cliente = NaturalPerson(nome, data_nascimento, cpf, endereco)
  clientes.append(cliente)
  print("Cliente cadastrado com sucesso!")
  return True

@log_transaction
def criar_conta_corrente(clientes, contas, numero_conta):
  cpf = input("Informe o CPF do cliente: ")
  cliente_cadastrado = buscar_cliente(cpf, clientes)
  if cliente_cadastrado:
    nova_conta = CurrentAccount.new_account(client=cliente_cadastrado, number=numero_conta)
    contas.append(nova_conta)
    cliente_cadastrado.add_account(nova_conta)
    print(f"Conta criada com sucesso! Agência: {nova_conta.agency}, Conta: {nova_conta.number:04d}")
    return True
  else:
    print("Cliente não encontrado. Cadastre o cliente primeiro.")
    return

def listar_contas(clientes):
  cpf = input("Informe o CPF do cliente: ")
  cliente = buscar_cliente(cpf, clientes)
  if not cliente:
    print("Cliente não encontrado.")
    return

  contas = cliente.accounts
  if not contas:
    print("Nenhuma conta cadastrada.")
    return

  iterator = AccountIterator(contas)
  for conta in iterator:
    print("=" * 100)
    print(conta)
  print("=" * 100)
  return

def buscar_cliente(cpf, clientes):
  clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
  return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.accounts:
        print("\n@@@ Cliente não possui conta! @@@")
        return

    # FIXME: não permite cliente escolher a conta
    return cliente.accounts[0]

def main():
  # NOVAS FUNÇÕES
  accounts = []
  clientes = []

  while True:

      opcao = menu()

      if opcao == 1:
          deposito(clientes)
      elif opcao == 2:
          saque(clientes)
      elif opcao == 3:
          mostrar_extrato(clientes)
      elif opcao == 4:
          cadastrar_cliente(clientes)
      elif opcao == 5:
          numero_conta = len(accounts) + 1
          criar_conta_corrente(clientes, accounts, numero_conta)
      elif opcao == 6:
          listar_contas(clientes)
      elif opcao == 0:
          print("Obrigado por utilizar nosso sistema. Até logo!")
          break
      else:
          print("Operação inválida, por favor selecione novamente a operação desejada.")

main()