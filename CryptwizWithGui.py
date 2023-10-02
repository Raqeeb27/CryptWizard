import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
import bcrypt

class PasswordManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CryptWizard V1.0")
        self.root.geometry("400x300")

        self.db_connection = self.connect_to_database()

        self.create_widgets()

    def connect_to_database(self):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="asdf",
                database="passwordmanager"
            )
            if connection.is_connected():
                return connection
        except Error as e:
            print("\nError connecting to the database:", e)
        return None

    def create_widgets(self):
        self.label = tk.Label(self.root, text="Crypt Wizard", font=("Helvetica", 16))
        self.label.pack(pady=20)

        self.register_button = tk.Button(self.root, text="Register", command=self.register_user)
        self.register_button.pack()

        self.login_button = tk.Button(self.root, text="Login", command=self.user_login)
        self.login_button.pack()

        # self.view_users_button = tk.Button(self.root, text="List of Users", command=self.view_users)
        # self.view_users_button.pack()

        self.exit_button = tk.Button(self.root, text="Exit", command=self.root.quit)
        self.exit_button.pack()

    def register_user(self):
        self.register_window = tk.Toplevel(self.root)
        self.register_window.title("Register")
        self.register_window.geometry("300x200")

        self.register_label = tk.Label(self.register_window, text="Register", font=("Helvetica", 16))
        self.register_label.pack(pady=10)

        self.username_label = tk.Label(self.register_window, text="Username:")
        self.username_label.pack()

        self.username_entry = tk.Entry(self.register_window)
        self.username_entry.pack()

        self.password_label = tk.Label(self.register_window, text="Password:")
        self.password_label.pack()

        self.password_entry = tk.Entry(self.register_window, show="*")
        self.password_entry.pack()

        self.register_button = tk.Button(self.register_window, text="Register", command=self.add_user)
        self.register_button.pack(pady=10)

    def add_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode(), salt)

        try:
            cursor = self.db_connection.cursor()
            query = "INSERT INTO Users (username, salt, master_key) VALUES (%s, %s, %s)"
            cursor.execute(query, (username, salt.decode(), hashed_password.decode()))
            self.db_connection.commit()
            messagebox.showinfo("Success", "User registered successfully!")
            self.register_window.destroy()
        except Error as e:
            messagebox.showerror("Error", f"Registration failed: {e}")



    def user_login(self):
        self.login_window = tk.Toplevel(self.root)
        self.login_window.title("Login")
        self.login_window.geometry("300x250")

        self.login_label = tk.Label(self.login_window, text="Login", font=("Helvetica", 16))
        self.login_label.pack(pady=10)

        self.username_label = tk.Label(self.login_window, text="Username:")
        self.username_label.pack()

        self.username_entry = tk.Entry(self.login_window)
        self.username_entry.pack()

        self.password_label = tk.Label(self.login_window, text="Password:")
        self.password_label.pack()

        self.password_entry = tk.Entry(self.login_window, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(self.login_window, text="Login", command=self.authenticate_user)
        self.login_button.pack(pady=10)



    def authenticate_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            cursor = self.db_connection.cursor()
            query = "SELECT id, salt, master_key FROM Users WHERE username = %s"
            cursor.execute(query, (username, ))
            result = cursor.fetchone()

            if result:
                user_id, salt, stored_master_key = result
                user_master_key = bcrypt.hashpw(password.encode(), salt.encode())

                if user_master_key == stored_master_key.encode():
                    messagebox.showinfo("Success", "Login successful!")
                    self.login_window.destroy()
                    self.show_passwords(user_id)
                else:
                    messagebox.showerror("Error", "Authentication failed. Incorrect username or password.")
            else:
                messagebox.showerror("Error", "Authentication failed. User not found.")
        except Error as e:
            messagebox.showerror("Error", f"Login failed: {e}")

    def show_passwords(self, user_id):
        # Implement the logic to display and manage passwords here
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManagerApp(root)
    root.mainloop()
