import streamlit as st 
import requests
from requests.exceptions import ConnectionError
import json
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ip_api = "titanic-api"
port_api = "5000"

# Заголовок приложения
st.title("Купит ли пользователь страховку?")

# Ввод данных
st.write("Введите данные клиента:")

# Выпадающее меню для выбора класса билета
pclass = st.selectbox("Пол", ["Мужчина", "Женщина"])

# чекбокс поле для ввода наличия прав
has_licence = st.checkbox("Есть ли у вас права?")

# поле для ввода возраста автомобиля
car_age = st.text_input("Возраст автомобиля", value=3)
if not car_age.isdigit():
    st.error("Please enter a valid number for car age.")

# поле для ввода возраста клиента
client_age = st.text_input("Введите свой возраст", value=25)
if not client_age.isdigit():
    st.error("Please enter a valid number for client age.")

# чекбокс поле для ввода было ли повреждение
has_damage = st.checkbox("Было ли повреждение автомобиля без страховки?")

# поле для ввода стоимости страховки
insurance_cost = st.text_input("Введите стоимость годовой страховки", value=100)
if not insurance_cost.isdigit():
    st.error("Please enter a valid number for insurance cost.")

# Количество дней, в течение которых клиент был связан со страховой компанией
days_with_company = st.text_input("Сколько дней вы были клиентом в страховой компании?", value=30)
if not days_with_company.isdigit():
    st.error("Please enter a valid number for days with company.")

def get_prediction(input_data):
    response = requests.post(
        "http://titanic-api:5000/predict",  # исправленный URL
        json=input_data
    )
    return response

# Кнопка для отправки запроса
if st.button("Predict"):
    # Проверка, что все поля заполнены корректно
    try:
        client_age_int = int(client_age)
        car_age_int = int(car_age)
        insurance_cost_int = int(insurance_cost)
        days_with_company_int = int(days_with_company)
        
        # Подготовка данных для отправки
        data = {
            "Pclass": 1 if pclass == "Мужчина" else 2,
            "Age": client_age_int,
            "CarAge": car_age_int,
            "InsuranceCost": insurance_cost_int,
            "DaysWithCompany": days_with_company_int,
            "HasLicence": 1 if has_licence else 0,  # Преобразуем булево значение в 0 или 1
            "HasDamage": 1 if has_damage else 0  # Преобразуем булево значение в 0 или 1
        }
        
        logger.info(f"Отправляемые данные: {data}")
        
        try:
            # Отправка запроса к API
            response = get_prediction(data)
            
            logger.info(f"Код ответа: {response.status_code}")
            logger.info(f"Тело ответа: {response.text}")
            
            # Проверка статуса ответа
            if response.status_code == 200:
                prediction = response.json()["result"]  # изменено с prediction на result
                st.success(f"Предсказание: {prediction}")
            else:
                st.error(f"Ошибка запроса: {response.status_code}")
                st.error(f"Детали: {response.text}")
        except ConnectionError as e:
            st.error(f"Ошибка соединения с сервером: {str(e)}")
        except Exception as e:
            st.error(f"Необработанная ошибка: {str(e)}")
    except ValueError:
        st.error("Пожалуйста, введите корректные числовые значения во все поля.")