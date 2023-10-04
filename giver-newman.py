
import math
import json
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import pandas as pd


import networkx as nx

def calcular_centralidade_de_intermediacao_das_arestas(grafo):
    centralidade_intermediacao = nx.edge_betweenness_centrality(grafo)
    return centralidade_intermediacao

def encontrar_aresta_com_maior_centralidade(grafo):
    centralidade_intermediacao = calcular_centralidade_de_intermediacao_das_arestas(grafo)
    maior_centralidade = max(centralidade_intermediacao.values())
    aresta_maior_centralidade = [aresta for aresta, centralidade in centralidade_intermediacao.items() if centralidade == maior_centralidade][0]
    return aresta_maior_centralidade

def algoritmo_girvan_newman(grafo):
    componentes = list(nx.connected_components(grafo))
    while len(componentes) == 1:
        aresta_a_remover = encontrar_aresta_com_maior_centralidade(grafo)
        grafo.remove_edge(*aresta_a_remover)
        componentes = list(nx.connected_components(grafo))
    return componentes

def haversine(lat1, lon1, lat2, lon2):
    # Converte graus para radianos
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Diferença entre as latitudes e longitudes
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Fórmula de Haversine
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    # Raio da Terra em quilômetros (aproximadamente)
    r = 6371.0

    # Distância em quilômetros
    distance = r * c

    return distance


def get_data():
    file_name = "./data.json"
    format = []
    # abre o arquivo json e coloca os dados na variavel format
    with open(file_name, "r") as json_file:
        format = json.load(json_file)

    return format

def write_result(data):
    file_name = "./result.json"
    with open(file_name, "w") as json_file:
        json.dump(data, json_file, indent=4)  


def filter_data(data):
    # remove os dados duplicados por id e latitude e longitude
    new_data = []
    # cria um dicionario com os dados filtrados
    for i in range(len(data)):
        same = False
        for j in range(len(new_data)):
            if data[i]["id"] == new_data[j]["id"] and data[i]["latitude"] == new_data[j]["latitude"] and data[i]["longitude"] == new_data[j]["longitude"]:
                same = True
                break
        if not same:
            new_data.append(data[i])
    return new_data

def create_graph(data):
    grafo = []

    for i in range(len(data)):
        grafo.append({
            ## use the real id
            # "id": data[i],
            "id": i,
            "value": data[i]["value"],
            "neighbors": []
        })

    for i in range(len(grafo)):
        for j in range(len(grafo)):
            if i != j and data[i]["id"] != data[j]["id"]:
                distance = haversine(data[i]["latitude"], data[i]["longitude"], data[j]["latitude"], data[j]["longitude"])
                if distance < 100:
                    grafo[i]["neighbors"].append(grafo[j]["id"])

    return grafo


data = get_data()
grafo = create_graph(filter_data(data))
# write_result(grafo)

G = nx.Graph()
for item in grafo:
    node_id = item["id"]
    neighbors = item["neighbors"]
    G.add_node(node_id)  # Add the node
    
    # Add edges to neighbors
    for neighbor in neighbors:
        G.add_edge(node_id, neighbor)
print(G)
nx.draw(G, with_labels=True, node_color="blue")

comunidades = algoritmo_girvan_newman(G)

# Imprima as comunidades detectadas
for i, comunidade in enumerate(comunidades):
    print(f"Comunidade {i+1}: {comunidade}")

plt.show()