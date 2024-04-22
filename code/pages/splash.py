import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from mysql.connector import Error
import bcrypt

def create_db_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='BudgetTracker',
            user='root',
            password='Database123'
        )
    except Error as e:
        messagebox.showerror("Error", f"Failed to connect to the database: {e}")
    return connection

class SplashPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Login Section
        login_frame = tk.LabelFrame(self, text="Login", padx=5, pady=5)
        login_frame.pack(padx=10, pady=10, fill="x")

        tk.Label(login_frame, text="Username:").pack()
        self.username_entry = tk.Entry(login_frame)
        self.username_entry.pack()

        tk.Label(login_frame, text="Password:").pack()
        self.password_entry = tk.Entry(login_frame, show="*")
        self.password_entry.pack()

        tk.Button(login_frame, text="Login", command=self.login_user).pack(pady=10)

        # Account Creation Section
        create_account_frame = tk.LabelFrame(self, text="Create Account", padx=5, pady=5)
        create_account_frame.pack(padx=10, pady=10, fill="x")

        tk.Label(create_account_frame, text="New Username:").pack()
        self.new_username_entry = tk.Entry(create_account_frame)
        self.new_username_entry.pack()

        tk.Label(create_account_frame, text="New Password:").pack()
        self.new_password_entry = tk.Entry(create_account_frame, show="*")
        self.new_password_entry.pack()

        tk.Label(create_account_frame, text="Role:").pack()
        self.role_combobox = ttk.Combobox(create_account_frame, values=["admin", "buisness owner", "analyst", "user"])
        self.role_combobox.pack()

        tk.Button(create_account_frame, text="Create Account", command=self.create_account).pack(pady=10)

    def login_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get().encode('utf-8')
        connection = create_db_connection()
        cursor = connection.cursor()
        query = "SELECT user_id, hashed_password FROM UserInfo WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()

        if result:
            user_id, hashed_password = result
            if bcrypt.checkpw(password, hashed_password.encode('utf-8')):
                messagebox.showinfo("Login successful", "You have logged in successfully")
                self.controller.user_id = user_id 
                self.controller.show_frame("EditPage")  
            else:
                messagebox.showerror("Login failed", "Incorrect username or password")
        else:
            messagebox.showerror("Login failed", "Incorrect username or password")

        cursor.close()
        connection.close()

    def create_account(self):
        new_username = self.new_username_entry.get()
        new_password = self.new_password_entry.get().encode('utf-8')
        selected_role = self.role_combobox.get().strip()  # Trim any whitespace

        # Normalize the input to match database ENUM values
        role_map = {
            "admin": "admin",
            "analyst": "analyst",
            "business owner": "businessOwner",  # Correct the label if necessary in Combobox
            "user": "user"
        }
        normalized_role = role_map.get(selected_role.lower())  # Ensure the Combobox value maps correctly

        if not normalized_role:
            messagebox.showerror("Error", "Invalid role selected. Please select a valid role.")
            return

        connection = create_db_connection()
        cursor = connection.cursor()

        # Check if username already exists
        cursor.execute("SELECT * FROM UserInfo WHERE username = %s", (new_username,))
        if cursor.fetchone():
            messagebox.showerror("Error", "Username already exists. Please choose a different username.")
            return

        hashed_password = bcrypt.hashpw(new_password, bcrypt.gensalt())

        query = "INSERT INTO UserInfo (username, hashed_password, role) VALUES (%s, %s, %s)"
        try:
            cursor.execute(query, (new_username, hashed_password.decode('utf-8'), normalized_role))
            connection.commit()
            messagebox.showinfo("Account created", "Your account has been created successfully")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to create account: {err}")
        finally:
            cursor.close()
            connection.close()


