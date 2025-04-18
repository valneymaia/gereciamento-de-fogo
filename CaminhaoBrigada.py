class CaminhaoBrigada:
    def __init__(self, posto_base, capacidade_agua, equipe):
        """
        Inicializa um caminhão de combate a incêndios
        Args:
            posto_base: Vértice onde o caminhão está alocado
            capacidade_agua: Capacidade máxima de água do caminhão
            equipe: Número de brigadistas no caminhão
        """
        self.posto_base = posto_base
        self.capacidade_total = capacidade_agua
        self.agua_atual = capacidade_agua
        self.equipe = equipe
        self.localizacao_atual = posto_base
        self.tempo_gasto = 0
        self.agua_utilizada = 0
        self.caminho_percorrido = [posto_base]
        
    def deslocar(self, destino, grafo):
        """
        Move o caminhão para o destino especificado
        Args:
            destino: Vértice de destino
            grafo: Referência ao grafo do sistema
        """
        distancia, caminho = grafo.dijkstra(self.localizacao_atual, destino)
        self.tempo_gasto += distancia
        self.localizacao_atual = destino
        self.caminho_percorrido.extend(caminho[1:])  # Evita duplicar o primeiro ponto
        
    def combater_incendio(self, vertice, grafo):
        """
        Tenta apagar o fogo em um vértice
        Args:
            vertice: Vértice que está em chamas
            grafo: Referência ao grafo do sistema
        Returns:
            True se o fogo foi apagado, False caso contrário
        """
        if self.localizacao_atual != vertice:
            self.deslocar(vertice, grafo)
            
        # Verifica se tem recursos suficientes
        if (self.agua_atual >= vertice.agua_necessaria and 
            self.equipe >= vertice.equipes_necessarias):
            
            self.agua_atual -= vertice.agua_necessaria
            self.agua_utilizada += vertice.agua_necessaria
            vertice.agua_necessaria = 0  # Marca como atendido
            
            if grafo.apagar_incendio(vertice):
                return True
                
        return False
    
    def reabastecer(self, grafo):
        """
        Reabastece o caminhão no ponto de coleta mais próximo
        Args:
            grafo: Referência ao grafo do sistema
        """
        # Encontra o ponto de coleta mais próximo
        ponto_mais_proximo = None
        menor_distancia = float('inf')
        
        for ponto in grafo.pontos_coleta + grafo.postos_brigada:  # Postos também são pontos de coleta
            if ponto == self.localizacao_atual:
                ponto_mais_proximo = ponto
                break
                
            distancia, _ = grafo.dijkstra(self.localizacao_atual, ponto)
            if distancia < menor_distancia:
                menor_distancia = distancia
                ponto_mais_proximo = ponto
        
        if ponto_mais_proximo:
            if ponto_mais_proximo != self.localizacao_atual:
                self.deslocar(ponto_mais_proximo, grafo)
            self.agua_atual = self.capacidade_total
    
    def executar_missao(self, vertice_incendio, grafo):
        """
        Executa uma missão completa de combate a incêndio
        Args:
            vertice_incendio: Vértice onde o incêndio começou
            grafo: Referência ao grafo do sistema
        Returns:
            True se o incêndio foi controlado, False caso contrário
        """
        while grafo.tem_incendio_ativo():
            # Prioriza vértices que estão queimando
            for vertice in list(grafo.vertices_queimando):
                if self.combater_incendio(vertice, grafo):
                    break
            else:
                # Se não conseguiu apagar nenhum, reabastece
                if self.agua_atual < self.capacidade_total * 0.2:  # Reabastece quando está com 20%
                    self.reabastecer(grafo)
                else:
                    # Se não há incêndios acessíveis, espera
                    return False
            
        return True