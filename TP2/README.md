# Trabalho Prático 2: Algoritmos II

Esse trabalho apresenta três algoritmos diferentes para o Problema do Caixeiro Viajante, uma solução exata, baseada no algoritmo Branch-and-Bound, e duas soluções aproximadas, o algoritmo Twice-Around-the-Tree e o algoritmo de Christofides. O objetivo foi implementar os 3 algoritmos, e então fazer um relatório analisando suas soluções, em relação a suas diferenças entre desempenho, avaliando métricas de tempo, espaço e qualidade da solução.

# Requisitos

Para executar o programa, é necessária a biblioteca `networkx` instalada. Para instalar a dependência, execute o comando:

```bash
pip install networkx
```
# Como executar o programa no terminal

## Passo a Passo

1. O arquivo principal do programa é `main.py`, localizado na pasta `src`.

3. Use os argumentos abaixo para executar o programa:

### Argumentos opcionais para escolha de algoritmos

- **Opções:**
  - `-c`: Executar algoritmo Christofides
  - `-t`: Executar algoritmo Twice-Around-the-Tree"
  - `-b`: Executar algoritmo Branch-and-Bound
  - `-all`: Executar todos os algoritmos (default)

Caso não sejam passadas nenhuma opção de algoritmo, então todos os algoritmos serão executados, equivalente a opção "-all". Pode ser escolhido 1 ou 2 opções de algoritmos, ou seja, é possível rodar um individualmente ou fazer qualquer combinação entre dois parâmetros entre '-c', '-t', '-b', não importando ordem.

### Argumento opcional para tempo

- **Opção:**
  - `-timeout=<tempo>`: Define o tempo máximo de execução em segundos para cada algoritmo

Caso não seja passado um valor, cada algoritmo escolhido tem o tempo máximo de execução de 30min, passado esse tempo ele é abortado e os dados referentes à execução são colocados como NA (não-disponível). 

### Argumento opcional para profiling

- **Opção:**
  - `-verbose`: Ativa a saída detalhada, profiling do código para identificar os gargalos.

Caso não seja passado um valor, o programa irá exibir apenas o output padrão esperado.

### Formato Geral do Comando

```bash
python3 ./src/main.py ./data/teste < opções de algoritmos > [tempo] [verbose] 
```

4. Após a execução, os resultados serão exibidos no terminal.

##  Exemplos

* Executa o algoritmo de Christofides (timeout default = 30min):
 
 ```bash
python3 ./src/main.py ./data/a280.tsp -c
```

* Executa o algoritmo de Twice-Around-the-Tree (timeout default = 30min):

 ```bash
python3 ./src/main.py ./data/a280.tsp -t
```

* Executa os algoritmos de Twice-Around-the-Tree e Christofides (timeout default = 30min para cada):

 ```bash
python3 ./src/main.py ./data/a280.tsp -t -c
```

* Executa os algoritmos de Twice-Around-the-Tree, Christofides e Branch-and-Bound (timeout default = 30min para cada):

 ```bash
python3 ./src/main.py ./data/a280.tsp -all
```

* Executa os algoritmos de Twice-Around-the-Tree, Christofides e Branch-and-Bound (timeout default = 30min para cada):

 ```bash
python3 ./src/main.py ./data/a280.tsp
```

* Executa o algoritmo de Branch-and-Bound com timeout igual a 10 segundos:

 ```bash
python3 ./src/main.py ./data/a280.tsp -b -timeout=10
```

* Executa os algoritmos de Twice-Around-the-Tree e Branch-and-Bound com timeout igual a 10 segundos:

 ```bash
python3 ./src/main.py ./data/a280.tsp -t -b -timeout=10
```

* Executa os algoritmos de Twice-Around-the-Tree, Christofides e Branch-and-Bound com timeout igual a 5 segundos:

 ```bash
python3 ./src/main.py ./data/a280.tsp -timeout=5
```

* Executa o algoritmos Twice-Around-the-Tree com timeout igual a 1 segundo, ativando a saída detalhada:

 ```bash
python3 ./src/main.py ./data/a280.tsp -t -timeout=1 -verbose
```

# Como executar os experimentos

## Passo a Passo

1. O arquivo para realizar todos os testes para cada algoritmo é `experiment.py`, localizado na pasta `src`.

3. Não é necessário o uso de argumentos para executar o programa, mas pode ser passado o seguinte argumento opcional:

### Argumentos opcionais para tempo

- **Opção:**
  - `-timeout=<tempo>`: Define o tempo máximo de execução em segundos para cada algoritmo

Caso não seja passado um valor, cada algoritmo será rodado com o tempo máximo de execução de 30min, passado esse tempo ele é abortado e os dados referentes à execução são colocados como NA (não-disponível). 


### Formato Geral do Comando

```bash
python3 ./src/experiment.py [tempo]
```

4. Após a execução, os resultados serão exibidos no terminal e salvos no arquivo `results.csv`.

##  Exemplos

* Executa todas os testes da pasta `data` para cada algoritmo (timeout default = 30min):
 
 ```bash
python3 ./src/experiment.py
```

* Executa todas os testes da pasta `data` para cada algoritmo com timeout igual a 5 segundos:

 ```bash
python3 ./src/experiment.py -timeout=5
```

## Colaboradores

<table>
  <tr>
    <td align="center">
      <a href="#">
        <sub>
          <b><a href="https://github.com/LrcSantos">Lucas Rafael Costa Santos</a></b>
        </sub>
      </a>
    </td>
     <td align="center">
      <a href="#">
        <sub>
          <b><a href="https://github.com/luccaamp">Lucca Alvarenga de Magalhães Pinto</a></b>
        </sub>
      </a>
    </td>
  </tr>
</table>
