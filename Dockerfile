FROM python:3.11-slim

WORKDIR /app

# Объединяем установку системных зависимостей в одну команду для сокращения слоев
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Сначала копируем только requirements.txt и устанавливаем зависимости
COPY ./api_sellers/requirements.txt /app/
# Оптимизируем установку pip пакетов
RUN pip install --no-cache-dir --disable-pip-version-check -r requirements.txt

# Затем копируем только необходимые файлы
COPY ./api_sellers/app_api.py /app/
COPY ./api_sellers/model.pkl /app/

# Используем конкретный порт для ясности
EXPOSE 5000

# Запускаем приложение
CMD ["python3", "app_api.py"]
