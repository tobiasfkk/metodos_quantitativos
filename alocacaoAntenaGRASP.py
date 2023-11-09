import sys
from glob import glob
import random

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
#     return 1

def construcaoSemiGulosa(alpha):

    A0 = list(range(A))
    A1 = []
    f = 0

    while A0:
        # Determina o tamanho do conjunto de candidatos restritos
        p = max(1, int(alpha * len(A0)))

        # Calcula pontuações para todas as facilidades em A0
        scores = [calculate_score(j, A1, nx, ny, mx, my, D) for j in A0]

        # Ordena A0 com base nas pontuações em ordem decrescente
        sorted_indices = sorted(range(len(scores)), key=lambda k: scores[k], reverse=True)
        A0_sorted = [A0[i] for i in sorted_indices]

        # Seleciona aleatoriamente uma facilidade do conjunto de candidatos restritos
        j = random.choice(A0_sorted[:p])

        # Adiciona j em A1 e remove de A0
        A1.append(j)
        A0.remove(j)

        # Atualiza a função objetivo
        f += calculate_score(j, A1, nx, ny, mx, my, D)

    return A1, f

def calculate_score(j, A1, nx, ny, mx, my, D):
    # Pondera a pontuação ao adicionar a facilidade j em A1
    score = 0
    for i in range(len(nx)):
        if i not in A1:
            distance_val = distance(i, j)
            if distance_val <= D:
                score += 1 / distance_val  # Ponderação inversamente proporcional à distância
    return score

# Laço de Instâncias desejadas:

isEntrou = False

# if instancia == 'T' or instancia == 't': # Testa todas as instâncias
#     for instance in glob('./instancias/*'):
#         read_instance(instance)
#         print(instance[instance.rindex('/') + 1:] + ': ', end='')
#         isEntrou = True
#         # solve()
# else:
#     for instance in glob(f'./instancias/{instancia}'): # Testa apenas instância informada
#         read_instance(instance)
#         print(instance[instance.rindex('/') + 1:] + ': ', end='')
#         isEntrou = True
#         # solve()


if instancia == 'T' or instancia == 't':
    for instance in glob('./instancias/*'):
        read_instance(instance)
        print(instance[instance.rindex('/') + 1:] + ': ', end='')

        # Chamada da heurística construtiva semi-gulosa
        alpha = 0.5  # Ajuste o valor de alpha conforme necessário
        A1, f_value = construcaoSemiGulosa(alpha)

        # Mostra os resultados
        print("Solução Construída:", A1)
        print("Valor da Função Objetivo:", f_value)
        print("-------------")
        isEntrou = True
else:
    for instance in glob(f'./instancias/{instancia}'):
        read_instance(instance)
        print(instance[instance.rindex('/') + 1:] + ': ', end='')

        # Chamada da heurística construtiva semi-gulosa
        alpha = 0.5  # Ajuste o valor de alpha conforme necessário
        A1, f_value = construcaoSemiGulosa(alpha)

        # Mostra os resultados
        print("Solução Construída:", A1)
        print("Valor da Função Objetivo:", f_value)
        print("-------------")
        isEntrou = True

if isEntrou == False:
    print('Instância informada não existe!')
    print('Aplicar GRASP em uma instância específica use: python alocacaoAntenaGRASP <nome da instancia>.txt')
    print('Aplicar GRASP em todas as instâncias use: python alocacaoAntenaGRASP T')
    sys.exit(1)