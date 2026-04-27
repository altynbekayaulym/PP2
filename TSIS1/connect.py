import psycopg2

def get_connection():
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            dbname="phonebook_db",
            user="postgres",
            password="Aayau_08"
        )
        return conn
    except Exception as e:
        print("Ошибка подключения к базе:", e)
        exit()