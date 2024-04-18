import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error

class Savings_Goal_Per_Cat:
    def __init__(self, root, create_db_connection, user_id):
        self.create_db_connection = create_db_connection
        self.user_id = user_id  # Set from EditPage when instantiated
        self.setup_savings_goal_per_category_section(root)

    def add_saving_goal_per_category(self):
        category_id = self.category_id_entry.get()
        saving_amount = self.saving_amount_per_category_entry.get()

        try:
            connection = create_db_connection()
            cursor = connection.cursor()
            insert_query = """
                INSERT INTO SavingGoalPerCategory (savingAmountPerCategory, userId, categoryId) 
                VALUES (%s, %s, %s)
            """
            cursor.execute(insert_query, (saving_amount, self.user_id, category_id))
            connection.commit()
            messagebox.showinfo("Success", "Savings goal per category added successfully")
        except Error as e:
            messagebox.showerror("Error", f"Failed to add savings goal per category: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def delete_saving_goal_per_category(self):
        saving_goal_per_cat_id = self.delete_saving_goal_per_cat_id_entry.get()
        print(saving_goal_per_cat_id)
        try:
            connection = create_db_connection()
            cursor = connection.cursor()
            delete_query = "DELETE FROM SavingGoalPerCategory WHERE savingGoalPerCatId = %s AND userId = %s"
            cursor.execute(delete_query, (saving_goal_per_cat_id, self.user_id))
            connection.commit()
            messagebox.showinfo("Success", "Savings goal per category deleted successfully")
        except Error as e:
            messagebox.showerror("Error", f"Failed to delete savings goal per category: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def update_saving_goal_per_category(self):  
        saving_goal_per_cat_id = self.update_saving_goal_per_cat_id_entry.get()
        new_saving_amount = self.update_saving_amount_per_category_entry.get()
        category_id = self.update_category_id_entry.get()

        try:
            connection = create_db_connection()
            cursor = connection.cursor()
            update_query = """
                UPDATE SavingGoalPerCategory 
                SET savingAmountPerCategory = %s, categoryId = %s
                WHERE savingGoalPerCatId = %s AND userId = %s
            """
            cursor.execute(update_query, (new_saving_amount, category_id, saving_goal_per_cat_id, self.user_id))
            connection.commit()
            messagebox.showinfo("Success", "Savings goal per category updated successfully")
        except Error as e:
            messagebox.showerror("Error", f"Failed to update savings goal per category: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def setup_savings_goal_per_category_section(self, root):
        label_frame = tk.LabelFrame(root, text="Savings Goal Per Category", padx=5, pady=5)
        label_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)

        self.setup_add_savings_goal_per_category_frame(label_frame)
        self.setup_delete_savings_goal_per_category_frame(label_frame)
        self.setup_update_savings_goal_per_category_frame(label_frame)

    def setup_add_savings_goal_per_category_frame(self, parent):
        tk.Label(parent, text="Category ID:").pack(fill='x', expand=True)
        self.category_id_entry = tk.Entry(parent)
        self.category_id_entry.pack(fill='x', expand=True)

        tk.Label(parent, text="Saving Amount Per Category:").pack(fill='x', expand=True)
        self.saving_amount_per_category_entry = tk.Entry(parent)
        self.saving_amount_per_category_entry.pack(fill='x', expand=True)

        add_button = tk.Button(parent, text="Add Savings Goal Per Category", command=self.add_saving_goal_per_category, bg='green', fg='white')
        add_button.pack(fill='x', expand=True, pady=4)

    def setup_delete_savings_goal_per_category_frame(self, parent):
        tk.Label(parent, text="Saving Goal Per Cat ID to Delete:").pack(fill='x', expand=True)
        self.delete_saving_goal_per_cat_id_entry = tk.Entry(parent)
        self.delete_saving_goal_per_cat_id_entry.pack(fill='x', expand=True)

        delete_button = tk.Button(parent, text="Delete Savings Goal Per Category", command=self.delete_saving_goal_per_category, bg='red', fg='white')
        delete_button.pack(fill='x', expand=True, pady=4)

    def setup_update_savings_goal_per_category_frame(self, parent):
        tk.Label(parent, text="Saving Goal Per Cat ID:").pack(fill='x', expand=True)
        self.update_saving_goal_per_cat_id_entry = tk.Entry(parent)
        self.update_saving_goal_per_cat_id_entry.pack(fill='x', expand=True)

        tk.Label(parent, text="New Saving Amount Per Category:").pack(fill='x', expand=True)
        self.update_saving_amount_per_category_entry = tk.Entry(parent)
        self.update_saving_amount_per_category_entry.pack(fill='x', expand=True)

        # Add the missing entry for updating category ID
        tk.Label(parent, text="Category ID:").pack(fill='x', expand=True)
        self.update_category_id_entry = tk.Entry(parent)  # This was missing and is likely the source of your error
        self.update_category_id_entry.pack(fill='x', expand=True)

        update_button = tk.Button(parent, text="Update Savings Goal Per Category", command=self.update_saving_goal_per_category)
        update_button.pack(fill='x', expand=True, pady=4)


    def update_for_user(self, user_id):
        self.user_id = user_id
        # Optionally refresh the data shown in this section
        self.refresh_data()

    def refresh_data(self):
        if not self.user_id:
            return
        connection = create_db_connection()
        try:
            cursor = connection.cursor()
            query = "SELECT categoryId, savingAmountPerCategory FROM SavingGoalPerCategory WHERE userId = %s"
            cursor.execute(query, (self.user_id,))
            data = cursor.fetchall()
            print("Data refreshed for user:", self.user_id)
        except Exception as e:
            messagebox.showerror("Error", f"Could not fetch savings goal per category data: {e}")
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