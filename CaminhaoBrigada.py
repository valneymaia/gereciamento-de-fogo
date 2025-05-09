from Vertice import TipoVertice

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
        self.historico_acoes = []  

    def registrar_acao(self, tipo, vertice=None, tempo=0, agua=0):
        self.historico_acoes.append({
            'tipo': tipo,
            'vertice': vertice.id if vertice else None,
            'tempo': tempo,
            'agua': agua
        })

    def combater_incendio(self, vertice, grafo):   # Se apagou fogo retorna verdadeiro e gasta tempo
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
        # Verifica se já está em um ponto de coleta ou posto
        if (self.localizacao_atual.tipo == TipoVertice.PONTO_COLETA or 
            self.localizacao_atual.tipo == TipoVertice.POSTO_BRIGADA):
            tempo_reabastecimento = 0
            self.tempo_gasto += tempo_reabastecimento
            self.agua_atual = self.capacidade_total
            self.registrar_acao('reabastecer', self.localizacao_atual, tempo_reabastecimento)
            print(f"⛽ Caminhão reabastecido na Lagoa  {self.localizacao_atual.id} (água: {self.agua_atual}L)")
            return True
        else:
            # Encontra o ponto de coleta mais próximo
            ponto_agua = None
            menor_distancia = float('inf')
            
            for ponto in grafo.pontos_coleta + grafo.postos_brigada:
                distancia, _ = grafo.dijkstra(self.localizacao_atual, ponto)
                if distancia < menor_distancia:
                    menor_distancia = distancia
                    ponto_agua = ponto
            
            if ponto_agua:
                tempo_desloc = self.deslocar(ponto_agua, grafo)
                print(f"🚚 Caminhão indo para ponto de água {ponto_agua.id} (tempo: {tempo_desloc}min)")
                # Reabastece após chegar
                self.tempo_gasto += 0  # Tempo instantâneo
                self.agua_atual = self.capacidade_total
                self.registrar_acao('reabastecer', ponto_agua, tempo_desloc)
                print(f"⛽ Caminhão reabastecido na Lagoa {ponto_agua.id} (água: {self.agua_atual}L)")
                return True
        
        print("⚠️ Não foi possível encontrar ponto de água para reabastecer")
        return False