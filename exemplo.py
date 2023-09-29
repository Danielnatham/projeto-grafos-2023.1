
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import pandas as pd

# Função utilizada para encontrar os vizinhos dos nós de um grafo e retorna essa informação na forma de dicionário
def pegar_vizinhos(grafo):
  vizinhos = {}
  for n in grafo:
    vizinhos[n] = list(grafo.neighbors(n))
  
  return vizinhos

# Função para criar um grafo a partir dos grupos de nós (comunidades) e dos vizinhos do grafo original
def criarGrafo(vizinhos, grupo_de_nos):
  novos_grafos = []

  for x in range(len(grupo_de_nos)):
    grupo = grupo_de_nos[x]
    novo_grafo = nx.Graph()
    for no in grupo:
      lista_de_vizinhos_no = vizinhos[no]
      for v in lista_de_vizinhos_no:
        if (v in grupo):
          novo_grafo.add_edge(no, v)
    novos_grafos.append(novo_grafo)

  return novos_grafos

# Função para criar grafo da maior componente de uma rede
def criarGrafoDaMaiorComponente(vizinhos, maiorComponente):
  novo_grafo = nx.Graph()
  for no in maiorComponente:
    lista_de_vizinhos_no = vizinhos[no]
    for v in lista_de_vizinhos_no:
      if (v in maiorComponente):
        novo_grafo.add_edge(no, v)
  
  return novo_grafo

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

G = nx.karate_club_graph()

# Encontre as comunidades usando Girvan-Newman
detected_communities = girvan_newman(G)

np.random.seed(0)
grafo_karate = nx.karate_club_graph()
cores = []
nx.draw(grafo_karate,with_labels=True)
plt.show()

