from Vertice import Vertice, TipoVertice

def ler_dados_do_arquivo(nome_arquivo):
    try:
        with open(nome_arquivo, 'r') as arquivo:
            linhas = [linha.strip() for linha in arquivo if linha.strip()]

        if len(linhas) < 1:
            raise ValueError("O arquivo está vazio ou não contém o número de vértices.")
        num_vertices = int(linhas[0])
        if num_vertices < 3:
            raise ValueError("O número de vértices deve ser pelo menos 3.")

        adjacencias = {Vertice(i): [] for i in range(num_vertices)}
        
        # Lendo as conexões do grafo
        linha_arquivo = 1
        while linha_arquivo < len(linhas) and linhas[linha_arquivo].lower() != "fim":
            try:
                vertice1_id, vertice2_id, custo = map(int, linhas[linha_arquivo].split())
                if vertice1_id < 0 or vertice2_id < 0 or vertice1_id >= num_vertices or vertice2_id >= num_vertices or custo <= 0:
                    raise ValueError(f"Dados inválidos na conexão: {linhas[linha_arquivo]}")
                
                vertice1 = next(v for v in adjacencias.keys() if v.id == vertice1_id)
                vertice2 = next(v for v in adjacencias.keys() if v.id == vertice2_id)
                
                adjacencias[vertice1].append((vertice2, custo))
                adjacencias[vertice2].append((vertice1, custo))
                vertice1.adicionar_vizinho(vertice2, custo)
                vertice2.adicionar_vizinho(vertice1, custo)
                
            except ValueError:
                raise ValueError(f"Erro ao processar a conexão: {linhas[linha_arquivo]}")
            linha_arquivo += 1

        if linha_arquivo >= len(linhas) or linhas[linha_arquivo].lower() != "fim":
            raise ValueError("A seção de conexões não termina com 'fim'.")
        linha_arquivo += 1

        # Lendo os IDs dos postos de brigada (3 postos)
        postos_brigada = []
        if linha_arquivo + 2 >= len(linhas):
            raise ValueError("Dados dos postos de brigada ausentes ou incompletos.")
        
        for _ in range(3):
            posto_id = int(linhas[linha_arquivo])
            if posto_id < 0 or posto_id >= num_vertices:
                raise ValueError(f"ID de posto de brigada inválido: {posto_id}")
            
            posto = next(v for v in adjacencias.keys() if v.id == posto_id)
            posto.tipo = TipoVertice.POSTO_BRIGADA
            postos_brigada.append(posto)
            linha_arquivo += 1

        # Lendo os IDs dos pontos de coleta de água (2 pontos)
        pontos_coleta = []
        if linha_arquivo + 1 >= len(linhas):
            raise ValueError("Dados dos pontos de coleta ausentes ou incompletos.")
        
        for _ in range(2):
            coleta_id = int(linhas[linha_arquivo])
            if coleta_id < 0 or coleta_id >= num_vertices:
                raise ValueError(f"ID de ponto de coleta inválido: {coleta_id}")
            
            coleta = next(v for v in adjacencias.keys() if v.id == coleta_id)
            coleta.tipo = TipoVertice.PONTO_COLETA
            pontos_coleta.append(coleta)
            linha_arquivo += 1

        # Lendo os pontos iniciais do incêndio (3 vértices)
        incendios_iniciais = []
        if linha_arquivo + 2 >= len(linhas):
            raise ValueError("Dados dos pontos de incêndio ausentes ou incompletos.")
        
        for _ in range(3):
            incendio_id = int(linhas[linha_arquivo])
            if incendio_id < 0 or incendio_id >= num_vertices:
                raise ValueError(f"ID do ponto de incêndio inválido: {incendio_id}")
            
            incendio_ponto = next(v for v in adjacencias.keys() if v.id == incendio_id)
            
            # Verifica se não é posto ou ponto de coleta
            if incendio_ponto.tipo != TipoVertice.NORMAL:
                raise ValueError(f"O vértice {incendio_id} não pode ser posto/coleta e foco inicial")
                
            # Verifica se já foi adicionado
            if incendio_ponto in incendios_iniciais:
                raise ValueError(f"Vértice {incendio_id} duplicado como foco inicial")
                
            incendios_iniciais.append(incendio_ponto)
            linha_arquivo += 1

        return {
            'grafo': adjacencias,
            'postos_brigada': postos_brigada,
            'pontos_coleta': pontos_coleta,
            'inicio_incendio': incendios_iniciais
        }

    except FileNotFoundError:
        print(f"Arquivo {nome_arquivo} não encontrado.")
        return None
    except ValueError as e:
        print(f"Erro nos dados do arquivo: {e}")
        return None
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return None