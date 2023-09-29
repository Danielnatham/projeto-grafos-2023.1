import requests
import json
country_code = "ME"

url = "https://api.openaq.org/v2/measurements?date_to=2023-09-29T00%3A19%3A00Z&limit=100&page=1&offset=0&sort=desc&parameter=temperature&radius=1000&country=AT&order_by=datetime"

headers = {"Accept": "application/json"}

response = requests.get(url, headers=headers)

if response.status_code == 200:

    data = response.json()

    format = []
    for item in data["results"]:
        format.append({
            "id": item["locationId"], 
            "location": item["location"],
            "parameter": item["parameter"],
            "value": item["value"], 
            "entity": item["entity"],
            "sensorType": item["sensorType"],
            "latitude": item["coordinates"]["latitude"],
            "longitude": item["coordinates"]["longitude"],
        })
        
    file_name = "data.json"

    with open(file_name, "w") as json_file:
        json.dump(format, json_file, indent=4)  

    print(f"JSON data has been written to {file_name}")

else:
    print(f"Error receiving data: {response.status_code} {response.text}")

