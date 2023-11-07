import random
def geraInstancia(file_name, pontosDemanda, locaisCandidatos):
    with open(file_name, 'w') as file:

        # Gerando locais candidatos
        file.write(f"A {locaisCandidatos} ")

        # Gerando quantidade de pontos de demanda
        file.write(f"B {pontosDemanda} ")

        # Gerando custo C
        C = 7000
        file.write(f"C {C} ")

        # Gerando alcance D
        D = 10000
        file.write(f"D {D}\n")

        # Gerando coordenadas dos pontos de demanda
        for i in range(1, pontosDemanda + 1):
            x = random.randint(0, 33000)
            y = random.randint(0, 30000)
            file.write(f"n {x} {y}\n")

        # Gerando coordenadas dos locais candidatos
        for j in range(1, locaisCandidatos + 1):
            x = random.randint(0, 33000)
            y = random.randint(0, 30000)
            file.write(f"m {x} {y}\n")

#Gerando as instâncias pequenas:
pontosDemanda = 10
locaisCandidatos = 10
for i in range(15):
    geraInstancia(f'./instancias/instanciaPequena{i+1}.txt', pontosDemanda, locaisCandidatos)

#Gerando as instâncias maiores:
pontosDemanda = 700
locaisCandidatos =700
for i in range(15):
    geraInstancia(f'./instancias/instanciaGrande{i+1}.txt', pontosDemanda, locaisCandidatos)