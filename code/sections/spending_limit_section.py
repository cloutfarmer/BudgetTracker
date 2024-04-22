import tkinter as tk
from tkinter import messagebox
from mysql.connector import Error
import mysql.connector

class Spending_Limit:
    def __init__(self, root, create_db_connection, user_id):
        self.create_db_connection = create_db_connection
        self.user_id = user_id  # Set from EditPage when instantiated
        self.setup_spending_limit_section(root)

    def add_spending_limit(self):
        spending_limit_amount = self.spending_limit_amount_entry.get()

        try:
            connection = create_db_connection()
            cursor = connection.cursor()
            insert_query = "INSERT INTO SpendingLimit (limitAmount, user_id) VALUES (%s, %s)"
            cursor.execute(insert_query, (spending_limit_amount, self.user_id))
            sl_id = cursor.lastrowid  # Retrieve the last insert ID
            connection.commit()
            messagebox.showinfo("Success", f"Spending Limit added successfully. Spending Limit ID: {sl_id}")
        except Error as e:
            messagebox.showerror("Error", f"Failed to add spending limit: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def update_spending_limit(self):
        spending_limit_id = self.spending_limit_id_entry.get()
        new_spending_limit_amount = self.update_spending_limit_amount_entry.get()

        try:
            connection = create_db_connection()
            cursor = connection.cursor()
            update_query = "UPDATE SpendingLimit SET limitAmount = %s WHERE spendinglimitId = %s"
            cursor.execute(update_query, (new_spending_limit_amount, spending_limit_id))
            affected_rows = cursor.rowcount  
            if affected_rows == 0:
                messagebox.showwarning("Update Failed", "No spending limit updated. Please check if the record exists and belongs to you.")
            else:
                connection.commit()
                messagebox.showinfo("Success", "Spending limit updated successfully")
        except Error as e:
            messagebox.showerror("Error", f"Failed to update spending limit: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def delete_spending_limit(self):
        spending_limit_id = self.delete_spending_limit_id_entry.get()
        

        try:
            connection = create_db_connection()
            cursor = connection.cursor()
            
            delete_query = "DELETE FROM SpendingLimit WHERE spendinglimitId = %s AND user_id = %s"
            cursor.execute(delete_query, (spending_limit_id,self.user_id))
            
            affected_rows = cursor.rowcount  
            if affected_rows == 0:
                messagebox.showwarning("Delete Failed", "No spedning limit deleted. Please check if the record exists and belongs to you.")
            else:
                connection.commit()
                messagebox.showinfo("Success", "Spending limit deleted successfully")
        except Error as e:
            messagebox.showerror("Error", f"Failed to delete spending limit: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def setup_spending_limit_section(self, parent):
        label_frame = tk.LabelFrame(parent, text="Spending Limit", padx=5, pady=5)
        label_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)

        self.setup_add_spending_limit_frame(label_frame)
        self.setup_delete_spending_limit_frame(label_frame)
        self.setup_update_spending_limit_frame(label_frame)

    def setup_add_spending_limit_frame(self, parent):

        tk.Label(parent, text="Spending Limit Amount:").pack(fill='x', expand=True)
        self.spending_limit_amount_entry = tk.Entry(parent)
        self.spending_limit_amount_entry.pack(fill='x', expand=True)

        add_button = tk.Button(parent, text="Add Spending Limit", command=self.add_spending_limit, bg='green', fg='white')
        add_button.pack(fill='x', expand=True, pady=4)

    def setup_update_spending_limit_frame(self, parent):
        tk.Label(parent, text="Spending Limit ID:").pack(fill='x', expand=True)
        self.spending_limit_id_entry = tk.Entry(parent)
        self.spending_limit_id_entry.pack(fill='x', expand=True)

        tk.Label(parent, text="New Spending Limit Amount:").pack(fill='x', expand=True)
        self.update_spending_limit_amount_entry = tk.Entry(parent)
        self.update_spending_limit_amount_entry.pack(fill='x', expand=True)

        update_button = tk.Button(parent, text="Update Spending Limit", command=self.update_spending_limit)
        update_button.pack(fill='x', expand=True, pady=4)

    def setup_delete_spending_limit_frame(self, parent):
        tk.Label(parent, text="Spending Limit ID to Delete:").pack(fill='x', expand=True)
        
        self.delete_spending_limit_id_entry = tk.Entry(parent) 
        self.delete_spending_limit_id_entry.pack(fill='x', expand=True)
        
        delete_button = tk.Button(parent, text="Delete Spending Limit", command=self.delete_spending_limit, bg='red', fg='white')
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