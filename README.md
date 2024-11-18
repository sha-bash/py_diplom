# Backend-приложение для автоматизации закупок

## Порядок установки и запуска

1. Убедитесь, что у вас установлены:
   - Docker
   - Docker Compose
   - Git

2. Клонируйте репозиторий:
   ```bash
   git clone <url-репозитория>
   cd netology_diplom
   ```

3. Создайте файл .env в корневой директории проекта со следующими переменными:
   ```
   POSTGRES_USER=your_username
   POSTGRES_PASSWORD=your_password
   POSTGRES_DB=your_database_name
   POSTGRES_HOST=db
   POSTGRES_PORT=5432
   ```

4. Создайте и активируйте виртуальное окружение:
   ```bash
   python -m venv venv
   source venv/bin/activate  # для Linux/MacOS
   venv\Scripts\activate     # для Windows
   ```

5. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

6. Запустите базу данных через Docker Compose:
   ```bash
   docker-compose up -d
   ```

7. Выполните миграции базы данных:
   ```bash
   python manage.py migrate
   ```

8. Создайте суперпользователя:
   ```bash
   python manage.py createsuperuser
   ```

9. Запустите сервер разработки:
   ```bash
   python manage.py runserver
   ```

## Доступные эндпоинты

- Административная панель: http://localhost:8000/admin/
- API endpoints: http://localhost:8000/api/
  - /api/shops/ - список магазинов
  - /api/categories/ - список категорий
  - /api/products/ - список продуктов
  - /api/product-info/ - информация о продуктах

## Примечания

- Для доступа к API необходима аутентификация
- База данных работает на порту 5431 (можно изменить в docker-compose.yaml)
- Все API эндпоинты требуют авторизации
