import sys
from glob import glob
import random

instancia = sys.argv[1]
percentualAleatoriedade = float(sys.argv[2])

def leituraInstancia(instancia):
    global A, B, C, D, mx, my, nx, ny
    nx = []
    ny = []
    mx = []
    my = []
    file = open(instancia, 'r')
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

def calculaDistancia(i, j):
    return ((mx[j] - nx[i]) ** 2 + (my[j] - ny[i]) ** 2) ** 0.5

def calculaScore(j, B0, D):
    score = 0
    for i in B0: # Passa por todos os pontos de demanda ainda nao atendidos
        distancia = calculaDistancia(i, j)
        if distancia <= D:
            score += 1 / distancia
    return score

def construcaoSemiGulosa(percentualAleatoriedade):
    # Antenas nao alocadas
    A0 = list(range(A))

    # Antenas alocadas
    A1 = []

    # Constrói o array vazio que será utilizado no final
    A0Final = [0] * A

    # Pontos de demanda não atendidos
    B0 = list(range(B))

    # Pontos de demanda atendidos
    B1 = []

    # Constrói o array vazio que será utilizado no final
    B0Final = [0] * B

    f = 0
    A0removidos =[]

    while B0: # enquanto existir ponto de demanda nao atendido
        if A0: # se existir antena disponível para alocar
            scores = []

            # Lista q receberá a facilidade que não atende nenhum ponto de demanda, para então remover de A0
            A0remove = []

            for j in A0:
                score = calculaScore(j, B0, D)
                if score > 0:
                    scores.append(score) #desta forma vai selecionar apenas os locais candidatos que atendam pelo menos uma antena
                else:
                    A0remove.append(j) # Armazena os antenas que não atendem nenhum ponto de demanda
                    A0removidos.append(j)  # Armazena os antenas que não atendem nenhum ponto de demanda para adicionar ao conjunto de antenas nao alocadas posteriormente

            for j in A0remove:
                A0.remove(j) # Remove facilidade que não atende nenhum ponto de demanda

            if A0 and scores:
                indicesOrdenados = sorted(range(len(scores)), key=lambda k: scores[k], reverse=True) # Ordena o índice dos scores
                A0ordenado = [A0[j] for j in indicesOrdenados]
                p = max(1, int(percentualAleatoriedade * len(A0ordenado)))  # numero de antenas q serão consideradas após ordenar
                candidatos = A0ordenado[:p]

                j = random.choice(candidatos) # Escolha aleatória de uma facilidade do subconjunto filtrado pelo percentual de aleatoriedade
                A1.append(j) # Adiciona a facilidade escolhida em A1
                A0.remove(j) # Remove a facilidade escolhida de A0
                A0Final[j] = 1

                for i in B0:
                    distancia = calculaDistancia(i, j)
                    if distancia <= D:
                        # Verifica se existe antena já alocada (A1) mais próxima do ponto de demanda em B0
                        antena_mais_proxima = min(A1, key=lambda a: calculaDistancia(i, a), default=None)

                        if antena_mais_proxima is not None:
                            distancia_atual = calculaDistancia(i, antena_mais_proxima)
                            if distancia_atual < distancia:
                                print('aeee')
                                # Atualiza a antena que está atendendo o ponto
                                B1 = [(p, nova_antena) if p == i else (p, a) for p, a in B1]

                f += calculaScore(j, B0, D)

                for i in B0:
                    distancia = calculaDistancia(i, j)
                    if distancia <= D:
                        B1.append((i,j))  # Adiciona ponto de demanda ao array de atendidos junto com a antena que foi alocada
                        B0.remove(i)  # Remove ponto de demanda pois foi atendido
                        B0Final[i] = 1


        else:
            break

    # Adiciona novamente a antena que não atendeu nenhum ponto de demanda ao conjunto de antenas não alocadas
    for j in A0removidos:
        A0.append(j)

    return A1, A0, B1, B0, f, A0Final, B0Final

def print_allocation(A1, B1):
    print("Resultado da Alocação das Antenas:")
    for j in range(A):
        if j in A1:
            print(f' - Antena {j + 1}: Alocada')
        else:
            print(f' - Antena {j + 1}: Não Alocada')
    print("\nResultado da Cobertura dos Pontos de Demanda:")

    for i in range(B):
        if any(pontoDemanda == i for pontoDemanda, _ in B1):
            print(f' - Ponto de demanda {i + 1}: Atendido')
        else:
            print(f' - Ponto de demanda {i + 1}: Não Atendido')

isEntrou = False # validadação de erro
if instancia == 'T' or instancia == 't':
    for instance in glob('./instancias/*'):
        leituraInstancia(instance)
        print(instance[instance.rindex('/') + 1:] + ': ')
        A1, A0, B1, B0, f, A0Final, B0Final = construcaoSemiGulosa(percentualAleatoriedade) # Chamada da heurística construtiva semi-gulosa
        print(" - Antenas alocadas: ", len(A1))
        print(" - Antenas não alocadas: ", len(A0))
        print(" - Pontos de demanda atendidos: ", len(B1))
        print(" - Pontos de demanda não atendidos: ", len(B0))
        print(" - Score das antenas alocadas:", f)
        print(" - Custo total:", len(A1) * C)
        print(" - Antenas:", A0Final)
        print(" - Pontos de demanda:", B0Final)
        print("")
        print_allocation(A1, B1)
        print("")
        isEntrou = True
else:
    for instance in glob(f'./instancias/{instancia}'):
        leituraInstancia(instance)
        print("Instância " + instance[instance.rindex("/") + 1:] + ": ")
        A1, A0, B1, B0, f, A0Final, B0Final = construcaoSemiGulosa(percentualAleatoriedade)  # Chamada da heurística construtiva semi-gulosa
        print(" - Antenas alocadas:", len(A1))
        print(" - Antenas não alocadas:", len(A0))
        print(" - Pontos de demanda atendidos:", len(B1))
        print(" - Pontos de demanda não atendidos:", len(B0))
        print(" - Score das antenas alocadas:", f)
        print(" - Custo total:", len(A1) * C)
        print(" - Antenas:", A0Final)
        print(" - Pontos de demanda:", B0Final)
        print("")
        print_allocation(A1, B1)
        print("")
        isEntrou = True

if isEntrou == False:
    print('Instância informada não existe!')
    print('Aplicar GRASP em uma instância específica use: python alocacaoAntenaGRASP <nome da instancia>.txt <percentual de aleatoriedade, valor entre 0 e 1>')
    print('Aplicar GRASP em todas as instâncias use: python alocacaoAntenaGRASP <T> <percentual de aleatoriedade, valor entre 0 e 1>')
    sys.exit(1)

    # for i, antena in B1:  # Verificar se a antena atual atende melhor algum ponto de demanda ja atendido por outra antena, adicionando junto no score
    #     distancia = calculaDistancia(i, j)
    #     if distancia <= D:
    #         score += 1 / distancia
    #         B1[(i, antena)] = i, j  # Atualiza o ponto de demanda atendido, agora de forma mais próxima de outra antena
    #         # AQUI PRECISA REMOVER o score da antena referente o ponto q n sera mais atendido por ela

    # def busca_local_simples(A1, f_value, nx, ny, mx, my, D):
    #     while True:
    #         melhorou = False
    #
    #         for j_em_A1 in A1:
    #             for j_em_A0 in set(range(A)) - set(A1):
    #                 A1_temp = A1.copy()
    #                 A1_temp.remove(j_em_A1)
    #                 A1_temp.append(j_em_A0)
    #
    #                 nova_f_value = f_value - calculate_score(j_em_A1, A1_temp, nx, ny, mx, my, D)
    #                 nova_f_value += calculate_score(j_em_A0, A1_temp, nx, ny, mx, my, D)
    #
    #                 if nova_f_value > f_value:
    #                     A1 = A1_temp
    #                     f_value = nova_f_value
    #                     melhorou = True
    #
    #         if not melhorou:
    #             break
    #
    #     return A1, f_value