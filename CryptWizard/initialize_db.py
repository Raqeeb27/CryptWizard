import sqlite3

# SQLite database file path
db_file = 'db.sqlite3'

# Create tables and initial data
def create_tables_and_data():
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Create the 'Usernames' table
        cursor.execute("CREATE TABLE IF NOT EXISTS Usernames (id INTEGER PRIMARY KEY, username TEXT NOT NULL)")

        # Create the 'Passwords' table
        cursor.execute("CREATE TABLE IF NOT EXISTS Passwords (id INTEGER PRIMARY KEY, password TEXT NOT NULL)")

        # Insert initial data if needed
        # cursor.execute("INSERT INTO Usernames (username) VALUES (?)", ('user1',))
        # cursor.execute("INSERT INTO Passwords (password) VALUES (?)", ('password1',))

        conn.commit()
        cursor.close()
        conn.close()
        print("SQLite database and tables created successfully.")

    except sqlite3.Error as err:
        print(f"Error: {err}")

if __name__ == '__main__':
    create_tables_and_data()

