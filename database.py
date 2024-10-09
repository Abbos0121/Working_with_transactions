import psycopg2
from dotenv import load_dotenv
load_dotenv()

try:
    # Установка соединения с PostgreSQL
    connection = psycopg2.connect(
        host="DB_HOST",  # Адрес хоста (если на том же ПК — localhost)
        port="DB_PORT",  # Порт (по умолчанию 5432)
        database="DB_NAME",  # Имя базы данных
        user="DB_USER",  # Имя пользователя
        password="DB_PASSWORD",  # Пароль пользователя
    )

    # Создание курсора для выполнения SQL-запросов
    cursor = connection.cursor()

    # Выполнение SQL-запроса
    cursor.execute("SELECT version();")

    # Получение и вывод результата
    db_version = cursor.fetchone()
    print(f"PostgreSQL версия: {db_version}")

except (Exception, psycopg2.DatabaseError) as error:
    print(f"Ошибка подключения: {error}")

finally:
    if connection:
        cursor.close()
        connection.close()
        print("Соединение с PostgreSQL закрыто")
