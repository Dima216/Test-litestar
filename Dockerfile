# Используем официальный образ Python
FROM python:3.12

# Устанавливаем рабочий каталог
WORKDIR /code

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev

# Обновляем pip
RUN pip install --upgrade pip

# Устанавливаем Poetry
RUN python3 -m venv /opt/poetry \
    && /opt/poetry/bin/pip install -U pip setuptools \
    && /opt/poetry/bin/pip install poetry==1.8.3

# Копируем файлы pyproject.toml и poetry.lock
COPY pyproject.toml poetry.lock ./

# Копируем конфигурации alembic
COPY alembic.ini ./
COPY ./alembic /code/alembic

# Отключаем создание виртуальных окружений
RUN /opt/poetry/bin/poetry config virtualenvs.create false

# Устанавливаем зависимости с помощью Poetry
RUN /opt/poetry/bin/poetry install --only main

# Копируем приложение
COPY ./app /code/app

# Открываем порт для приложения
EXPOSE 8000
