import sys
from glob import glob
import random

instancia = sys.argv[1]
percentualGulosidade = float(sys.argv[2])

A = None # Quantidade de locais candidatos
B = None # Quantidade de pontos de demanda
C = None # Custo das antenas
D = None # Alcance das antenas
nx = None # Coordenada x de pontos de demanda
ny = None # Coordenada y de pontos de demanda
mx = None # Coordenada x de locais candidatos
my = None # Coordenada y de locais candidatos

def read_instance(instance):
    global A, B, C, D, mx, my, nx, ny
    nx = []
    ny = []
    mx = []
    my = []
    file = open(instance, 'r')
    first = True
    for line in file.readlines():
        if first:
            A = int(line.split(' ')[1])
            B = int(line.split(' ')[3])
            C = int(line.split(' ')[5])
            D = int(line.split(' ')[7])
            first = False
            continue
        if (line.split(' ')[0] == 'n'):
            nx.append(int(line.split(' ')[1]))
            ny.append(int(line.split(' ')[2]))
        elif (line.split(' ')[0] == 'm'):
            mx.append(int(line.split(' ')[1]))
            my.append(int(line.split(' ')[2]))

def distance(i, j):
    return ((mx[i] - nx[j]) ** 2 + (my[i] - ny[j]) ** 2) ** 0.5

# def solve():
#     n = B
#     m = A
#     P = 999999  # penalty
#     K = 100000  # importance factor
#
#     # Criação do modelo
#     model = ConcreteModel()
#
#     # Variáveis de decisão
#     model.a = Var(range(A), domain=Binary, initialize=0)
#     model.b = Var(range(B), domain=Binary, initialize=0)
#
#     # IMPLEMENTAÇÃO DO PROFESSOR PARA O ARTIGO COM O K
#     model.obj = Objective(
#         expr=K * sum(model.b[i] for i in range(n)) -
#              sum(C * model.a[j] for j in range(m)) -
#              sum(min([distance(i, j) for j in range(m) if value(model.a[j]) == 0] + [P]) for i in range(n)),
#         sense=maximize
#     )
#
#     # Restricoes
#     model.cons = ConstraintList()
#
#     # Restrição para garantir que pelo menos uma antena seja alocada para cada ponto de demanda
#     for i in range(n):
#         model.cons.add(
#             expr=sum(model.a[j] for j in range(m) if distance(i, j) <= D) >= model.b[i]
#         )
#
#     # Restrição para garantir que pelo menos uma antena seja alocada
#     model.cons.add(expr=sum(model.a[j] for j in range(m)) >= 1)
#
#     # Solução
#     solver = SolverFactory('glpk')
#     results = solver.solve(model)
#
#     # Verificar se a solução é ótima
#     is_optimal = (results.solver.status == SolverStatus.ok) and (
#                 results.solver.termination_condition == TerminationCondition.optimal)
#
#     if is_optimal:
#         print("Solução Ótima Encontrada!")
#     else:
#         print("O Solver não encontrou uma solução ótima.")
#
#     # Mostrar resultados das antenas e pontos de demanda
#     print("Resultado da Alocação das Antenas:")
#     for j in range(A):
#         print(f'Antena {j + 1}: {model.a[j]()}')
#
#     print("Resultado da Cobertura dos Pontos de Demanda:")
#     for i in range(B):
#         print(f'Ponto de demanda {i + 1}: {model.b[i]()}')
#
#     # Valor da função objetivo
#     print("\nValor da Função Objetivo:")
#     print(model.obj.expr())
#
#     # Número de Pontos não atendidos
#     unattended_demand = sum(1 - model.b[i]() for i in range(B))
#     print(f"Número de Pontos Não Atendidos: {unattended_demand}")
#     return 1

def calculate_score(j, A1, nx, ny, mx, my, D):
    score = 0
    for i in range(len(nx)): #passa por todos os pontos de demanda
        if i not in A1:
            distance_val = distance(i, j)
            if distance_val <= D:
                score += 1 / distance_val  # Ponderação inversamente proporcional à distância
    return score

def busca_local_simples(A1, f_value, nx, ny, mx, my, D):
    while True:
        melhorou = False

        for j_em_A1 in A1:
            for j_em_A0 in set(range(A)) - set(A1):
                A1_temp = A1.copy()
                A1_temp.remove(j_em_A1)
                A1_temp.append(j_em_A0)

                nova_f_value = f_value - calculate_score(j_em_A1, A1_temp, nx, ny, mx, my, D)
                nova_f_value += calculate_score(j_em_A0, A1_temp, nx, ny, mx, my, D)

                if nova_f_value > f_value:
                    A1 = A1_temp
                    f_value = nova_f_value
                    melhorou = True

        if not melhorou:
            break

    return A1, f_value

def construcaoSemiGulosaComBuscaLocal(percentualGulosidade):
    A0 = list(range(A))
    A1 = []
    f = 0

    while A0:
        # p = max(1, int(percentualGulosidade * len(A0)))
        p = int(percentualGulosidade * len(A0)) #valor p é definido de acordo com o percentual de gulosidade - qtd de itens de A0 q serão achados de forma gulosa

        scores = [calculate_score(j, A1, nx, ny, mx, my, D) for j in A0]
        sorted_indices = sorted(range(len(scores)), key=lambda k: scores[k], reverse=True)
        A0_sorted = [A0[i] for i in sorted_indices]
        j = random.choice(A0_sorted[:p])
        A1.append(j)
        A0.remove(j)
        f += calculate_score(j, A1, nx, ny, mx, my, D)

    A1, f = busca_local_simples(A1, f, nx, ny, mx, my, D)

    return A1, f

def print_allocation(A1, nx, ny, mx, my, D):
    print("Resultado da Alocação das Antenas:")
    for j in range(A):
        if j in A1:
            print(f'Antena {j + 1}: Alocada')
        else:
            print(f'Antena {j + 1}: Não Alocada')

    print("\nResultado da Cobertura dos Pontos de Demanda:")
    for i in range(B):
        covered = any(distance(j, i) <= D for j in A1)
        if covered:
            print(f'Ponto de demanda {i + 1}: Atendido')
        else:
            print(f'Ponto de demanda {i + 1}: Não Atendido')


# Laço de Instâncias desejadas:

isEntrou = False

if instancia == 'T' or instancia == 't':
    for instance in glob('./instancias/*'):
        read_instance(instance)
        print(instance[instance.rindex('/') + 1:] + ': ', end='')

        # Chamada da heurística construtiva semi-gulosa
       
        A1, f_value = construcaoSemiGulosaComBuscaLocal(percentualGulosidade)
        # Mostra os resultados
        print("Solução Construída:", A1)
        print("Valor da Função Objetivo:", f_value)
        # Adiciona a impressão da alocação
        print_allocation(A1, nx, ny, mx, my, D)
        print("-------------")
        isEntrou = True
else:
    for instance in glob(f'./instancias/{instancia}'):
        read_instance(instance)
        print(instance[instance.rindex('/') + 1:] + ': ', end='')

        # Chamada da heurística construtiva semi-gulosa
        A1, f_value = construcaoSemiGulosaComBuscaLocal(percentualGulosidade)

        # Mostra os resultados
        print("Solução Construída:", A1)
        print("Valor da Função Objetivo:", f_value)
        # Adiciona a impressão da alocação
        print_allocation(A1, nx, ny, mx, my, D)
        print("-------------")
        isEntrou = True

if isEntrou == False:
    print('Instância informada não existe!')
    print('Aplicar GRASP em uma instância específica use: python alocacaoAntenaGRASP <nome da instancia>.txt <percentual de gulosidade, valor entre 0 e 1>')
    print('Aplicar GRASP em todas as instâncias use: python alocacaoAntenaGRASP <T> <percentual de gulosidade, valor entre 0 e 1>')
    sys.exit(1)