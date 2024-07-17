from fastapi import FastAPI, HTTPException
import uvicorn
import os
import pickle
import pandas as pd
import sqlite3
import requests

# Cargando el modelo
model_path = './data/advertising_model.pkl'
with open(model_path, 'rb') as model_file:
    model = pickle.load(model_file)


df = pd.read_csv('./data/Advertising.csv')
conn = sqlite3.connect('Adv_data.db')
df.to_sql('Advertising', conn, if_exists='replace', index=False)

app = FastAPI()

conec = sqlite3.connect('Adv_data.db')
cursor = conec.cursor()

# Saludo de entrada
@app.get("/")
async def saludo():
    return "Hola, esta es una API para probar un modelo"

# 1. Endpoint de predicción
@app.get("/predict")
async def prediccion(TV: float, radio: float, newspaper: float):
   try:
        data_inversion = {'TV': TV, 'radio': radio, 'newspaper': newspaper}

        input = pd.DataFrame([data_inversion])
        prediction = model.predict(input)
        return {"Prediction": prediction[0]}

   except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
   
    

# 2. Endpoint de ingesta de datos
@app.post("/add_data")
async def add_data(TV,radio, newspaper, sales):
    try:
        cursor.execute('''INSERT INTO Advertising (TV, radio, newspaper, sales) 
                        VALUES (?,?,?,?)''', (TV,radio,newspaper,sales))
        conn.commit()
        return "Datos ingresados"
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# 3. Endpoint de reentramiento del modelo
@app.post("/retrain")
async def retrain():
    try:
        df = pd.read_sql_query("SELECT * FROM Advertising", conn)

    
        X = df[['TV', 'radio', 'newspaper']]  
        y = df['sales']  
        model.fit(X, y)
        with open(model_path, 'wb') as model_file:
            pickle.dump(model, model_file)
        return "Modelo reentrenado!"

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Fin
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)