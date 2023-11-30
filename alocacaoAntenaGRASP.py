import sys
from glob import glob
import random
import time

instancia = sys.argv[1]
percentualAleatoriedade = float(sys.argv[2])

def leituraInstancia(instancia):
    global A, B, C, D, maxIteracoes, K, mx, my, nx, ny
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
            maxIteracoes = int(line.split(' ')[9])
            K = int(line.split(' ')[11])
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
            if distancia != 0:
                score += 1 / distancia
    return score

def retornaDistanciaMinima(pontosDemanda,A1): #Soma a distancia de todos os pontos de demanda(alocados ou nao) á antena alocada mais próxima)
    somatorioMinimaDistancia = 0
    for i in pontosDemanda: #B - todos os pontos de demanda, atendidos ou nao
        distancia = 0
        minimaDistancia = 0
        for j in A1: # ntenas alocadas
            j = j[0] # antena está no primeiro termo
            if minimaDistancia == 0: # apenas primeira vez
                minimaDistancia = calculaDistancia(i, j)
            else:
                distancia = calculaDistancia(i, j)
            if distancia < minimaDistancia and distancia != 0:
                minimaDistancia = distancia
        somatorioMinimaDistancia += minimaDistancia
    return somatorioMinimaDistancia

def grasp(percentualAleatoriedade):

    i = 0
    while (i < maxIteracoes):
        A1, A0, B1, B0, A0Final, B0Final, f = construcaoSemiGulosa(percentualAleatoriedade, K)
        melhorA1, melhorA0, melhorB1, melhorB0, melhorA0Final, melhorB0Final, melhorf = buscaLocalSimples(A1, A0, B1, B0, A0Final, B0Final, K, f)

        if i == 0: # Primeira vez vai ser a melhor solucao após a busca local
            graspA1 = melhorA1
            graspA0 = melhorA0
            graspB1 = melhorB1
            graspB0 = melhorB0
            graspA0Final = melhorA0Final
            graspB0Final = melhorB0Final
            graspf = melhorf
        elif melhorf > graspf:
            graspA1 = melhorA1
            graspA0 = melhorA0
            graspB1 = melhorB1
            graspB0 = melhorB0
            graspA0Final = melhorA0Final
            graspB0Final = melhorB0Final
            graspf = melhorf

        i += 1

    return graspA1, graspA0, graspB1, graspB0, graspA0Final, graspB0Final, graspf

def construcaoSemiGulosa(percentualAleatoriedade, K):


    A0 = list(range(A) )# Antenas nao alocadas
    for j in A0:
        A0[j] = (j,0) # Adiciona o score 0 para todas as antenas

    A1 = [] # Antenas alocadas
    A0Final = [0] * A # Constrói o array vazio que será utilizado no final
    B0 = list(range(B)) # Pontos de demanda não atendidos
    pontosDemanda = list(range(B))
    B1 = [] # Pontos de demanda atendidos
    B0Final = [0] * B # Constrói o array vazio que será utilizado no final
    A0removidos =[]

    while B0: # enquanto existir ponto de demanda nao atendido
         if A0: # se existir antena disponível para alocar

            # Lista q receberá a facilidade que não atende nenhum ponto de demanda, para então remover de A0
            A0remove = []
            B0remove = []

            for indice, j in enumerate(A0):
                j = j[0] # j recebe só o indice da antena
                score = calculaScore(j, B0, D)
                A0[indice] = (j,score) # Armazena a antena e seu score
                if score == 0:
                    A0remove.append((j,score)) # Armazena os antenas que não atendem nenhum ponto de demanda
                    A0removidos.append((j,score))  # Armazena os antenas que não atendem nenhum ponto de demanda para adicionar ao conjunto de antenas nao alocadas posteriormente

            for j in A0remove:
                A0.remove(j) # Remove facilidade que não atende nenhum ponto de demanda

            if A0:
                A0ordenado = sorted(A0, key=lambda tupla: tupla[1], reverse=True) # Ordena pelo score
                p = max(1, int(percentualAleatoriedade * len(A0ordenado)))  # numero de antenas q serão consideradas após ordenar
                candidatos = A0ordenado[:p]
                j = random.choice(candidatos) # Escolha aleatória de uma facilidade do subconjunto filtrado pelo percentual de aleatoriedade
                A1.append(j) # Adiciona a facilidade escolhida em A1
                A0.remove(j) # Remove a facilidade escolhida de A0
                j = j[0]  # j recebe apenas o indice da antena
                A0Final[j] = 1 # Identifica a antena como alocada

                for i in B0: # Para cada ponto de demanda ainda não atendido
                    distancia = calculaDistancia(i, j)
                    if distancia <= D:
                        B1.append((i,j))  # Adiciona ponto de demanda ao array de atendidos junto com o índice da antena que foi alocada
                        B0remove.append(i)
                        B0Final[i] = 1

                for i in B0remove:
                    B0.remove(i)  # Remove ponto de demanda pois foi atendido

            else:
                 break
         else:
            break

    for indicejj, jj in enumerate(A1):  # Antenas já alocadas
        scorejj = jj[1]
        jj = jj[0]  # jj recebe só o indice da antena
        for indiceii, i in enumerate(B1):  # Para cada ponto ja atendido, verifica se a nova antena instalada atende melhor
            j = i[1]  # j Antena que está atendendo atualmente
            i = i[0]  # i recebe só o indice do ponto de demanda
            if jj != j:  # Para não verificar a mesma antena duas vezes
                distanciaj = calculaDistancia(i, j) # Distancia da antena que está atendendo atualmente
                distanciajj = calculaDistancia(i, jj) # Distancia da antena do for
                if distanciajj < distanciaj:  # Caso a nova antena atenda melhor o ponto de demanda
                    B1[indiceii] = (i, jj)  # Faz a troca para a antena ja alocada anteriormente q atende melhor o ponto i
                    scorejj += 1 / distanciajj
                    A1[indicejj] = (jj,scorejj) # Atualiza o score da antena que recebeu um novo ponto de demanda

    A1remove = []
    for j in A1: # Se a antena alocada não atende mais nenhum ponto de demanda pois foram todos atendidos de forma melhor por outra antena, esta é removida
        if not any(j[0] == i[1] for i in B1): # Verificando se o número da antena não está presente no segundo termo de todo ponto alocado
            A1remove.append((j))  # Armazena os antenas que não atendem nenhum ponto de demanda
            A0removidos.append((j))  # Armazena os antenas que não atendem nenhum ponto de demanda para adicionar ao conjunto de antenas nao alocadas posteriormente

    for j in A1remove:
        A1.remove(j)  # Remove facilidade que não atende nenhum ponto de demanda

    for j in A0removidos:
        A0.append(j) # Adiciona novamente a antena que não atendeu nenhum ponto de demanda ao conjunto de antenas não alocadas

    somatorioMinimaDistancia = retornaDistanciaMinima(pontosDemanda,A1)
    f = K*len(B1) - C*len(A1) - somatorioMinimaDistancia
    return A1, A0, B1, B0, A0Final, B0Final, f

def buscaLocalSimples(A1, A0, B1, B0, A0Final, B0Final, K, f):

    pontosDemanda = list(range(B))

    melhorA1 = A1.copy()
    melhorA0 = A0.copy()
    melhorB1 = B1.copy()
    melhorB0 = B0.copy()
    melhorA0Final = A0Final.copy()
    melhorB0Final = B0Final.copy()
    melhorf = f

    if len(A1) > 1: # Se tiver apenas uma antena, não faz sentido remover ela

        auxA1 = A1.copy()
        auxA0 = A0.copy()
        auxB1 = B1.copy()
        auxB0 = B0.copy()
        auxA0Final = A0Final.copy()
        auxB0Final = B0Final.copy()
        auxf = f

        A1copy = A1.copy()

        for j in A1copy:
            auxA0.append(j)  # Adiciona a antena removida ao array de não alocadas
            auxA1.remove(j)  # Remove a antena do array das antenas alocadas
            j = j[0] # índice da antena é apenas o primeiro termo
            auxA0Final[j] = 0  # Identifica a antena como não alocada no array final

            B1remove = []
            for i in auxB1: # Para todos os pontos de demanda atendidos
                if i[1] == j: # Se o segundo termo do ponto alocado é a antena
                    B1remove.append(i) # Adiciona o ponto de demanda para remoção

            for i in B1remove:
                auxB1.remove(i)  # Remove ponto de demanda pois foi desatendido
                auxB0.append(i)  # Coloca o ponto de demanda no array de não atendidos
                i = i[0]  # Pega apenas o indice da antena que está no primeiro termo - exemplo: [(pontodemanda, antena),(pontodemanda, antena),(pontodemanda, antena)]
                auxB0Final[i] = 0  # Identifica o ponto de demanda como não atendido no array final

            somatorioMinimaDistancia = retornaDistanciaMinima(pontosDemanda, auxA1)
            auxf = K * len(auxB1) - C * len(auxA1) - somatorioMinimaDistancia

            if auxf > melhorf: # Se a funcao encontrada for melhor que a melhor funcao
                melhorA1 = auxA1.copy()
                melhorA0 = auxA0.copy()
                melhorB1 = auxB1.copy()
                melhorB0 = auxB0.copy()
                melhorA0Final = auxA0Final.copy()
                melhorB0Final = auxB0Final.copy()
                melhorf = auxf

            auxA1 = A1.copy()
            auxA0 = A0.copy()
            auxB1 = B1.copy()
            auxB0 = B0.copy()
            auxA0Final = A0Final.copy()
            auxB0Final = B0Final.copy()
            auxf = f

    return melhorA1, melhorA0, melhorB1, melhorB0, melhorA0Final, melhorB0Final, melhorf

def print_allocation(A1, B1):
    print("Resultado da Alocação das Antenas:")
    for j in range(A):
        if any(j == item[0] for item in A1):
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
        A1, A0, B1, B0, A0Final, B0Final, f = grasp(percentualAleatoriedade) # Chamada do GRASP
        print(" - Antenas alocadas: ", len(A1))
        print(" - Antenas não alocadas: ", len(A0))
        print(" - Pontos de demanda atendidos: ", len(B1))
        print(" - Pontos de demanda não atendidos: ", len(B0))
        print(" - Valor da função objeivo: ", f)
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
        A1, A0, B1, B0, A0Final, B0Final, f = grasp(percentualAleatoriedade)  # Chamada do GRASP
        print(" - Antenas alocadas:", len(A1))
        print(" - Antenas não alocadas:", len(A0))
        print(" - Pontos de demanda atendidos:", len(B1))
        print(" - Pontos de demanda não atendidos:", len(B0))
        print(" - Valor da função objeivo: ", f)
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