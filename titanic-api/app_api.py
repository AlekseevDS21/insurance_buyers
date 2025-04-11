'''
Давайте создадим простое API с тремя ручками: одна для предсказания выживания (/predict), 
другая для получения количества сделанных запросов (/stats), и третья для проверки работы API (/health).

Шаг 1: Установка необходимых библиотек
Убедитесь, что у вас установлены необходимые библиотеки:
pip install fastapi uvicorn pydantic scikit-learn pandas

Шаг 2: Создание app_api.py
Шаг 3: Запустите ваше приложение: python app_api.py
Шаг 4: Тестирование API
Теперь вы можете протестировать ваше API с помощью curl или любого другого инструмента для отправки HTTP-запросов.

Проверка работы API (/health)
curl -X GET http://127.0.0.1:5000/health
curl -X GET http://127.0.0.1:5000/stats
curl -X POST http://127.0.0.1:5000/predict_model -H "Content-Type: application/json" -d "{\"Pclass\": 3, \"Age\": 22.0, \"Fare\": 7.2500}"
'''

from fastapi import FastAPI, Request, HTTPException
import pickle
import pandas as pd
from pydantic import BaseModel
import random  # добавлено для генерации случайных предсказаний
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Загрузка модели из файла pickle
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

# Счетчик запросов
request_count = 0

# Обновленная модель для валидации входных данных
class PredictionInput(BaseModel):
    Pclass: int
    Age: int
    CarAge: int
    InsuranceCost: int
    DaysWithCompany: int
    HasLicence: int
    HasDamage: int

@app.get("/stats")
def stats():
    return {"request_count": request_count}

@app.get("/health")
def health():
    return {"status": "OK"}

@app.post("/predict_model")
async def predict_model(input_data: PredictionInput):
    global request_count
    request_count += 1

    # Логируем входные данные для отладки
    logger.info(f"Получены данные: {input_data.dict()}")

    try:
        # Создаем DataFrame из данных
        new_data = pd.DataFrame({
            'Pclass': [input_data.Pclass],
            'Age': [input_data.Age],
            'CarAge': [input_data.CarAge],
            'InsuranceCost': [input_data.InsuranceCost],
            'DaysWithCompany': [input_data.DaysWithCompany],
            'HasLicence': [input_data.HasLicence],
            'HasDamage': [input_data.HasDamage]
        })

        logger.info(f"DataFrame создан: {new_data}")

        # Генерируем случайное предсказание
        random_prediction = random.choice([0, 1])

        # Преобразование результата в человеко-читаемый формат
        result = "Купит страховку" if random_prediction == 1 else "Не купит страховку"

        logger.info(f"Предсказание: {result}")
        return {"prediction": result}

    except Exception as e:
        logger.error(f"Ошибка при обработке данных: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)