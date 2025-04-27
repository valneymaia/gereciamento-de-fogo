class CaminhaoBrigada:
    def __init__(self, posto_base, capacidade_agua, equipe):
        self.posto_base = posto_base
        self.capacidade_total = capacidade_agua
        self.agua_atual = capacidade_agua
        self.equipe = equipe
        self.localizacao_atual = posto_base
        self.tempo_gasto = 0
        self.agua_utilizada = 0
        self.caminho_percorrido = [posto_base]
        self.historico_acoes = []  # Inicializa o histórico de ações

    def registrar_acao(self, tipo, vertice=None, tempo=0, agua=0):
        """Registra uma ação no histórico"""
        self.historico_acoes.append({
            'tipo': tipo,
            'vertice': vertice.id if vertice else None,
            'tempo': tempo,
            'agua': agua
        })

    def combater_incendio(self, vertice, grafo):
        """Retorna True se apagou o incêndio e consome tempo"""
        if self.agua_atual >= vertice.agua_necessaria:
            self.agua_atual -= vertice.agua_necessaria
            self.agua_utilizada += vertice.agua_necessaria
            if grafo.apagar_incendio(vertice):
                self.tempo_gasto += 10  # 10 minutos para apagar
                self.registrar_acao('combate', vertice, vertice.agua_necessaria, True)
                return True
        return False

    def deslocar(self, destino, grafo):
        """Retorna o tempo gasto no deslocamento"""
        distancia, caminho = grafo.dijkstra(self.localizacao_atual, destino)
        self.tempo_gasto += distancia
        self.localizacao_atual = destino
        self.caminho_percorrido.extend(caminho[1:])
        self.registrar_acao('deslocar', destino, distancia)
        return distancia  # Retorna o tempo gasto

    def reabastecer(self, grafo):
        """Reabastece o caminhão"""
        tempo_reabastecimento = 15
        self.tempo_gasto += tempo_reabastecimento
        self.agua_atual = self.capacidade_total
        self.registrar_acao('reabastecer', self.localizacao_atual, tempo_reabastecimento)