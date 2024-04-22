import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error

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

class Expense:
    def __init__(self, root, create_db_connection, user_id):
        self.create_db_connection = create_db_connection
        self.user_id = user_id
        self.setup_expenses_section(root)

    def add_expense(self):
        date_of_transaction = self.expense_date_entry.get()
        amount = float(self.expense_amount_entry.get())
        category = self.expense_category_entry.get()
        description = self.expense_description_entry.get()

        try:
            connection = create_db_connection()
            cursor = connection.cursor()
            insert_query = """
                INSERT INTO expense (dateOfTransaction, amount, user_id, category, description)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (date_of_transaction, amount, self.user_id, category, description))
            expense_id = cursor.lastrowid  # Retrieve the last insert ID
            connection.commit()
            messagebox.showinfo("Success", f"Expense added successfully. Expense ID: {expense_id}")
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
            delete_query = "DELETE FROM expense WHERE TransactionID = %s AND user_id = %s"
            cursor.execute(delete_query, (transaction_id, self.user_id))
            affected_rows = cursor.rowcount
            if affected_rows == 0:
                messagebox.showwarning("Delete Failed", "No expense deleted. Please check if the record exists and belongs to you.")
            else:
                connection.commit()
                messagebox.showinfo("Success", "Expense deleted successfully")
        except Error as e:
            messagebox.showerror("Error", f"Failed to delete expense: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def update_expense(self):
        transaction_id = self.update_transaction_id_entry.get()
        new_date = self.update_date_of_transaction_entry.get()
        new_amount = float(self.update_total_amount_per_id_entry.get())
        new_category = self.update_category_id_entry.get()
        new_description = self.update_description_entry.get()

        try:
            connection = create_db_connection()
            cursor = connection.cursor()
            update_query = """
                UPDATE expense
                SET dateOfTransaction = %s, amount = %s, category = %s, description = %s
                WHERE TransactionID = %s AND user_id = %s
            """
            cursor.execute(update_query, (new_date, new_amount, new_category, new_description, transaction_id, self.user_id))
            affected_rows = cursor.rowcount
            if affected_rows == 0:
                messagebox.showwarning("Update Failed", "No expense updated. Please check if the record exists and belongs to you.")
            else:
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

        tk.Label(parent, text="Amount:").pack(fill='x', expand=True)
        self.expense_amount_entry = tk.Entry(parent)
        self.expense_amount_entry.pack(fill='x', expand=True)

        tk.Label(parent, text="Category:").pack(fill='x', expand=True)
        self.expense_category_entry = tk.Entry(parent)
        self.expense_category_entry.pack(fill='x', expand=True)

        tk.Label(parent, text="Description:").pack(fill='x', expand=True)
        self.expense_description_entry = tk.Entry(parent)
        self.expense_description_entry.pack(fill='x', expand=True)

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

        tk.Label(parent, text="New Amount:").pack(fill='x', expand=True)
        self.update_total_amount_per_id_entry = tk.Entry(parent)
        self.update_total_amount_per_id_entry.pack(fill='x', expand=True)

        tk.Label(parent, text="New Category:").pack(fill='x', expand=True)
        self.update_category_id_entry = tk.Entry(parent)
        self.update_category_id_entry.pack(fill='x', expand=True)

        tk.Label(parent, text="New Description:").pack(fill='x', expand=True)
        self.update_description_entry = tk.Entry(parent)
        self.update_description_entry.pack(fill='x', expand=True)

        update_button = tk.Button(parent, text="Update Expense", command=self.update_expense)
        update_button.pack(fill='x', expand=True, pady=4)
