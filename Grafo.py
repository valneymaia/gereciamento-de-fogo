from collections import deque
import heapq
from random import randint, random

from Vertice import TipoVertice

class Grafo:
    def __init__(self, adjacencias, postos_brigada, pontos_coleta):
        self.adjacencias = adjacencias  # Dicionário de adjacências
        self.postos_brigada = postos_brigada  # Lista de vértices que são postos de brigada
        self.pontos_coleta = pontos_coleta  # Lista de vértices que são pontos de coleta de água
        self.caminhoes = []  # Lista de caminhões de combate a incêndio
        self.vertices_queimando = set()  # Conjunto de vértices em chamas
        self.vertices_queimados_total = set() 
        self.vertices_queimados = set()
        self.vertices_protegidos = set()

    def adicionar_aresta(self, origem, destino, peso): #  aresta bidirecional
        if origem not in self.adjacencias:
            self.adjacencias[origem] = []
        if destino not in self.adjacencias:
            self.adjacencias[destino] = []
        self.adjacencias[origem].append((destino, peso))
        self.adjacencias[destino].append((origem, peso))

    def dijkstra(self, origem, destino):
        distancias = {vertice: float('inf') for vertice in self.adjacencias}
        anteriores = {vertice: None for vertice in self.adjacencias}
        distancias[origem] = 0
        heap = [(0, origem)]  # (distância acumulada em minutos, vértice atual)

        while heap:
            dist_atual, vertice_atual = heapq.heappop(heap)
            if vertice_atual == destino:
                break

            for vizinho, peso in self.adjacencias[vertice_atual]:
                nova_dist = dist_atual + peso  # peso = minutos de deslocamento
                if nova_dist < distancias[vizinho]:
                    distancias[vizinho] = nova_dist
                    anteriores[vizinho] = vertice_atual
                    heapq.heappush(heap, (nova_dist, vizinho))

        caminho = self._reconstruir_caminho(anteriores, destino)
        return distancias[destino], caminho  # Retorna tempo total em minutos e caminho

    def _reconstruir_caminho(self, anteriores, destino): 
        caminho = []
        atual = destino
        while atual is not None:
            caminho.append(atual)
            atual = anteriores[atual]
        return caminho[::-1]  # Inverte para ficar na ordem correta
    
    def propagar_fogo(self):
        """
        Propaga o fogo para os vizinhos diretos (1 nível de BFS) com 75% de chance.
        """
        novos_queimando = set()
        visitados = set()
        fila = deque((v, 0) for v in self.vertices_queimando)  # (vértice, profundidade)

        while fila:
            vertice, profundidade = fila.popleft()
            visitados.add(vertice)

            # Só propaga para o primeiro nível de vizinhos
            if profundidade >= 1:
                continue

            for vizinho, _ in self.adjacencias[vertice]:
                if (vizinho.tipo == TipoVertice.NORMAL and
                    not vizinho.protegido and
                    not vizinho.queimando and
                    not vizinho.queimado and
                    vizinho not in visitados and
                    random() < 0.75):

                    vizinho.queimando = True
                    novos_queimando.add(vizinho)
                    visitados.add(vizinho)
                    fila.append((vizinho, profundidade + 1))  # só avança 1 nível

        self.vertices_queimando.update(novos_queimando)

        for vertice in list(self.vertices_queimando):
            vertice.queimado = True
            self.vertices_queimados.add(vertice)

        return list(novos_queimando)

    def tem_incendio_ativo(self):
        """Verifica se ainda há vértices em chamas"""
        return len(self.vertices_queimando) > 0
    
    def apagar_incendio(self, vertice):
        """Remove um vértice do conjunto de vértices em chamas"""
        if vertice in self.vertices_queimando:
            vertice.queimando = False
            self.vertices_queimando.remove(vertice)
            # Não marca como queimado porque foi apagado a tempo
            return True
        return False