##
# Faculdade de Tecnologia de Americana
# Análise e Desenvolvimento de Sistemas
# Professor: Andre Lima
# Grupo: Lucas Alves da Silva
#        Caio Matheus Teles
# Requisitos:  PuLP => Bibliteca para modelagem de problemas de PL.
#              Sys  => Biblioteca que fornece funções e variáveis ​​usadas
#                      para manipular diferentes partes do ambiente de tempo
#                      de execução.
#             NumPy => Biblioteca usada para trabalhar com listas

import sys
from pulp import *
import numpy as np
import os

if __name__ == '__main__':
    nome_arquivo = sys.argv[0]
    print('=' * 80)
    print(f'\n                          SIMPLEX - Arquivo: {nome_arquivo}\n')
    print('=' * 80)

try:
    while True:
        value_res = []
        value_obj = []
        var = []
        op_res = []
        obj = input('Qual é o objetivo da função: ').title()
        qtd_var = int(input('Quantidade de variaveis: '))
        qtd_res = int(input('Quantidade de restrições: '))

        print('=' * 80)

        if (obj == 'Maximizar'):
            prob = LpProblem("Maximizar_Lucro", LpMaximize)  # Função de Maximizar
        elif (obj == 'Minimizar'):
            prob = LpProblem("Minimizar_Lucro", LpMinimize)  # Função de Minimizar

        print('Função objetiva')
        for z in range(qtd_var):
            var.append(LpVariable(f'x{z + 1}', 0, None))  # Variavel deve ser maior ou igual `a zero
            value_obj.append(int(input(f'[x{z + 1}]: ')))

        print('=' * 80)
        c = 0
        for z in range(len(var)):
            c = c + np.multiply(value_obj, var)[z]

        # Função Objetiva
        prob += c

        # Restricoes
        print('Restrições')
        for z in range(qtd_res):
            m = []
            for x in range(qtd_var):
                m.append(int(input(f'R{z + 1} - [x{x + 1}]: ')))
            value_res.append(m)
            op_res.append(input('Insira - Ex: <= | = | >= valor: ').split(' '))
            print('-')

        print('=' * 80)
        s = np.multiply(value_res, var)
        result = np.concatenate(s)
        h = len(result) / qtd_res

        x = []
        k = []
        n = []

        k.append(result[0:int(h)])
        x.append(result[int(h):len(result)])

        n.append(k)
        n.append(x)

        for z in range(len(n)):
            if (op_res[z][0] == '='):
                prob += sum(n[z][0]) == int(op_res[z][1])
            elif (op_res[z][0] == '>='):
                prob += sum(n[z][0]) >= int(op_res[z][1])
            elif (op_res[z][0] == '<='):
                prob += sum(n[z][0]) <= int(op_res[z][1])

        for z in range(qtd_var):
            prob += var[z] >= 0

        # Resolucao do problema
        prob.solve()

        # Escreve o modelo no arquivo
        prob.writeLP(nome_arquivo + ".lp")

        # Imprime o estado da resolucao
        print(LpStatus[prob.status])

        # Imprime os valores das variaveis
        for variable in prob.variables():
            print(f'{variable.name} = {(variable.varValue):.02f}')

        # Imprime o valor objetivo
        print(f'Z = {value(prob.objective):.02f}')
        escolha = str(input('Fazer novo cálculo: [S/N]: '))[0].upper()
        if escolha in 'N':
            break
        else:
            os.system('cls')

except IOError:
    print('ERRO: Nome do arquivo invalido: \"' + nome_arquivo + '\"')
    print('\n================================================================================')

input('...Pressione algo para sair...')
