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
        
    def adicionar_aresta(self, origem, destino, peso):
        """Adiciona uma aresta bidirecional com peso entre dois vértices"""
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
        """Reconstroi o caminho a partir do dicionário de vértices anteriores"""
        caminho = []
        atual = destino
        while atual is not None:
            caminho.append(atual)
            atual = anteriores[atual]
        return caminho[::-1]  # Inverte para ficar na ordem correta
    
    def propagar_fogo(self):
        """
        Versão alternativa com BFS e probabilidade separada
        """
        # Primeiro encontra todos os vértices candidatos a propagação com BFS
        candidatos = set()
        visitados = set()
        fila = list(self.vertices_queimando)
        
        while fila:
            vertice_atual = fila.pop(0)
            visitados.add(vertice_atual)
            
            for vizinho, _ in self.adjacencias[vertice_atual]:
                if (vizinho not in self.vertices_queimando and 
                    vizinho not in visitados and
                    vizinho.tipo == TipoVertice.NORMAL and
                    not vizinho.protegido):
                    
                    candidatos.add(vizinho)
                    fila.append(vizinho)
        
        # Aplica a probabilidade de 50% nos candidatos
        novos_queimando = {v for v in candidatos if random() < 0.5}
        
        # Atualiza os conjuntos
        self.vertices_queimando.update(novos_queimando)
        self.vertices_queimados_total.update(novos_queimando)
        
        return list(novos_queimando)

    def tem_incendio_ativo(self):
        """Verifica se ainda há vértices em chamas"""
        return len(self.vertices_queimando) > 0
    
    def apagar_incendio(self, vertice):
        """Remove um vértice do conjunto de vértices em chamas"""
        if vertice in self.vertices_queimando:
            self.vertices_queimando.remove(vertice)
            return True
        return False
