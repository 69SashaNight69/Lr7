# Вказуємо базовий образ Python
FROM python:3.9-slim

# Встановлюємо необхідні системні пакети
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Створюємо робочий каталог
WORKDIR /app

# Копіюємо requirements.txt в робочий каталог
COPY requirements.txt .

# Встановлюємо Python-залежності
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо весь проект в робочий каталог
COPY . .

# Відкриваємо порт для MongoDB
EXPOSE 27017

# Вказуємо команду для запуску програми
CMD ["python", "main.py"]

