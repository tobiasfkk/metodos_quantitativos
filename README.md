# Gerador de Instâncias

Gerador de instâncias cria dois modelos de instâncias: grandes e pequenas, ambas em formato txt e com parâmetros de entrada configuráveis pelo usuário.

Parâmetros de entrada:

    <comprimento da área> = quilômetro
    <largura da área> = quilômetro
    <custo das antenas> = moeda (real por exemplo)
    <alcance das antenas> = quilômetro
    <instâncias pequenas> = unidade numérica
    <pontos demanda instâncias pequenas> = unidade numérica
    <locais candidatos instâncias pequenas> = unidade numérica
    <instâncias grandes> = unidade numérica
    <pontos demanda instâncias grandes> = unidade numérica
    <locais candidatos instâncias grandes> = unidade numérica

Uso: 

    python geradorInstancia.py <comprimento da área> <largura da área> <custo das antenas> <alcance das antenas> <instâncias pequenas> <pontos demanda instâncias pequenas> <locais candidatos instâncias pequenas> <instâncias grandes> <pontos demanda instâncias grandes> <locais candidatos instâncias grandes>

Exemplo: 

    python geradorInstancia.py 33000 30000 7000 10000 5 10 10 5 700 700

Executando pelo terminal o comando do exemplo acima, serão gerados dois grupos de instâncias, pequenas e grandes.

As intâncias serão criadas no caminho *.../métodos_quantitativos/instancias* e estarão ordenadas pelo nome, exemplo:

    instanciaGrande1.txt
    instanciaGrande2.txt
    instanciaGrande3.txt
    instanciaGrande4.txt
    instanciaGrande5.txt
    instanciaPequena1.txt
    instanciaPequena2.txt
    instanciaPequena3.txt
    instanciaPequena4.txt
    instanciaPequena5.txt

Usando de exemplo o conteúdo de instanciaPequena1.txt:

    A 10 B 10 C 7000 D 10000
    n 26788 8132
    n 22363 20166
    n 30812 3771
    n 14762 29883
    n 21769 4274
    n 15873 7925
    n 5537 12268
    n 21405 11142
    n 29449 6580
    n 2395 28331
    m 6999 16544
    m 14925 1992
    m 8608 12367
    m 13679 26235
    m 24312 11078
    m 9131 3976
    m 11523 120
    m 18744 28332
    m 19392 11397
    m 11924 15064

Definições:
    
    A = Quantidade de locais candidatos
    B = Quantidade de pontos de demanda
    C = Custo das antenas
    D = Alcance das antenas
    n = <Coordenada x do ponto de demanda> <Coordenada y do ponto de demanda>
    m = <Coordenada x do local candidato> <Coordenada y do local candidato>

Os valores m e n são gerados aleatoriamente respeitando os valores de comprimento e largura especificados.

Cada execução do gerador exclui as instâncias existentes da pasta e gera novos arquivos .txt.


# Aplicando GRASP na(s) instância(s)
 
Uso:
    
- Aplicando heurística GRASP em uma instância específica:

      python alocacaoAntenaGRASP <nome da instancia>.txt <percentual de gulosidade> 
- Aplicando heurística GRASP em todas as instâncias:

      python alocacaoAntenaGRASP T <percentual de gulosidade> 

Exemplo:
    
- Aplicando heurística GRASP em uma instância específica:

      python alocacaoAntenaGRASP instanciaPequena1.txt 0.5

- Aplicando heurística GRASP em todas as instâncias:

      python alocacaoAntenaGRASP T 0.5

Lembrando que só é possível aplicar a heurística nas instâncias presentes no caminho:

    .../métodos_quantitativos/instancias

Parâmetros de entrada:

    <nome da instância> = nome do arquivo texto localizado no caminho .../métodos_quantitativos/instancias
    <percentual de gulosidade> = percentual da gulosidade para aplicada na heurística construtiva - valor entre 0 e 1