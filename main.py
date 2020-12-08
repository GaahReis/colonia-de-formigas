import math

from aco import ACO, Grafico
from plot import plot

# Gabriel Henrique Reis
# Marcel Losso

def distancia(cidade1: dict, cidade2: dict):
    return math.sqrt((cidade1['x'] - cidade2['x']) ** 2 + (cidade1['y'] - cidade2['y']) ** 2)


def main():
    cidades = []
    pontos = []
    with open('./exemplo.txt') as f:
        for line in f.readlines():
            city = line.split(' ')
            cidades.append(dict(index=int(city[0]), x=int(city[1]), y=int(city[2])))
            pontos.append((int(city[1]), int(city[2])))
    matriz_custo = []
    rank = len(cidades)
    for i in range(rank):
        row = []
        for j in range(rank):
            row.append(distancia(cidades[i], cidades[j]))
        matriz_custo.append(row)
    aco = ACO(10, 100, 1.0, 10.0, 0.5, 10, 2)
    grafico = Grafico(matriz_custo, rank)
    caminho, custo = aco.resolve(grafico)
    print('custo: {}, caminho: {}'.format(custo, caminho))
    plot(pontos, caminho)

if __name__ == '__main__':
    main()
