import tkinter as tk
from tkinter import messagebox
from mysql.connector import Error
import mysql.connector

class Spending_Limit_Per_Cat:
    def __init__(self, root, create_db_connection, user_id):
        self.create_db_connection = create_db_connection
        self.user_id = user_id  
        self.setup_spending_limit_per_category_section(root)

    def add_spending_limit_per_category(self):
        category_id = self.category_id_entry.get()
        limit_amount = self.spending_limit_per_category_entry.get()

        try:
            connection = create_db_connection()
            cursor = connection.cursor()
            insert_query = "INSERT INTO SpendingLimitPerCategory (categoryId, user_id, spendinglimitAmountpercategory) VALUES (%s, %s, %s)"
            cursor.execute(insert_query, (category_id, self.user_id, limit_amount))
            connection.commit()
            messagebox.showinfo("Success", "Spending limit per category added successfully")
        except Error as e:
            messagebox.showerror("Error", f"Failed to add spending limit per category: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def update_spending_limit_per_category(self):
        category_id = self.update_category_id_entry.get()
        new_limit_amount = self.update_spending_limit_per_category_entry.get()

        try:
            connection = create_db_connection()
            cursor = connection.cursor()
            update_query = "UPDATE SpendingLimitPerCategory SET spendinglimitAmountpercategory = %s WHERE spendinglimitpercatid = %s AND user_id = %s"
            cursor.execute(update_query, (new_limit_amount, category_id, self.user_id))
            affected_rows = cursor.rowcount  
            if affected_rows == 0:
                messagebox.showwarning("Update Failed", "No spedning limit per category updated. Please check if the record exists and belongs to you.")
            else:
                connection.commit()
                messagebox.showinfo("Success", "Spending limit per category updated successfully")
        except Error as e:
            messagebox.showerror("Error", f"Failed to update spending limit per category: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def delete_spending_limit_per_category(self):
        category_id = self.delete_category_id_entry.get()  
        try:
            connection = create_db_connection()
            cursor = connection.cursor()
            delete_query = "DELETE FROM SpendingLimitPerCategory WHERE spendinglimitpercatid = %s AND user_id = %s"
            cursor.execute(delete_query, (category_id, self.user_id))
            affected_rows = cursor.rowcount  
            if affected_rows == 0:
                messagebox.showwarning("Delete Failed", "No spending limit per category deleted. Please check if the record exists and belongs to you.")
            else:
                connection.commit()
                messagebox.showinfo("Success", "Spending limit per category deleted successfully")
        except Error as e:
            messagebox.showerror("Error", f"Failed to delete spending limit per category: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()


    def setup_spending_limit_per_category_section(self, parent):
        label_frame = tk.LabelFrame(parent, text="Spending Limit Per Category", padx=5, pady=5)
        label_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)

        self.setup_add_spending_limit_per_category_frame(label_frame)
        self.setup_delete_spending_limit_per_category_frame(label_frame)
        self.setup_update_spending_limit_per_category_frame(label_frame)

    def setup_add_spending_limit_per_category_frame(self, parent):
        tk.Label(parent, text="Category ID:").pack(fill='x', expand=True)
        self.category_id_entry = tk.Entry(parent)
        self.category_id_entry.pack(fill='x', expand=True)

        tk.Label(parent, text="Limit Amount:").pack(fill='x', expand=True)
        self.spending_limit_per_category_entry = tk.Entry(parent)
        self.spending_limit_per_category_entry.pack(fill='x', expand=True)

        add_button = tk.Button(parent, text="Add Limit Per Cat.", command=self.add_spending_limit_per_category, bg='green', fg='white')
        add_button.pack(fill='x', expand=True, pady=4)

    def setup_update_spending_limit_per_category_frame(self, parent):
        tk.Label(parent, text="Update - Limit ID:").pack(fill='x', expand=True)
        self.update_category_id_entry = tk.Entry(parent)
        self.update_category_id_entry.pack(fill='x', expand=True)

        tk.Label(parent, text="Update - New Limit Amount:").pack(fill='x', expand=True)
        self.update_spending_limit_per_category_entry = tk.Entry(parent)
        self.update_spending_limit_per_category_entry.pack(fill='x', expand=True)

        update_button = tk.Button(parent, text="Update Limit", command=self.update_spending_limit_per_category)
        update_button.pack(fill='x', expand=True, pady=4)

    def setup_delete_spending_limit_per_category_frame(self, parent):
        tk.Label(parent, text="Delete - Limit ID:").pack(fill='x', expand=True)
        self.delete_category_id_entry = tk.Entry(parent)  # This should be a unique entry for the delete operation
        self.delete_category_id_entry.pack(fill='x', expand=True)

        
        delete_button = tk.Button(parent, text="Delete Limit", command=self.delete_spending_limit_per_category, bg='red', fg='white')
        delete_button.pack(fill='x', expand=True, pady=4)

    def update_for_user(self, user_id):
        self.user_id = user_id 
        self.refresh_data()

    def refresh_data(self):
        if not self.user_id:
            return  
        connection = create_db_connection()
        try:
            cursor = connection.cursor()
            query = "SELECT dateOfIncome, TotalAmountOfIncome FROM Income WHERE user_id = %s"
            cursor.execute(query, (self.user_id,))
        except Exception as e:
            messagebox.showerror("Error", f"Could not fetch income data: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

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