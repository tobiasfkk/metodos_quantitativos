import sys
from glob import glob

instancia = sys.argv[1]

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


# Laço de Instâncias desejadas:
if instancia == '':
    for instance in glob('./instancias'):
        read_instance(instance)
        print(instance[instance.rindex('/') + 1:] + ': ', end='')
else:
    for instance in glob(f'./instancias/{instancia}.txt'):
        read_instance(instance)
        print(instance[instance.rindex('/') + 1:] + ': ', end='')
    # solve()