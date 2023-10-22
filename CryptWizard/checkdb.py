import sqlite3

# Path to your SQLite database file
db_file = 'db.sqlite3'  # Replace with the actual path if needed

# Connect to the SQLite database
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Example: Query data from the Usernames table
cursor.execute("SELECT * FROM Usernames")
usernames = cursor.fetchall()

# Example: Query data from the Passwords table
cursor.execute("SELECT * FROM Passwords")
passwords = cursor.fetchall()

# Display the results
print("Usernames:")
for username in usernames:
    print(username)

print("\nPasswords:")
for password in passwords:
    print(password)

# Close the cursor and the database connection
cursor.close()
conn.close()

