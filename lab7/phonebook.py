import csv
import psycopg2
from connect import connect

def create_table():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) NOT NULL,
            phone VARCHAR(20) NOT NULL UNIQUE
        );
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("Table is ready.")


def insert_from_console():
    username = input("Enter username: ").strip()
    phone = input("Enter phone: ").strip()

    if not username or not phone:
        print("Username and phone cannot be empty.")
        return

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO phonebook (username, phone) VALUES (%s, %s)",
            (username, phone)
        )
        conn.commit()
        print("Contact added successfully.")
    except psycopg2.Error as e:
        print("Error:", e)
    finally:
        cur.close()
        conn.close()


def insert_from_csv():
    filename = input("Enter CSV filename: ").strip()

    try:
        with open(filename, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            conn = connect()
            cur = conn.cursor()

            for row in reader:
                username = row['username']
                phone = row['phone']

                cur.execute(
                    """
                    INSERT INTO phonebook (username, phone)
                    VALUES (%s, %s)
                    ON CONFLICT (phone) DO NOTHING
                    """,
                    (username, phone)
                )

            conn.commit()
            cur.close()
            conn.close()

            print("CSV data imported successfully.")

    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print("Error reading CSV:", e)


def view_all_contacts():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM phonebook ORDER BY id")
    rows = cur.fetchall()

    print("\n--- ALL CONTACTS ---")
    if rows:
        for row in rows:
            print(f"ID: {row[0]}, Username: {row[1]}, Phone: {row[2]}")
    else:
        print("No contacts found.")

    cur.close()
    conn.close()


def query_contacts():
    print("\nFilter options:")
    print("1. Search by exact username")
    print("2. Search by exact phone")
    print("3. Search by part of username")
    print("4. Search by part of phone")

    choice = input("Choose filter: ").strip()

    conn = connect()
    cur = conn.cursor()

    if choice == "1":
        username = input("Enter exact username: ").strip()
        cur.execute("SELECT * FROM phonebook WHERE username = %s", (username,))

    elif choice == "2":
        phone = input("Enter exact phone: ").strip()
        cur.execute("SELECT * FROM phonebook WHERE phone = %s", (phone,))

    elif choice == "3":
        username = input("Enter part of username: ").strip()
        cur.execute("SELECT * FROM phonebook WHERE username ILIKE %s", (f"%{username}%",))

    elif choice == "4":
        phone = input("Enter part of phone: ").strip()
        cur.execute("SELECT * FROM phonebook WHERE phone ILIKE %s", (f"%{phone}%",))

    else:
        print("Invalid choice.")
        cur.close()
        conn.close()
        return

    rows = cur.fetchall()

    print("\n--- QUERY RESULTS ---")
    if rows:
        for row in rows:
            print(f"ID: {row[0]}, Username: {row[1]}, Phone: {row[2]}")
    else:
        print("No contacts found.")

    cur.close()
    conn.close()

def update_contact():
    username = input("Enter username of contact to update: ").strip()

    print("What do you want to update?")
    print("1. Username")
    print("2. Phone")
    print("3. Both")

    choice = input("Choose option: ").strip()

    conn = connect()
    cur = conn.cursor()

    try:
        if choice == "1":
            new_username = input("Enter new username: ").strip()
            cur.execute(
                "UPDATE phonebook SET username = %s WHERE username = %s",
                (new_username, username)
            )

        elif choice == "2":
            new_phone = input("Enter new phone: ").strip()
            cur.execute(
                "UPDATE phonebook SET phone = %s WHERE username = %s",
                (new_phone, username)
            )

        elif choice == "3":
            new_username = input("Enter new username: ").strip()
            new_phone = input("Enter new phone: ").strip()
            cur.execute(
                "UPDATE phonebook SET username = %s, phone = %s WHERE username = %s",
                (new_username, new_phone, username)
            )

        else:
            print("Invalid choice.")
            cur.close()
            conn.close()
            return

        conn.commit()

        if cur.rowcount > 0:
            print("Contact updated successfully.")
        else:
            print("Contact not found.")

    except psycopg2.Error as e:
        print("Error:", e)
    finally:
        cur.close()
        conn.close()


def delete_contact():
    print("Delete by:")
    print("1. Username")
    print("2. Phone")

    choice = input("Choose option: ").strip()

    conn = connect()
    cur = conn.cursor()

    if choice == "1":
        username = input("Enter username to delete: ").strip()
        cur.execute("DELETE FROM phonebook WHERE username = %s", (username,))

    elif choice == "2":
        phone = input("Enter phone to delete: ").strip()
        cur.execute("DELETE FROM phonebook WHERE phone = %s", (phone,))

    else:
        print("Invalid choice.")
        cur.close()
        conn.close()
        return

    conn.commit()

    if cur.rowcount > 0:
        print("Contact deleted successfully.")
    else:
        print("Contact not found.")

    cur.close()
    conn.close()

def main():
    create_table()

    while True:
        print("\n========== PHONEBOOK MENU ==========")
        print("1. Insert contact from console")
        print("2. Import contacts from CSV")
        print("3. View all contacts")
        print("4. Query contacts with filters")
        print("5. Update contact")
        print("6. Delete contact")
        print("7. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            insert_from_console()
        elif choice == "2":
            insert_from_csv()
        elif choice == "3":
            view_all_contacts()
        elif choice == "4":
            query_contacts()
        elif choice == "5":
            update_contact()
        elif choice == "6":
            delete_contact()
        elif choice == "7":
            print("Exiting PhoneBook...")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()