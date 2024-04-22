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

class Income:
    def __init__(self, root, create_db_connection, user_id):
        self.create_db_connection = create_db_connection
        self.user_id = user_id  # Set from EditPage when instantiated
        self.setup_income_section(root)
    
    def add_income(self):
        date_of_income = self.date_entry.get()
        total_amount_of_income = self.amount_entry.get()
        source = self.source_entry.get()
        description = self.description_entry.get()
        try:
            connection = create_db_connection()
            cursor = connection.cursor()

            # Adjust the SQL query to include source and description
            insert_query = """
            INSERT INTO Income (user_id, TotalAmountOfIncome, source, dateOfIncome, description)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (self.user_id, total_amount_of_income, source, date_of_income, description))
            connection.commit()
            messagebox.showinfo("Success", "Income added successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add income: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    
    def delete_income(self):
        income_id = self.income_id_entry.get()  # Fetch the Income ID from the entry widget

        try:
            connection = create_db_connection()
            cursor = connection.cursor()

            delete_query = "DELETE FROM Income WHERE IncomeId = %s AND user_id = %s"
            cursor.execute(delete_query, (income_id, self.user_id))
            affected_rows = cursor.rowcount
            if affected_rows == 0:
                messagebox.showwarning("Delete Failed", "No income deleted. Please check if the record exists and belongs to you.")
            else:
                connection.commit()
                messagebox.showinfo("Success", "Income deleted successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete income: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()


    def update_income(self):
        income_id = self.update_income_id_entry.get()
        new_date_of_income = self.update_date_entry.get()
        new_total_amount_of_income = self.update_amount_entry.get()
        new_source = self.update_source_entry.get()
        new_description = self.update_description_entry.get()

        try:
            connection = create_db_connection()
            cursor = connection.cursor()
            update_query = """
            UPDATE Income
            SET dateOfIncome = %s, TotalAmountOfIncome = %s, source = %s, description = %s
            WHERE IncomeId = %s AND user_id = %s
            """
            cursor.execute(update_query, (new_date_of_income, new_total_amount_of_income, new_source, new_description, income_id, self.user_id))
            affected_rows = cursor.rowcount  
            if affected_rows == 0:
                messagebox.showwarning("Update Failed", "No income updated. Please check if the record exists and belongs to you.")
            else:
                connection.commit()
                messagebox.showinfo("Success", "Income updated successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update income: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()


    def setup_income_section(self, root):
        income_label_frame = tk.LabelFrame(root, text="Income", padx=5, pady=5)
        income_label_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)

        self.setup_add_income_frame(income_label_frame)
        self.setup_delete_income_frame(income_label_frame)
        self.setup_update_income_frame(income_label_frame)

    def setup_add_income_frame(self, parent):
        tk.Label(parent, text="Date of Income:").pack(fill='x', expand=True)
        self.date_entry = tk.Entry(parent)
        self.date_entry.pack(fill='x', expand=True)

        tk.Label(parent, text="Total Amount:").pack(fill='x', expand=True)
        self.amount_entry = tk.Entry(parent)
        self.amount_entry.pack(fill='x', expand=True)

        tk.Label(parent, text="Source:").pack(fill='x', expand=True)
        self.source_entry = tk.Entry(parent)
        self.source_entry.pack(fill='x', expand=True)

        tk.Label(parent, text="Description:").pack(fill='x', expand=True)
        self.description_entry = tk.Entry(parent)
        self.description_entry.pack(fill='x', expand=True)

        add_income_button = tk.Button(parent, text="Add Income", command=self.add_income, bg='green', fg='white')
        add_income_button.pack(fill='x', expand=True, pady=4)

    def setup_delete_income_frame(self, parent):
        tk.Label(parent, text="Income ID to Delete:").pack(fill='x', expand=True)
        self.income_id_entry = tk.Entry(parent)
        self.income_id_entry.pack(fill='x', expand=True)
        delete_income_button = tk.Button(parent, text="Delete Income", command=self.delete_income, bg='red', fg='white')
        delete_income_button.pack(fill='x', expand=True, pady=4)

    def setup_update_income_frame(self, parent):
        tk.Label(parent, text="Income ID to Update:").pack(fill='x', expand=True)
        self.update_income_id_entry = tk.Entry(parent)
        self.update_income_id_entry.pack(fill='x', expand=True)
        
        tk.Label(parent, text="New Date of Income:").pack(fill='x', expand=True)
        self.update_date_entry = tk.Entry(parent)
        self.update_date_entry.pack(fill='x', expand=True)

        tk.Label(parent, text="New Total Amount:").pack(fill='x', expand=True)
        self.update_amount_entry = tk.Entry(parent)
        self.update_amount_entry.pack(fill='x', expand=True)

        tk.Label(parent, text="New Source:").pack(fill='x', expand=True)
        self.update_source_entry = tk.Entry(parent)
        self.update_source_entry.pack(fill='x', expand=True)

        tk.Label(parent, text="New Description:").pack(fill='x', expand=True)
        self.update_description_entry = tk.Entry(parent)
        self.update_description_entry.pack(fill='x', expand=True)

        update_income_button = tk.Button(parent, text="Update Income", command=self.update_income)
        update_income_button.pack(fill='x', expand=True, pady=4)

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
            data = cursor.fetchall()
            print("Data refreshed for user:", self.user_id)
        except Exception as e:
            messagebox.showerror("Error", f"Could not fetch income data: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
