def menu():
  menu = """
    ======== MENU ========

        [1] - Depositar
        [2] - Sacar
        [3] - Extrato
        [4] - Cadastrar Usuário
        [5] - Criar Conta
        [6] - Listar Contas
        [0] - Sair
    
    Digite a opção desejada: 
=> """
  opcao = int(input(menu))
  return opcao

def deposito(saldo, valor, extrato):
  if valor > 0:
    saldo += valor
    extrato.append(("Depósito", valor))
    print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
  else:
    print("Operação falhou! O valor informado é inválido.")

  return saldo, extrato

def saque(*, saldo, valor, extrato, limite, numero_saques, limites_saques):
  excedeu_saldo = valor > saldo
  excedeu_limite = valor > limite
  excedeu_saques = numero_saques >= limites_saques

  if excedeu_saldo:
    print("Operação falhou! Você não tem saldo suficiente.")
  elif excedeu_limite:
    print("Operação falhou! O valor do saque excede o limite.")
  elif excedeu_saques:
    print("Operação falhou! Número máximo de saques excedido.")
  elif valor > 0:
    saldo -= valor
    extrato.append(("Saque", valor))
    print(f"Saque de R$ {valor:.2f} realizado com sucesso!")
    numero_saques += 1
  else:
    print("Operação falhou! O valor informado é inválido.")

  return saldo, extrato, numero_saques

def mostrar_extrato(saldo, *, extrato):
  print("\n================ EXTRATO ================")
  if extrato:
    for op in extrato:
      print(f'{op[0]}: R$ {op[1]:.2f}')
  else:
    print("Não foram realizadas movimentações.")
  print(f"\nSaldo: R$ {saldo:.2f}")
  print("==========================================")

def cadastrar_usuario(usuarios):
  cpf = input("Informe o CPF (apenas números): ")
  usuario_cadastrado = buscar_usuario(cpf, usuarios)
    
  if usuario_cadastrado:
    print("Usuário já cadastrado com esse CPF.")
    return
  
  nome = input("Informe o nome do usuário: ")
  data_nascimento = input("Informe a data de nascimento (DD/MM/AAAA): ")
  endereco = input("Informe o endereço: ")
    
  novo_usuario = {
    'nome': nome,
    'data_nascimento': data_nascimento,
    'cpf': cpf,
    'endereco': endereco
  }
  usuarios.append(novo_usuario)
  print("Usuário cadastrado com sucesso!")
  return

def criar_conta_corrente(usuarios, contas, agencia, numero_conta):
  cpf = input("Informe o CPF do usuário: ")
  usuario_cadastrado = buscar_usuario(cpf, usuarios)
  if usuario_cadastrado:
    print(f"Conta criada com sucesso! Agência: {agencia}, Conta: {numero_conta}")
    nova_conta = {
      'agencia': agencia,
      'numero_conta': numero_conta,
      'usuario': usuario_cadastrado
    }
    return nova_conta
  
  print("Usuário não encontrado. Cadastre o usuário primeiro.")
  return

def buscar_usuario(cpf, usuarios):
  usuarios_filtrados = [usuario for usuario in usuarios if usuario['cpf'] == cpf]
  return usuarios_filtrados[0] if usuarios_filtrados else None

def listar_contas(contas):
  if not contas:
    print("Nenhuma conta cadastrada.")
    return
  
  for conta in contas:
    print(f"Agência: {conta['agencia']}, Conta: {conta['numero_conta']}, Titular: {conta['usuario']['nome']}")
  print("================"*3)
  return

def main():
  saldo = 0
  extrato = []
  numero_saques = 0
  limite = 500
  LIMITE_SAQUES = 3
  AGENCIA = "0001"

  # NOVAS FUNÇÕES
  contas = []
  usuarios = []

  while True:

      opcao = menu()

      if opcao == 1:
        valor = float(input("Informe o valor do depósito: "))
        saldo, extrato = deposito(saldo, valor, extrato)
      elif opcao == 2:
        valor = float(input("Informe o valor do saque: "))
        saldo, extrato, numero_saques = saque(saldo=saldo, valor=valor, extrato=extrato, limite=limite, numero_saques=numero_saques, limites_saques=LIMITE_SAQUES)
      elif opcao == 3:
        mostrar_extrato(saldo, extrato=extrato)
      elif opcao == 4:
        cadastrar_usuario(usuarios)
      elif opcao == 5:
        agencia = AGENCIA
        numero_conta = len(contas) + 1
        conta = criar_conta_corrente(usuarios, contas, agencia, numero_conta)
        if conta:
          contas.append(conta)
          print("Conta criada com sucesso!")
      elif opcao == 6:
        listar_contas(contas)
      elif opcao == 0:
        print("Obrigado por utilizar nosso sistema. Até logo!")
        break
      else:
          print("Operação inválida, por favor selecione novamente a operação desejada.")

main()