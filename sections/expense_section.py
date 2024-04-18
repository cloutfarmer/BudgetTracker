import tkinter as tk
from tkinter import messagebox
from mysql.connector import Error
import mysql.connector

import tkinter as tk
from tkinter import messagebox
from mysql.connector import Error

class Expense:
    def __init__(self, root, create_db_connection, user_id):
        self.create_db_connection = create_db_connection
        self.user_id = user_id  # Set from EditPage when instantiated
        self.setup_expenses_section(root)

    def add_expense(self):
        date_of_transaction = self.expense_date_entry.get()
        total_amount = self.expense_amount_entry.get()
        category_id = self.expense_category_id_entry.get()

        try:
            connection = create_db_connection()
            cursor = connection.cursor()
            insert_query = """
                INSERT INTO Expense (dateOfTransaction, totalAmountPerId, userID, categoryId)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert_query, (date_of_transaction, total_amount, self.user_id, category_id))
            connection.commit()
            messagebox.showinfo("Success", "Expense added successfully")
        except Error as e:
            messagebox.showerror("Error", f"Failed to add expense: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def delete_expense(self):
        transaction_id = self.expense_transaction_id_entry.get()

        try:
            connection = create_db_connection()
            cursor = connection.cursor()
            delete_query = "DELETE FROM Expense WHERE TransactionId = %s AND userId = %s"
            cursor.execute(delete_query, (transaction_id, self.user_id))
            connection.commit()
            messagebox.showinfo("Success", "Expense deleted successfully")
        except Error as e:
            messagebox.showerror("Error", f"Failed to delete expense: {e}")
        finally:
            if connection is not None and connection.is_connected():
                cursor.close()
                connection.close()

    def update_expense(self):
        transaction_id = self.update_transaction_id_entry.get()
        new_date = self.update_date_of_transaction_entry.get()
        new_amount = self.update_total_amount_per_id_entry.get()
        category_id = self.update_category_id_entry.get()

        try:
            connection = create_db_connection()
            cursor = connection.cursor()
            update_query = """
                UPDATE Expense
                SET dateOfTransaction = %s, totalAmountPerId = %s, categoryId = %s
                WHERE TransactionId = %s AND userId = %s
            """
            cursor.execute(update_query, (new_date, new_amount, category_id, transaction_id, self.user_id))
            connection.commit()
            messagebox.showinfo("Success", "Expense updated successfully")
        except Error as e:
            messagebox.showerror("Error", f"Failed to update expense: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def setup_expenses_section(self, root):
        expenses_label_frame = tk.LabelFrame(root, text="Expenses", padx=5, pady=5)
        expenses_label_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        self.setup_add_expense_frame(expenses_label_frame)
        self.setup_delete_expense_frame(expenses_label_frame)
        self.setup_update_expense_frame(expenses_label_frame)

    def setup_add_expense_frame(self, parent):
        tk.Label(parent, text="Date of Transaction:").pack(fill='x', expand=True)
        self.expense_date_entry = tk.Entry(parent)
        self.expense_date_entry.pack(fill='x', expand=True)

        tk.Label(parent, text="Total Amount:").pack(fill='x', expand=True)
        self.expense_amount_entry = tk.Entry(parent)
        self.expense_amount_entry.pack(fill='x', expand=True)

        tk.Label(parent, text="Category ID:").pack(fill='x', expand=True)
        self.expense_category_id_entry = tk.Entry(parent)
        self.expense_category_id_entry.pack(fill='x', expand=True)

        add_button = tk.Button(parent, text="Add Expense", command=self.add_expense, bg='green', fg='white')
        add_button.pack(fill='x', expand=True, pady=4)

    def setup_delete_expense_frame(self, parent):
        tk.Label(parent, text="Transaction ID to Delete:").pack(fill='x', expand=True)
        self.expense_transaction_id_entry = tk.Entry(parent)
        self.expense_transaction_id_entry.pack(fill='x', expand=True)

        delete_button = tk.Button(parent, text="Delete Expense", command=self.delete_expense, bg='red', fg='white')
        delete_button.pack(fill='x', expand=True, pady=4)

    def setup_update_expense_frame(self, parent):
        tk.Label(parent, text="Transaction ID:").pack(fill='x', expand=True)
        self.update_transaction_id_entry = tk.Entry(parent)
        self.update_transaction_id_entry.pack(fill='x', expand=True)

        tk.Label(parent, text="New Date of Transaction:").pack(fill='x', expand=True)
        self.update_date_of_transaction_entry = tk.Entry(parent)
        self.update_date_of_transaction_entry.pack(fill='x', expand=True)

        tk.Label(parent, text="New Total Amount:").pack(fill='x', expand=True)
        self.update_total_amount_per_id_entry = tk.Entry(parent)
        self.update_total_amount_per_id_entry.pack(fill='x', expand=True)

        tk.Label(parent, text="Category ID:").pack(fill='x', expand=True)
        self.update_category_id_entry = tk.Entry(parent)
        self.update_category_id_entry.pack(fill='x', expand=True)

        update_button = tk.Button(parent, text="Update Expense", command=self.update_expense)
        update_button.pack(fill='x', expand=True, pady=4)

    def update_for_user(self, user_id):
        self.user_id = user_id  
        self.refresh_data()

    def refresh_data(self):
        if not self.user_id:
            return 
        connection = create_db_connection()
        try:
            cursor = connection.cursor()
            query = "SELECT dateOfTransaction, totalAmountPerId FROM Expense WHERE userId = %s"
            cursor.execute(query, (self.user_id,))
            data = cursor.fetchall()
            print("Data refreshed for user:", self.user_id)
        except Exception as e:
            messagebox.showerror("Error", f"Could not fetch expense data: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()


def test_connection():
    try:
        connection = create_db_connection()
        if connection.is_connected():
            messagebox.showinfo("Connection Test", "Connected to MySQL database")
        connection.close()
    except Error as e:
        messagebox.showerror("Connection Test", f"Error: {e}")

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