
import math
import json
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
def create_graph(data):
    grafo = []

    for i in range(len(data)):
        grafo.append({
            "id": data[i]["id"],
            "location": data[i]["location"],
            "parameter": data[i]["parameter"],
            "value": data[i]["value"],
            "entity": data[i]["entity"],
            "sensorType": data[i]["sensorType"],
            "latitude": data[i]["latitude"],
            "longitude": data[i]["longitude"],
            "neighbors": []
        })

    for i in range(len(grafo)):
        for j in range(len(grafo)):
            if i != j:
                distance = haversine(grafo[i]["latitude"], grafo[i]["longitude"], grafo[j]["latitude"], grafo[j]["longitude"])
                if distance < 100:
                    grafo[i]["neighbors"].append(grafo[j]["id"])

    return grafo


data = get_data()
grafo = create_graph(data)
write_result(grafo)

