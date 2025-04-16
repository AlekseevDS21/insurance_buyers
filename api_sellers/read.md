

## 1. Установка зависимостей

Перед запуском убедитесь, что у вас установлены Python (3.7+) и необходимые библиотеки:

```bash
pip install fastapi uvicorn pandas scikit-learn pydantic
```

---

## 2. Запуск сервера

Скопируйте код в файл `main.py` и выполните:

```bash
uvicorn main:app --host 0.0.0.0 --port 5000 --reload
```

- Сервер будет доступен по адресу: `http://127.0.0.1:5000`  

---

## 3. Проверка работоспособности

Отправьте GET-запрос на эндпоинт `/health`:

```bash
curl http://127.0.0.1:5000/health
```

Ожидаемый ответ:

```json
{"status": "OK"}
```

---

## 4. Отправка данных для предсказания

Отправьте POST-запрос на `/predict` с JSON-данными клиента.

### Пример запроса (curl):

```bash
curl -X POST http://127.0.0.1:5000/predict \
-H "Content-Type: application/json" \
-d '{
    "Pclass": 1,
    "Age": 35,
    "CarAge": 1,
    "InsuranceCost": 30000,
    "DaysWithCompany": 200,
    "HasLicence": 1,
    "HasDamage": 0
}'
```

### Параметры запроса:

| Поле              | Тип  | Описание                          |
|-------------------|------|-----------------------------------|
| `Pclass`          | int  | Пол клиента (1 или 0)             |
| `Age`             | int  | Возраст клиента                   |
| `CarAge`          | int  | Возраст автомобиля                |
| `InsuranceCost`   | int  | Годовая стоимость страховки       |
| `DaysWithCompany` | int  | Сколько дней клиент с компанией   |
| `HasLicence`      | int  | Есть ли водительские права (1/0)  |
| `HasDamage`       | int  | Были ли аварии (1/0)              |

### Пример ответа:

```json
{"result": "Купит страховку"}
```

или

```json
{"result": "Не купит"}
```
