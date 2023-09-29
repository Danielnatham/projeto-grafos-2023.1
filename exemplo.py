import networkx as nx

def girvan_newman(G):
    # Crie uma cópia da rede para que não a modifiquemos diretamente
    G_copy = G.copy()
    
    # Inicialize uma lista para armazenar as comunidades detectadas
    communities = []
    
    while G_copy.number_of_edges() > 0:
        # Calcule a centralidade de betweenness de todas as arestas na rede
        edge_betweenness = nx.edge_betweenness_centrality(G_copy)
        
        # Encontre a aresta com a maior centralidade de betweenness
        max_betweenness = max(edge_betweenness.values())
        
        # Encontre todas as arestas com a maior centralidade de betweenness
        max_betweenness_edges = [edge for edge, betweenness in edge_betweenness.items() if betweenness == max_betweenness]
        
        # Remova as arestas com a maior centralidade de betweenness
        G_copy.remove_edges_from(max_betweenness_edges)
        
        # Encontre as componentes conectadas na rede resultante
        components = list(nx.connected_components(G_copy))
        
        # Se o número de componentes conectadas aumentou, adicione as comunidades à lista
        if len(components) > len(communities):
            communities = components
    
    return communities

# Exemplo de uso:
# Crie um grafo de exemplo
G = nx.karate_club_graph()

# Encontre as comunidades usando Girvan-Newman
detected_communities = girvan_newman(G)

# Imprima as comunidades
for i, community in enumerate(detected_communities):
    print(f"Comunidade {i + 1}: {community}")
