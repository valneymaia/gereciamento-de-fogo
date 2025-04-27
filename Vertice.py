from random import randint, seed
from enum import Enum, auto

class TipoVertice(Enum):
    NORMAL = auto()
    POSTO_BRIGADA = auto()
    PONTO_COLETA = auto()

class Vertice:
    def __init__(self, id, tipo=TipoVertice.NORMAL):
        """
        Inicializa um vértice do grafo de combate a incêndios
        Args:
            id: Identificador único do vértice
            tipo: Tipo do vértice (NORMAL, POSTO_BRIGADA, PONTO_COLETA)
        """
        self.id = id
        self.tipo = tipo
        self.queimando = False
        self.protegido = False
        self.agua_necessaria = self._calcular_agua_necessaria()
        self.equipes_necessarias = self._calcular_equipes_necessarias()
        self.vizinhos = []  # Lista de arestas para vértices vizinhos
        
    def __lt__(self, other):
        """Permite comparação para ordenação"""
        return self.id < other.id
        
    def _calcular_agua_necessaria(self):
        """
        Calcula a água necessária para apagar um incêndio neste vértice
        Baseado em características do terreno (implementação simplificada)
        """
        if self.tipo != TipoVertice.NORMAL:
            return 0  # Postos e pontos de coleta não queimam
            
        # Baseado em características aleatórias do terreno
        seed(self.id)  # Para ser determinístico
        return randint(100, 1000)  # Litros necessários
        
    def _calcular_equipes_necessarias(self):
        """
        Calcula o número de equipes necessárias para combater o incêndio
        """
        if self.tipo != TipoVertice.NORMAL:
            return 0
            
        seed(self.id + 1)  # Diferente seed do cálculo de água
        return randint(1, 3)  # Número de equipes necessárias
        
    def iniciar_incendio(self):
        """Marca o vértice como queimando, se for possível"""
        if self.tipo == TipoVertice.NORMAL and not self.protegido:
            self.queimando = True
            return True
        return False
        
    def apagar_incendio(self):
        """Tenta apagar o incêndio neste vértice"""
        if self.queimando:
            self.queimando = False
            return True
        return False
        
    def adicionar_vizinho(self, vizinho, peso):
        """Adiciona um vértice vizinho com o peso da aresta"""
        self.vizinhos.append((vizinho, peso))
        
    def risco_incendio(self):
        """
        Calcula um fator de risco para propagação de incêndio
        Baseado em características do terreno (implementação simplificada)
        """
        if self.tipo != TipoVertice.NORMAL:
            return 0
            
        seed(self.id + 2)
        return randint(1, 10)  # Fator de risco de 1 a 10