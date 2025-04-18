class EquipeBrigada:
    def __init__(self, posto_base, grafo):
        """
        Inicializa uma equipe de brigadistas terrestres
        Args:
            posto_base: Vértice onde a equipe está alocada
            grafo: Referência ao grafo do sistema
        """
        self.posto_base = posto_base
        self.grafo = grafo
        self.localizacao_atual = posto_base
        self.tempo_gasto = 0
        self.disponivel = True
        self.vertices_protegidos = 0
        self.caminho_percorrido = [posto_base]
        
    def deslocar(self, destino):
        """
        Move a equipe para o destino especificado
        Args:
            destino: Vértice de destino
        """
        distancia, caminho = self.grafo.dijkstra(self.localizacao_atual, destino)
        self.tempo_gasto += distancia
        self.localizacao_atual = destino
        self.caminho_percorrido.extend(caminho[1:])  # Evita duplicar o primeiro ponto
        
    def proteger_area(self, vertice):
        """
        Protege um vértice para evitar que seja queimado
        Args:
            vertice: Vértice a ser protegido
        Returns:
            True se a proteção foi bem sucedida, False caso contrário
        """
        if self.localizacao_atual != vertice:
            self.deslocar(vertice)
            
        # Verifica se o vértice ainda não está queimando
        if vertice not in self.grafo.vertices_queimando:
            self.vertices_protegidos += 1
            vertice.protegido = True  # Marca como protegido
            return True
        return False
    
    def combater_incendio(self, vertice):
        """
        Tenta apagar um incêndio diretamente (sem água, apenas ação terrestre)
        Args:
            vertice: Vértice que está em chamas
        Returns:
            True se o fogo foi contido, False caso contrário
        """
        if self.localizacao_atual != vertice:
            self.deslocar(vertice)
            
        # Só pode combater incêndios pequenos sem auxílio de caminhões
        if vertice in self.grafo.vertices_queimando and vertice.agua_necessaria == 0:
            if self.grafo.apagar_incendio(vertice):
                return True
        return False
    
    def executar_missao(self, vertices_alvo):
        """
        Executa uma missão de proteção e combate terrestre
        Args:
            vertices_alvo: Lista de vértices prioritários para proteção
        """
        self.disponivel = False
        
        for vertice in vertices_alvo:
            if vertice.protegido or vertice in self.grafo.vertices_queimando:
                continue
                
            # Prioriza vértices adjacentes a focos de incêndio
            if any(vizinho in self.grafo.vertices_queimando 
                   for vizinho, _ in self.grafo.adjacencias[vertice]):
                
                if self.proteger_area(vertice):
                    print(f"Equipe protegeu vértice {vertice.id} com sucesso")
                else:
                    print(f"Equipe não conseguiu proteger vértice {vertice.id}")
                    
        # Volta para o posto base após a missão
        self.deslocar(self.posto_base)
        self.disponivel = True