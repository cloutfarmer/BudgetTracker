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

class Budget:
    def __init__(self, root, create_db_connection, user_id):
        self.create_db_connection = create_db_connection
        self.user_id = user_id
        self.setup_budget_section(root)

    def add_budget(self):
        amount = self.amount_entry.get()
        category = self.category_entry.get()
        budget_date = self.budget_date_entry.get()

        try:
            connection = create_db_connection()
            cursor = connection.cursor()
            insert_query = """
                INSERT INTO budget (amount, user_id, category, budgetDate)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert_query, (amount, self.user_id, category, budget_date))
            connection.commit()
            messagebox.showinfo("Success", "Budget added successfully")
        except Error as e:
            messagebox.showerror("Error", f"Failed to add budget: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def update_budget(self):
        budget_id = self.update_budget_id_entry.get()
        new_amount = self.update_amount_entry.get()
        new_category = self.update_category_entry.get()
        new_budget_date = self.update_budget_date_entry.get()

        try:
            connection = create_db_connection()
            cursor = connection.cursor()
            update_query = """
                UPDATE budget
                SET amount = %s, category = %s, budgetDate = %s
                WHERE budgetId = %s AND user_id = %s
            """
            cursor.execute(update_query, (new_amount, new_category, new_budget_date, budget_id, self.user_id))
            affected_rows = cursor.rowcount
            if affected_rows == 0:
                messagebox.showwarning("Update Failed", "No budget updated. Please check if the record exists and belongs to you.")
            else:
                connection.commit()
                messagebox.showinfo("Success", "Budget updated successfully")
        except Error as e:
            messagebox.showerror("Error", f"Failed to update budget: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def delete_budget(self):
        budget_id = self.delete_budget_id_entry.get()

        try:
            connection = create_db_connection()
            cursor = connection.cursor()
            delete_query = "DELETE FROM budget WHERE budgetId = %s AND user_id = %s"
            cursor.execute(delete_query, (budget_id, self.user_id))
            affected_rows = cursor.rowcount
            if affected_rows == 0:
                messagebox.showwarning("Delete Failed", "No budget deleted. Please check if the record exists and belongs to you.")
            else:
                connection.commit()
                messagebox.showinfo("Success", "Budget deleted successfully")
        except Error as e:
            messagebox.showerror("Error", f"Failed to delete budget: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def setup_budget_section(self, root):
        budget_label_frame = tk.LabelFrame(root, text="Budget Management", padx=5, pady=5)
        budget_label_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)

        self.setup_add_budget_frame(budget_label_frame)
        self.setup_update_budget_frame(budget_label_frame)
        self.setup_delete_budget_frame(budget_label_frame)

    def setup_add_budget_frame(self, parent):
        tk.Label(parent, text="Amount:").pack(fill='x', expand=True)
        self.amount_entry = tk.Entry(parent)
        self.amount_entry.pack(fill='x', expand=True)

        tk.Label(parent, text="Category:").pack(fill='x', expand=True)
        self.category_entry = tk.Entry(parent)
        self.category_entry.pack(fill='x', expand=True)

        tk.Label(parent, text="Budget Date (YYYY-MM-DD):").pack(fill='x', expand=True)
        self.budget_date_entry = tk.Entry(parent)
        self.budget_date_entry.pack(fill='x', expand=True)

        add_button = tk.Button(parent, text="Add Budget", command=self.add_budget, bg='green', fg='white')
        add_button.pack(fill='x', expand=True, pady=4)

    def setup_update_budget_frame(self, parent):
        tk.Label(parent, text="Budget ID to Update:").pack(fill='x', expand=True)
        self.update_budget_id_entry = tk.Entry(parent)
        self.update_budget_id_entry.pack(fill='x', expand=True)

        tk.Label(parent, text="New Amount:").pack(fill='x', expand=True)
        self.update_amount_entry = tk.Entry(parent)
        self.update_amount_entry.pack(fill='x', expand=True)

        tk.Label(parent, text="New Category:").pack(fill='x', expand=True)
        self.update_category_entry = tk.Entry(parent)
        self.update_category_entry.pack(fill='x', expand=True)

        tk.Label(parent, text="New Budget Date (YYYY-MM-DD):").pack(fill='x', expand=True)
        self.update_budget_date_entry = tk.Entry(parent)
        self.update_budget_date_entry.pack(fill='x', expand=True)

        update_button = tk.Button(parent, text="Update Budget", command=self.update_budget)
        update_button.pack(fill='x', expand=True, pady=4)

    def setup_delete_budget_frame(self, parent):
        tk.Label(parent, text="Budget ID to Delete:").pack(fill='x', expand=True)
        self.delete_budget_id_entry = tk.Entry(parent)
        self.delete_budget_id_entry.pack(fill='x', expand=True)

        delete_button = tk.Button(parent, text="Delete Budget", command=self.delete_budget, bg='red', fg='white')
        delete_button.pack(fill='x', expand=True, pady=4)
