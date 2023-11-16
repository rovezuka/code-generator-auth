# Используем базовый образ Python
FROM python:3.8

# Устанавливаем переменную окружения PYTHONUNBUFFERED для предотвращения буферизации вывода
ENV PYTHONUNBUFFERED 1

# Устанавливаем рабочую директорию в /app
WORKDIR /app

# Копируем зависимости проекта в контейнер
COPY requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы проекта в контейнер
COPY . /app/

# Команда для запуска приложения
CMD ["python", "run.py"]
