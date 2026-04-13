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


def upsert_contact():
    username = input("Enter username: ").strip()
    phone = input("Enter phone: ").strip()

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute(
            "CALL upsert_contact(%s, %s)",
            (username, phone)
        )

        conn.commit()
        print("Contact inserted/updated successfully.")

    except psycopg2.Error as e:
        print("Error:", e)

    finally:
        cur.close()
        conn.close()


def search_pattern():
    pattern = input("Enter search pattern: ").strip()

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM search_contacts(%s)",
        (pattern,)
    )

    rows = cur.fetchall()

    print("\n--- SEARCH RESULTS ---")

    for row in rows:
        print(row)

    cur.close()
    conn.close()


def bulk_insert():
    n = int(input("How many contacts? "))

    usernames = []
    phones = []

    for i in range(n):
        usernames.append(input("Username: "))
        phones.append(input("Phone: "))

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "CALL bulk_insert_contacts(%s, %s)",
        (usernames, phones)
    )

    conn.commit()

    cur.close()
    conn.close()

    print("Bulk insert completed.")


def paginate_contacts():
    limit = int(input("Enter limit: "))
    offset = int(input("Enter offset: "))

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM get_paginated_contacts(%s, %s)",
        (limit, offset)
    )

    rows = cur.fetchall()

    print("\n--- PAGINATED RESULTS ---")

    for row in rows:
        print(row)

    cur.close()
    conn.close()


def delete_contact():
    value = input("Enter username or phone to delete: ").strip()

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "CALL delete_contact(%s)",
        (value,)
    )

    conn.commit()

    print("Deleted successfully.")

    cur.close()
    conn.close()


def main():
    create_table()

    while True:
        print("\n========== PHONEBOOK MENU ==========")
        print("1. Insert/Update Contact")
        print("2. Search by Pattern")
        print("3. Bulk Insert")
        print("4. Pagination View")
        print("5. Delete Contact")
        print("6. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            upsert_contact()

        elif choice == "2":
            search_pattern()

        elif choice == "3":
            bulk_insert()

        elif choice == "4":
            paginate_contacts()

        elif choice == "5":
            delete_contact()

        elif choice == "6":
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()