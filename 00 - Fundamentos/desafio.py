menu = """
    ======== MENU ========

        [1] - Depositar
        [2] - Sacar
        [3] - Extrato
        [0] - Sair
    
    Digite a opção desejada: 
=> """

saldo = 0
limite = 500
extrato = []
numero_saques = 0
LIMITE_SAQUES = 3

while True:

    opcao = input(menu)

    if opcao == "1":
        valor = float(input("Informe o valor do depósito: "))

        if valor > 0:
            saldo += valor
            extrato.append(("Depósito", valor))
            print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")

        else:
            print("Operação falhou! O valor informado é inválido.")

    elif opcao == "2":
        valor = float(input("Informe o valor do saque: "))

        excedeu_saldo = valor > saldo

        excedeu_limite = valor > limite

        excedeu_saques = numero_saques >= LIMITE_SAQUES

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

    elif opcao == "3":
        print("\n================ EXTRATO ================")
        if extrato:
            for op in extrato:
                print(f'{op[0]}: R${op[1]:.2f}\n')
        else:
            print("Não foram realizadas movimentações.")
        print(f"\nSaldo: R$ {saldo:.2f}\n")
        print("==========================================")

    elif opcao == "0":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
