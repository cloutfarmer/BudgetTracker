import tkinter as tk
from tkinter import messagebox
from mysql.connector import Error
import mysql.connector

class Savings_Goal:
    def __init__(self, root, create_db_connection, user_id):
        self.create_db_connection = create_db_connection
        self.user_id = user_id  # Set from EditPage when instantiated
        self.setup_savings_goal_section(root)

    def add_saving_goal(self):
        goal_amount = self.goal_amount_entry.get()

        try:
            connection = create_db_connection()
            cursor = connection.cursor()
            insert_query = "INSERT INTO SavingGoal (goalAmount, userId) VALUES (%s, %s)"
            cursor.execute(insert_query, (goal_amount, self.user_id))
            connection.commit()
            messagebox.showinfo("Success", "Savings goal added successfully")
        except Error as e:
            messagebox.showerror("Error", f"Failed to add savings goal: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def update_saving_goal(self):
        saving_goal_id = self.saving_goal_id_entry.get()
        new_goal_amount = self.update_goal_amount_entry.get()

        try:
            connection = create_db_connection()
            cursor = connection.cursor()
            update_query = "UPDATE SavingGoal SET goalAmount = %s WHERE savingGoalId = %s AND userId = %s"
            cursor.execute(update_query, (new_goal_amount, saving_goal_id, self.user_id))
            connection.commit()
            messagebox.showinfo("Success", "Savings goal updated successfully")
        except Error as e:
            messagebox.showerror("Error", f"Failed to update savings goal: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def delete_saving_goal(self):
        saving_goal_id = self.delete_saving_goal_id_entry.get()

        try:
            connection = create_db_connection()
            cursor = connection.cursor()
            delete_query = "DELETE FROM SavingGoal WHERE savingGoalId = %s AND userId = %s"
            cursor.execute(delete_query, (saving_goal_id, self.user_id))
            connection.commit()
            messagebox.showinfo("Success", "Savings goal deleted successfully")
        except Error as e:
            messagebox.showerror("Error", f"Failed to delete savings goal: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def setup_savings_goal_section(self, root):
        savings_goal_label_frame = tk.LabelFrame(root, text="Savings Goal", padx=5, pady=5)
        savings_goal_label_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)

        self.setup_add_savings_goal_frame(savings_goal_label_frame)
        self.setup_delete_savings_goal_frame(savings_goal_label_frame)
        self.setup_update_savings_goal_frame(savings_goal_label_frame)

    def setup_add_savings_goal_frame(self, parent):

        tk.Label(parent, text="Goal Amount:").pack(fill='x', expand=True)
        self.goal_amount_entry = tk.Entry(parent)
        self.goal_amount_entry.pack(fill='x', expand=True)

        add_button = tk.Button(parent, text="Add Savings Goal", command=self.add_saving_goal, bg='green', fg='white')
        add_button.pack(fill='x', expand=True, pady=4)

    def setup_delete_savings_goal_frame(self, parent):
        tk.Label(parent, text="Savings Goal ID to Delete:").pack(fill='x', expand=True)
        self.delete_saving_goal_id_entry = tk.Entry(parent)
        self.delete_saving_goal_id_entry.pack(fill='x', expand=True)

        delete_button = tk.Button(parent, text="Delete Savings Goal", command=self.delete_saving_goal, bg='red', fg='white')
        delete_button.pack(fill='x', expand=True, pady=4)

    def setup_update_savings_goal_frame(self, parent):
        tk.Label(parent, text="Savings Goal ID:").pack(fill='x', expand=True)
        self.saving_goal_id_entry = tk.Entry(parent)  # Note: This overwrites the delete frame's saving_goal_id_entry
        self.saving_goal_id_entry.pack(fill='x', expand=True)

        tk.Label(parent, text="New Goal Amount:").pack(fill='x', expand=True)
        self.update_goal_amount_entry = tk.Entry(parent)
        self.update_goal_amount_entry.pack(fill='x', expand=True)

        update_button = tk.Button(parent, text="Update Savings Goal", command=self.update_saving_goal)
        update_button.pack(fill='x', expand=True, pady=4)

    def update_for_user(self, user_id):
        self.user_id = user_id  # Update the internal user_id
        # Optionally refresh the data shown in this section
        self.refresh_data()

    def refresh_data(self):
        # This method should clear existing data and fetch new data based on self.user_id
        if not self.user_id:
            return  # Do nothing if user_id is not set
        connection = create_db_connection()
        try:
            cursor = connection.cursor()
            query = "SELECT dateOfIncome, TotalAmountOfIncome FROM Income WHERE userId = %s"
            cursor.execute(query, (self.user_id,))
            data = cursor.fetchall()
            # Update your UI components with this data
            print("Data refreshed for user:", self.user_id)
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