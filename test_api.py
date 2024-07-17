import requests

def add_data():
    try:
        url = 'http://127.0.0.1:8000/add_data?TV=100&radio=100&newspaper=200&sales=40000'  
        response = requests.post(url)
        print("add_data response:", response.json())  # Añadir un print para ver la respuesta
        response.raise_for_status()
        assert response.status_code == 200
        assert response.json() == "Datos ingresados"
    except Exception as e:
        print("Error in add_data:", e)



def prediccion():
    try:
        url = 'http://localhost:8000/predict?TV=100&radio=100&newspaper=200'
        response = requests.get(url)
        print("prediccion response:", response.json())
        response.raise_for_status()
        assert response.status_code == 200
        assert 'prediction' in response.json()
    except Exception as e:
        print("Error in prediccion:", e)


def retrain():
    try:
        url = 'http://localhost:8000/retrain'
        response = requests.post(url)
        response.raise_for_status()
        print("retrain response:", response.text)
        assert response.text == 'Modelo reentrenado!'
    except Exception as e:
        print("Error in retrain:", e)




if __name__ == "__main__":
    add_data()
    prediccion()
    retrain()