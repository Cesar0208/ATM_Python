from os import system
from time import sleep

# Importar usuários
import pandas as pd
banco_de_dados = pd.read_excel('Banco_de_dados.xlsx')

# Definir funções
# Iniciar banco
def iniciar_banco(usuario):
    while True:
        loc_dados = banco_de_dados[banco_de_dados['Usuário'].str.match(usuario, na=False)]
        print('-' * 20, "CESAR'S ATM", '-' * 20)
        tela_inicial()
        escolha = str(input('Qual é a sua escolha? '))

        if escolha == '1':
            saldo = loc_dados['Saldo'].values
            saldo = ','.join(str(item) for item in saldo)
            saldo = int(saldo)
            print(f'O seu saldo é de: R${saldo} reais.')
            limpar_tela()

        elif escolha == '2':
            quantidade = float(input('Quanto você quer depositar? '))

            saldo = loc_dados['Saldo'].values[0] + quantidade
            print(f'Com o acressimo de R${quantidade} o seu saldo ficou R${saldo}')

            banco_de_dados.loc[banco_de_dados['Usuário'] == usuario, 'Saldo'] = saldo
            banco_de_dados.to_excel('Banco_de_dados.xlsx', index=False)

            limpar_tela()

        elif escolha == '3':
            quantidade = float(input('Quanto você quer sacar? '))

            saldo = loc_dados['Saldo'].values[0] - quantidade
            print(f'Com o saque de R${quantidade} o seu saldo ficou R${saldo}')

            banco_de_dados.loc[banco_de_dados['Usuário'] == usuario, 'Saldo'] = saldo
            banco_de_dados.to_excel('Banco_de_dados.xlsx', index=False)

            limpar_tela()

        elif escolha == '4':
            para_qual_conta = str(input('Para qual conta quer transferir? '))
            if para_qual_conta in banco_de_dados['Usuário'].values:
                quantidade_trans = float(input('Qual é a quantidade de transferência? '))
                if quantidade_trans <= 0:
                    print('O valor deverá ser positivo.')
                else:
                    saldo = loc_dados['Saldo'].values[0]
                    if quantidade_trans <= saldo:
                        saldo_transferidor = saldo - quantidade_trans
                        banco_de_dados.loc[banco_de_dados['Usuário'] == usuario, 'Saldo'] = saldo_transferidor

                        loc_dados_receptor = banco_de_dados[banco_de_dados['Usuário'].str.match(para_qual_conta, na=False)]
                        saldo_receptor = loc_dados_receptor['Saldo'].values[0]
                        saldo_receptor = saldo_receptor + quantidade_trans
                        banco_de_dados.loc[banco_de_dados['Usuário'] == para_qual_conta, 'Saldo'] = saldo_receptor

                        banco_de_dados.to_excel('Banco_de_dados.xlsx', index=False)

                        print('Transferência realizada.')
                        limpar_tela()
                    else:
                        print('Não foi possível realizar pois a transferencia foi maior que o saldo.')
                        limpar_tela()
            else:
                print('Não foi possível encontrar essa conta.')
                limpar_tela()

        elif escolha == '5':
            print('Obrigado por acessar o nosso banco.')
            limpar_tela()
            break
        else:
            print('Escolha uma opção valida.')
            limpar_tela()

def limpar_tela():
    sleep(1.5)
    system('cls')

def tela_inicial():
    print('''Bem vindo(a):
[1] - Ver saldo
[2] - Depositar
[3] - Sacar
[4] - Transferir entre contas
[5] - Sair''')

def criar_conta():
    while True:
        usuario_criar = input('Digite seu usuário: ')
        senha_criar = input('Digite sua senha com pelo menos 1 letra: ')
        rep_senha = input('Repita sua senha: ')
        if senha_criar == rep_senha:
            print('Conta criada. Por favor, acesse.')
            dados_usuarios = {'Usuário': usuario_criar, 'Senha': senha_criar, 'Saldo': 0}
            novos_dados = pd.DataFrame(dados_usuarios, index=[0])
            novos_dados = novos_dados[banco_de_dados.columns]
            banco_completo = pd.concat([banco_de_dados, novos_dados],ignore_index=True)
            banco_completo.to_excel('Banco_de_dados.xlsx', index=False)
            limpar_tela()
            break
        else:
            print('Refaça seu cadastro.')

def dados_conta():
    while True:
        print('-' * 10, 'Bem vindo', '-' * 10)
        sim_nao_conta = str(input('Você possui uma conta (S/N)? ').lower())
        if sim_nao_conta == 's' or sim_nao_conta == 'sim':
            system('cls')
            break
        else:
            print('-' * 10,'Crie sua conta', '-' * 10)
            criar_conta()
            limpar_tela()
            break
    
    while True:
        banco_de_dados = pd.read_excel('Banco_de_dados.xlsx')
        print('-' * 10,'Digite os seus dados para acessar sua conta', '-' * 10)
        usuario = input('Digite seu usuário: ')
        senha = input('Digite sua senha: ')
        if usuario in banco_de_dados['Usuário'].values:
            loc_dados = banco_de_dados[banco_de_dados['Usuário'].str.match(usuario, na=False)]
            senha_banco = loc_dados['Senha'].values
            if senha_banco == senha:
                print('Acesso Liberado')
                limpar_tela()
                iniciar_banco(usuario)
                return usuario
            else:
                print('Senha errada.')
                limpar_tela()
        else:
            print('Registro não encontrado')
            limpar_tela()
    




dados_conta()
