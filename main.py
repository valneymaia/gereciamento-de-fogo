from copy import deepcopy
from leitura_dados import ler_dados_do_arquivo
from Grafo import Grafo
from Vertice import Vertice, TipoVertice
from CaminhaoBrigada import CaminhaoBrigada
from EquipeBrigada import EquipeBrigada
import time

def main():
    arquivo_entrada = "entrada.txt"
    dados = ler_dados_do_arquivo(arquivo_entrada)
    if not dados:
        print("Erro ao carregar dados do arquivo.")
        return

    grafo_original = Grafo(dados['grafo'], dados['postos_brigada'], dados['pontos_coleta'])
    inicio_incendio = dados['inicio_incendio']

    # Configurações
    CAPACIDADE_CAMINHAO = 5000  # litros
    EQUIPES_POR_CAMINHAO = 3     # brigadistas
    TEMPO_MAXIMO = 8 * 60        # 8 horas em minutos
    INTERVALO_PROPAGACAO = 30    # minutos entre propagações

    print("\n=== SIMULAÇÃO DE COMBATE A INCÊNDIOS ===")
    print(f"Incêndio iniciado no vértice {inicio_incendio.id}")
    print(f"Postos: {[p.id for p in dados['postos_brigada']]}")
    print(f"Pontos de água: {[p.id for p in dados['pontos_coleta']]}\n")

    # Inicialização
    grafo = deepcopy(grafo_original)
    inicio_incendio = next(v for v in grafo.adjacencias.keys() if v.id == inicio_incendio.id)
    inicio_incendio.iniciar_incendio()
    grafo.vertices_queimando.add(inicio_incendio)

    # Recursos
    caminhoes = [CaminhaoBrigada(posto, CAPACIDADE_CAMINHAO, EQUIPES_POR_CAMINHAO) 
                for posto in grafo.postos_brigada]
    equipes = [EquipeBrigada(posto, grafo) for posto in grafo.postos_brigada]

    # Simulação
    tempo_decorrido = 0
    vertices_salvos = len(grafo.adjacencias) - 1
    sucesso = False

    while tempo_decorrido <= TEMPO_MAXIMO:
        print(f"\n⏱️ Tempo: {tempo_decorrido} minutos")
        
        if not grafo.tem_incendio_ativo():
            sucesso = True
            break
            
        print(f"🔥 Vértices em chamas: {[v.id for v in grafo.vertices_queimando]}")
        
        # Propagação do fogo
        if tempo_decorrido % INTERVALO_PROPAGACAO == 0 and grafo.vertices_queimando:
            novos_queimando = grafo.propagar_fogo()
            if novos_queimando:
                vertices_salvos -= len(novos_queimando)
                print(f"🚨 Fogo se propagou para: {[v.id for v in novos_queimando]}")
        
        # Ação das equipes
        for equipe in equipes:
            if equipe.disponivel and grafo.vertices_queimando:
                alvos = [v for v in grafo.adjacencias.keys() 
                        if any(viz in grafo.vertices_queimando for viz, _ in grafo.adjacencias[v])]
                if alvos:
                    equipe.executar_missao(alvos)
        
        # Ação dos caminhões
        for caminhao in caminhoes:
            if caminhao.localizacao_atual in grafo.vertices_queimando:
                if not caminhao.combater_incendio(caminhao.localizacao_atual, grafo):
                    caminhao.reabastecer(grafo)
            elif grafo.vertices_queimando:  # Verifica se ainda há vértices em chamas
                # Encontra o vértice em chamas mais próximo
                alvos_disponiveis = [v for v in grafo.vertices_queimando]
                if alvos_disponiveis:
                    alvo = min(
                        alvos_disponiveis,
                        key=lambda v: grafo.dijkstra(caminhao.localizacao_atual, v)[0]
                    )
                    caminhao.deslocar(alvo, grafo)
        
        # Atualização do tempo
        tempo_decorrido += 5  # Incremento de tempo da simulação
        time.sleep(0.5)

    # Relatório
    print("\n=== RELATÓRIO FINAL ===")
    status = "✅ CONTIDO" if sucesso else "❌ NÃO CONTIDO"
    print(f"\n{status} | Tempo: {tempo_decorrido}/{TEMPO_MAXIMO} minutos")
    print(f"Vértices salvos: {vertices_salvos}/{len(grafo.adjacencias)}")
    print(f"Vértices queimados: {len(grafo.vertices_queimando) if grafo.vertices_queimando else 0}")
    
    print("\n🔧 Recursos utilizados:")
    for i, caminhao in enumerate(caminhoes, 1):
        print(f"Caminhão {i}:")
        print(f"  🚛 Rota: {[v.id for v in caminhao.caminho_percorrido]}")
        print(f"  💧 Água usada: {caminhao.agua_utilizada}L")
        print(f"  ⏱ Tempo ativo: {caminhao.tempo_gasto} minutos")
    
    for i, equipe in enumerate(equipes, 1):
        print(f"Equipe {i}: Protegeu {equipe.vertices_protegidos} vértices")

if __name__ == "__main__":
    main()