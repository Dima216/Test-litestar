# Клонирование репозитория
git clone git@github.com:Dima216/Test-litestar.git

# Запуск проекта
docker compose up --build -d

# Применение миграций
docker compose exec -it litestar alembic upgrade head

# Ушло времени
2 дня