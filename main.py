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
    INTERVALO_PROPAGACAO = 5    # minutos entre propagações

    print("\n=== SIMULAÇÃO DE COMBATE A INCÊNDIOS ===")
    print(f"Incêndio iniciado nos vértices: {[v.id for v in dados['inicio_incendio']]}")
    print(f"Postos: {[p.id for p in dados['postos_brigada']]}")
    print(f"Pontos de água: {[p.id for p in dados['pontos_coleta']]}\n")


    # Inicialização
    grafo = deepcopy(grafo_original)
    for incendio in dados['inicio_incendio']:  # Agora é uma lista
        vertice_incendio = next(v for v in grafo.adjacencias.keys() if v.id == incendio.id)
        vertice_incendio.iniciar_incendio()
        grafo.vertices_queimando.add(vertice_incendio)

    # Recursos
    caminhoes = [CaminhaoBrigada(posto, CAPACIDADE_CAMINHAO, EQUIPES_POR_CAMINHAO) 
                for posto in grafo.postos_brigada]
    equipes = [EquipeBrigada(posto, grafo) for posto in grafo.postos_brigada]


    # Simulação
    tempo_decorrido = 0
    vertices_salvos = len(grafo.adjacencias) - len(dados['inicio_incendio'])
    sucesso = False

    print("\n=== PROGRESSO DA SIMULAÇÃO ===")

    while tempo_decorrido <= TEMPO_MAXIMO:
        print(f"\n⏱️ Tempo: {tempo_decorrido} minutos")
        
        if not grafo.tem_incendio_ativo():
            sucesso = True
            break
            
        # Mostra vértices em chamas
        queimando_antes = set(grafo.vertices_queimando)
        print(f"🔥 Vértices em chamas: {[v.id for v in queimando_antes]}")
        
        # Propagação do fogo 
        if tempo_decorrido % INTERVALO_PROPAGACAO == 0 and grafo.vertices_queimando:
            novos_queimando = grafo.propagar_fogo()
            if novos_queimando:
                vertices_salvos -= len(novos_queimando)
                print(f"🚨 Fogo se propagou para: {[v.id for v in novos_queimando]}")
        
        # Ação das equipes (tempo instantâneo para proteção)
        for equipe in equipes:
            if equipe.disponivel and grafo.vertices_queimando:
                alvos = [v for v in grafo.adjacencias.keys() 
                        if any(viz in grafo.vertices_queimando for viz, _ in grafo.adjacencias[v])]
                if alvos:
                    protegidos = equipe.executar_missao(alvos)
                    if protegidos:
                        print(f"🛡️ Equipe protegeu vértices: {[v.id for v in protegidos]}")
        
        # Ação dos caminhões
        tempo_passado_neste_ciclo = 0
        
        for caminhao in caminhoes:
            # Se está em um vértice em chamas, tenta apagar
            if caminhao.localizacao_atual in grafo.vertices_queimando:
                if caminhao.combater_incendio(caminhao.localizacao_atual, grafo):
                    print(f"🚒 Caminhão apagou fogo em {caminhao.localizacao_atual.id} (10 minutos)")
                    tempo_passado_neste_ciclo = max(tempo_passado_neste_ciclo, 10)  # Tempo para apagar
                else:
                    # Reabastece (tempo instantâneo)
                    caminhao.reabastecer(grafo)
                    print(f"⛽ Caminhão reabastecendo")
            elif grafo.vertices_queimando:
                # Encontra o incêndio mais próximo
                alvo, distancia = min(
                    ((v, grafo.dijkstra(caminhao.localizacao_atual, v)[0]) )
                    for v in grafo.vertices_queimando
                )
                
                # Move para o alvo
                tempo_desloc = caminhao.deslocar(alvo, grafo)
                print(f"🚚 Caminhão indo para vértice {alvo.id} (tempo: {tempo_desloc}min)")
                tempo_passado_neste_ciclo = max(tempo_passado_neste_ciclo, tempo_desloc)
        
        # Avança o tempo com base na ação mais longa deste ciclo
        if tempo_passado_neste_ciclo > 0:
            tempo_decorrido += tempo_passado_neste_ciclo
        else:
            # Se nenhuma ação foi tomada, avança o mínimo possível
            tempo_decorrido += 1
        
        # Mostra vértices recém-apagados
        apagados = queimando_antes - grafo.vertices_queimando
        if apagados:
            print(f"✅ Fogo apagado nos vértices: {[v.id for v in apagados]}")
        
        # Pequena pausa para visualização
        time.sleep(1.5)

  

   


    # Relatório
    print("\n=== RELATÓRIO FINAL ===")
    status = "✅ CONTIDO" if sucesso else "❌ NÃO CONTIDO"
    print(f"\n{status} | Tempo: {tempo_decorrido}/{TEMPO_MAXIMO} minutos")

    # Cálculo correto dos vértices queimados e salvos
    vertices_queimados = len(grafo.vertices_queimados_total.union(dados['inicio_incendio']))
    vertices_salvos = len(grafo.adjacencias) - vertices_queimados

    print(f"Vértices salvos: {vertices_salvos}/{len(grafo.adjacencias)}")
    print(f"Vértices queimados: {vertices_queimados}")

    # Relatório de recursos (corrigindo a indentação do tempo ativo)
    print("\n🔧 Recursos utilizados:")
    for i, caminhao in enumerate(caminhoes, 1):
        print(f"\nCaminhão {i}:")
        print(f"  🚛 Rota: {[v.id for v in caminhao.caminho_percorrido]}")
        print(f"  💧 Água usada: {caminhao.agua_utilizada}L")
        print(f"  ⏱ Tempo ativo: {caminhao.tempo_gasto} minutos")
        
     
if __name__ == "__main__":
    main()