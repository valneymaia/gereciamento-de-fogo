import heapq
from random import randint

from Vertice import TipoVertice


    
   



class Grafo:
    def __init__(self, adjacencias, postos_brigada, pontos_coleta):
        self.adjacencias = adjacencias  # Dicionário de adjacências
        self.postos_brigada = postos_brigada  # Lista de vértices que são postos de brigada
        self.pontos_coleta = pontos_coleta  # Lista de vértices que são pontos de coleta de água
        self.caminhoes = []  # Lista de caminhões de combate a incêndio
        self.vertices_queimando = set()  # Conjunto de vértices em chamas
        
    def adicionar_aresta(self, origem, destino, peso):
        """Adiciona uma aresta bidirecional com peso entre dois vértices"""
        if origem not in self.adjacencias:
            self.adjacencias[origem] = []
        if destino not in self.adjacencias:
            self.adjacencias[destino] = []
        self.adjacencias[origem].append((destino, peso))
        self.adjacencias[destino].append((origem, peso))

    def dijkstra(self, origem, destino):
        """
        Implementação do algoritmo de Dijkstra para encontrar o menor caminho
        Retorna a distância total e o caminho como uma lista de vértices
        """
        distancias = {vertice: float('inf') for vertice in self.adjacencias}
        anteriores = {vertice: None for vertice in self.adjacencias}
        distancias[origem] = 0
        heap = [(0, origem)]  # (distância acumulada, vértice atual)

        while heap:
            dist_atual, vertice_atual = heapq.heappop(heap)
            
            if vertice_atual == destino:
                break

            if dist_atual > distancias[vertice_atual]:
                continue

            for vizinho, peso in self.adjacencias[vertice_atual]:
                # Ignora vértices que já estão queimados
                if vizinho in self.vertices_queimando:
                    continue
                    
                nova_dist = dist_atual + peso
                if nova_dist < distancias[vizinho]:
                    distancias[vizinho] = nova_dist
                    anteriores[vizinho] = vertice_atual
                    heapq.heappush(heap, (nova_dist, vizinho))

        caminho = self._reconstruir_caminho(anteriores, destino)
        return distancias[destino], caminho

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
            Propaga o fogo para vértices vizinhos
            Retorna lista de novos vértices que começaram a queimar
            """
            novos_queimando = set()
            
            for vertice in list(self.vertices_queimando):
                for vizinho, _ in self.adjacencias[vertice]:
                    if (vizinho not in self.vertices_queimando and 
                        vizinho.tipo == TipoVertice.NORMAL and
                        not vizinho.protegido):
                        novos_queimando.add(vizinho)
            
            self.vertices_queimando.update(novos_queimando)
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