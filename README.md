![unknown_2025 04 16-16 55](https://github.com/user-attachments/assets/9e634bcd-2120-4517-8cc8-1fb90eb2ee8e)
# Insurance Buyers Application


## Запуск приложения

### Подготовка

Перед запуском, если контейнеры уже существуют, остановите и удалите их:

```bash
# Остановить и удалить контейнеры
docker rm -f titanic-api streamlit-service
```

### Запуск

Для запуска приложения:

```bash
# Сборка и запуск контейнеров
docker compose up -d
```

### Перезапуск с полной пересборкой

Если нужно пересобрать образы с нуля:

```bash
docker compose down
docker compose build --no-cache
docker compose up -d
```
