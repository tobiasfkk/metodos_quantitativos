import random
import sys
import os

# Certifica de que foram fornecidos exatamente 10 argumentos
if len(sys.argv) != 13:
    print("Parametros de entrada fornecidos incorretamente!")
    print("Uso: python geradorInstancia.py <comprimento da área> <largura da área> <custo das antenas> <alcance das antenas> <instâncias pequenas> <pontos demanda instâncias pequenas> <locais candidatos instâncias pequenas> <instâncias grandes> <pontos demanda instâncias grandes> <locais candidatos instâncias grandes> <máximo de iterações grasp> <valor K da função objetivo>")
    sys.exit(1)

# Recebe valores de entrada
comprimento = int(sys.argv[1]) #33000
largura = int(sys.argv[2]) #30000
custo = int(sys.argv[3]) #7000
alcance = int(sys.argv[4]) #10000
qtdIntanciasPequenas = int(sys.argv[5]) #15
pontosDemandaIntanciasPequenas = int(sys.argv[6]) #10
locaisCandidatosIntanciasPequenas = int(sys.argv[7]) #10
qtdIntanciasGrandes = int(sys.argv[8]) #15
pontosDemandaIntanciasGrandes = int(sys.argv[9]) #700
locaisCandidatosIntanciasGrandes = int(sys.argv[10]) #700
maxIteracoes = int(sys.argv[11]) #1000
K = int(sys.argv[12]) #1000

# Verifica se os valores de entrada são positivos
if comprimento <= 0 or largura <= 0 or custo <= 0 or alcance <= 0 or qtdIntanciasPequenas <= 0 or pontosDemandaIntanciasPequenas <= 0 or locaisCandidatosIntanciasPequenas <= 0 or qtdIntanciasGrandes <= 0 or pontosDemandaIntanciasGrandes <= 0 or locaisCandidatosIntanciasGrandes <= 0:
    print("Os valores de entrada devem ser todos positivos!")
    print("Uso: python geradorInstancia.py <comprimento da área> <largura da área> <custo das antenas> <alcance das antenas> <instâncias pequenas> <pontos demanda instâncias pequenas> <locais candidatos instâncias pequenas> <instâncias grandes> <pontos demanda instâncias grandes> <locais candidatos instâncias grandes> <máximo de iterações grasp> <valor K da função objetivo>")
    sys.exit(1)

def geraInstancia(file_name, pontosDemanda, locaisCandidatos):
    with open(file_name, 'w') as file:

        # Gerando locais candidatos
        file.write(f"A {locaisCandidatos} ")

        # Gerando quantidade de pontos de demanda
        file.write(f"B {pontosDemanda} ")

        # Gerando custo C
        C = custo
        file.write(f"C {C} ")

        # Gerando alcance D
        D = alcance
        file.write(f"D {D} ")

        file.write(f"mi {maxIteracoes} ")

        file.write(f"K {K}\n")

        # Gerando coordenadas dos pontos de demanda
        for i in range(1, pontosDemanda + 1):
            x = random.randint(0, comprimento)
            y = random.randint(0, largura)
            file.write(f"n {x} {y}\n")

        # Gerando coordenadas dos locais candidatos
        for j in range(1, locaisCandidatos + 1):
            x = random.randint(0, comprimento)
            y = random.randint(0, largura)
            file.write(f"m {x} {y}\n")

# Função para excluir arquivos .txt no diretório
def limpar_diretorio(diretorio):
    for arquivo in os.listdir(diretorio):
        if arquivo.endswith(".txt"):
            os.remove(os.path.join(diretorio, arquivo))

# Limpa o diretório de instâncias antes de gerar novos arquivos
diretorio_instancias = "./instancias"
limpar_diretorio(diretorio_instancias)

# Gerando as instâncias pequenas:
for i in range(qtdIntanciasPequenas):
    geraInstancia(f'./instancias/instanciaPequena{i+1}.txt', pontosDemandaIntanciasPequenas, locaisCandidatosIntanciasPequenas)

# Gerando as instâncias maiores:
for i in range(qtdIntanciasGrandes):
    geraInstancia(f'./instancias/instanciaGrande{i+1}.txt', pontosDemandaIntanciasGrandes, locaisCandidatosIntanciasGrandes)

print("Intancias criadas no caminho: .../métodos_quantitativos/instancias")