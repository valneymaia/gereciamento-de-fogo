from random import randint, seed
from enum import Enum, auto

class TipoVertice(Enum):
    NORMAL = auto()
    POSTO_BRIGADA = auto()
    PONTO_COLETA = auto()

class Vertice:
    def __init__(self, id, tipo=TipoVertice.NORMAL):
    
        self.id = id
        self.tipo = tipo #inicialmente normal
        self.queimando = False
        self.protegido = False
        self.agua_necessaria = self._calcular_agua_necessaria()
        self.equipes_necessarias = self._calcular_equipes_necessarias()
        self.vizinhos = []  # Lista de arestas para vértices vizinhos
        self.queimado = False
        
    def __lt__(self, other):
        """Permite comparação para ordenação"""
        return self.id < other.id
        
    def _calcular_agua_necessaria(self):
    
        if self.tipo != TipoVertice.NORMAL:
            return 0  # Postos e pontos de coleta não queimam
            
        # Baseado em características aleatórias do terreno
        seed(self.id) #r determinístico
        return randint(100, 1000)  # Litros necessários
        

        
    def _calcular_equipes_necessarias(self): 
        
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
    
        if self.queimando:
            self.queimando = False
            return True
        return False
        
    def adicionar_vizinho(self, vizinho, peso):
        self.vizinhos.append((vizinho, peso))
   
