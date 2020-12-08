import random


class Grafico(object):
    def __init__(self, matriz_custo: list, rank: int):
        self.matrix = matriz_custo
        self.rank = rank
        # noinspection PyUnusedLocal
        self.feromonio = [[1 / (rank * rank) for j in range(rank)] for i in range(rank)]


class ACO(object):
    def __init__(self, count_formiga: int, geracoes: int, alfa: float, beta: float, rho: float, q: int,
                 estrategia: int):

        self.Q = q
        self.rho = rho
        self.beta = beta
        self.alfa = alfa
        self.count_formiga = count_formiga
        self.geracoes = geracoes
        self.update_estrategia = estrategia

    def _update_feromonio(self, grafico: Grafico, formigas: list):
        for i, row in enumerate(grafico.feromonio):
            for j, col in enumerate(row):
                grafico.feromonio[i][j] *= self.rho
                for formiga in formigas:
                    grafico.feromonio[i][j] += formiga.feromonio_delta[i][j]

    # noinspection PyProtectedMember
    def resolve(self, grafico: Grafico):
        melhor_custo = float('inf')
        melhor_solucao = []
        for gen in range(self.geracoes):
            # noinspection PyUnusedLocal
            formigas = [_Formiga(self, grafico) for i in range(self.count_formiga)]
            for formiga in formigas:
                for i in range(grafico.rank - 1):
                    formiga._select_next()
                formiga.custo_total += grafico.matrix[formiga.tabu[-1]][formiga.tabu[0]]
                if formiga.custo_total < melhor_custo:
                    melhor_custo = formiga.custo_total
                    melhor_solucao = [] + formiga.tabu
                formiga._update_feromonio_delta()
            self._update_feromonio(grafico, formigas)

        return melhor_solucao, melhor_custo


class _Formiga(object):
    def __init__(self, aco: ACO, grafico: Grafico):
        self.colonia = aco
        self.grafico = grafico
        self.custo_total = 0.0
        self.tabu = []
        self.feromonio_delta = []
        self.permitido = [i for i in range(grafico.rank)] 
        self.eta = [[0 if i == j else 1 / grafico.matrix[i][j] for j in range(grafico.rank)] for i in
                    range(grafico.rank)] 
        start = random.randint(0, grafico.rank - 1)

        self.tabu.append(start)
        self.atual = start
        self.permitido.remove(start)

    def _select_next(self):
        denominator = 0
        for i in self.permitido:
            denominator += self.grafico.feromonio[self.atual][i] ** self.colonia.alfa * self.eta[self.atual][
                                                                                            i] ** self.colonia.beta
        # noinspection PyUnusedLocal
        possibilidades = [0 for i in range(self.grafico.rank)] 
        for i in range(self.grafico.rank):
            try:
                self.permitido.index(i)  
                possibilidades[i] = self.grafico.feromonio[self.atual][i] ** self.colonia.alfa * \
                    self.eta[self.atual][i] ** self.colonia.beta / denominator
            except ValueError:
                pass 
        
        selecionado = 0
        rand = random.random()
        for i, probability in enumerate(possibilidades):
            rand -= probability
            if rand <= 0:
                selecionado = i
                break
        self.permitido.remove(selecionado)
        self.tabu.append(selecionado)
        self.custo_total += self.grafico.matrix[self.atual][selecionado]
        self.atual = selecionado

    # noinspection PyUnusedLocal
    def _update_feromonio_delta(self):
        self.feromonio_delta = [[0 for j in range(self.grafico.rank)] for i in range(self.grafico.rank)]
        for _ in range(1, len(self.tabu)):
            i = self.tabu[_ - 1]
            j = self.tabu[_]
            if self.colonia.update_estrategia == 1: 
                self.feromonio_delta[i][j] = self.colonia.Q
            elif self.colonia.update_estrategia == 2: 
                # noinspection PyTypeChecker
                self.feromonio_delta[i][j] = self.colonia.Q / self.grafico.matrix[i][j]
            else: 
                self.feromonio_delta[i][j] = self.colonia.Q / self.custo_total
