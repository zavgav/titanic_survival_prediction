from fastapi import FastAPI, Request, HTTPException
import joblib
import pandas as pd
from pydantic import BaseModel

from transformers import age_transformer, family_size, has_cabin

app = FastAPI()

# Загрузка модели из файла .pkl
model = joblib.load("model/best_model.pkl")

# Счетчик запросов
request_count = 0

# Модель для валидации входных данных
class PredictionInput(BaseModel):
    Pclass: int
    Name: object
    Sex: object
    Age: float
    SibSp: int
    Parch: int
    Ticket: object | None
    Fare: float
    Cabin: object | None
    Embarked: object | None

@app.get("/stats")
def stats():
    return {'request_count': request_count}

@app.get("/health")
def health():
    return {'status': 'ok'}

@app.post("/predict_model")
def predict_model(input_data: PredictionInput):
    global request_count
    request_count += 1

    print("Received data:", input_data)  # Отладочный вывод

    # Создание DataFrame из входных данных
    new_data = pd.DataFrame({
        'Pclass': [input_data.Pclass],
        'Name': [input_data.Name],
        'Sex': [input_data.Sex],
        'Age': [input_data.Age],
        'SibSp': [input_data.SibSp],
        'Parch': [input_data.Parch],
        'Ticket': [input_data.Ticket],
        'Fare': [input_data.Fare],
        'Cabin': [input_data.Cabin],
        'Embarked': [input_data.Embarked]
    })

    # Предсказание
    prediction = model.predict(new_data)

    # Преобразование результата
    result = "Survived" if prediction[0] == 1 else "Died"

    return {"Prediction": result}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5000)