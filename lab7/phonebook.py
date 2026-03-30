import csv
from connect import get_connection


def create_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id    SERIAL PRIMARY KEY,
            name  VARCHAR(100) NOT NULL,
            phone VARCHAR(20)  NOT NULL
        )
    """)
    conn.commit()
    cur.close()
    conn.close()


def add_contact():
    name = input("Введите имя: ").strip()
    phone = input("Введите телефон: ").strip()

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
        (name, phone)
    )
    conn.commit()
    cur.close()
    conn.close()
    print("Контакт добавлен!")


def import_csv():
    filename = input("Введите путь к CSV файлу: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    try:
        with open(filename, newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            count = 0
            for row in reader:
                if len(row) < 2:
                    continue
                cur.execute(
                    "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
                    (row[0].strip(), row[1].strip())
                )
                count += 1
        conn.commit()
        print(f"Импортировано {count} контакт(ов)!")

    except FileNotFoundError:
        print("Файл не найден.")
    except Exception as e:
        conn.rollback()
        print("Ошибка:", e)
    finally:
        cur.close()
        conn.close()


def show_contacts():
    print("\nФильтр:")
    print("  1. Показать всех")
    print("  2. Поиск по имени")
    print("  3. Поиск по префиксу телефона")
    choice = input("Выбор: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    if choice == "2":
        name = input("Введите имя (или часть): ").strip()
        cur.execute(
            "SELECT id, name, phone FROM phonebook WHERE name ILIKE %s ORDER BY name",
            (f"%{name}%",)
        )
    elif choice == "3":
        prefix = input("Введите префикс телефона: ").strip()
        cur.execute(
            "SELECT id, name, phone FROM phonebook WHERE phone LIKE %s ORDER BY name",
            (f"{prefix}%",)
        )
    else:
        cur.execute("SELECT id, name, phone FROM phonebook ORDER BY name")

    rows = cur.fetchall()
    cur.close()
    conn.close()

    if not rows:
        print("Контакты не найдены.")
    else:
        print(f"\n{'ID':<5} {'Имя':<20} {'Телефон'}")
        print("-" * 40)
        for row in rows:
            print(f"{row[0]:<5} {row[1]:<20} {row[2]}")


def update_contact():
    print("\nОбновить по:")
    print("  1. Имени")
    print("  2. Телефону")
    choice = input("Выбор: ").strip()

    conn = get_connection()
    cur = conn.cursor()
