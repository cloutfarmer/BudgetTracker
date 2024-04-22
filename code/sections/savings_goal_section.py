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
        current_amount = self.current_amount_entry.get()
        deadline = self.deadline_entry.get()
        description = self.description_entry.get()

        try:
            connection = create_db_connection()
            cursor = connection.cursor()
            insert_query = "INSERT INTO SavingGoal (goalAmount, current_amount, deadline, description, user_id) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(insert_query, (goal_amount, current_amount, deadline, description, self.user_id))
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
        new_current_amount = self.update_current_amount_entry.get()
        new_deadline = self.update_deadline_entry.get()
        new_description = self.update_description_entry.get()

        try:
            connection = create_db_connection()
            cursor = connection.cursor()
            update_query = "UPDATE SavingGoal SET goalAmount = %s, current_amount = %s, deadline = %s, description = %s WHERE savingGoalId = %s AND user_id = %s"
            cursor.execute(update_query, (new_goal_amount, new_current_amount, new_deadline, new_description, saving_goal_id, self.user_id))
            affected_rows = cursor.rowcount  
            if affected_rows == 0:
                messagebox.showwarning("Update Failed", "No savings goal updated. Please check if the record exists and belongs to you.")
            else:
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
            delete_query = "DELETE FROM SavingGoal WHERE savingGoalId = %s AND user_id = %s"
            cursor.execute(delete_query, (saving_goal_id, self.user_id))
            affected_rows = cursor.rowcount  
            if affected_rows == 0:
                messagebox.showwarning("Delete Failed", "No savings goal deleted. Please check if the record exists and belongs to you.")
            else:
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
        
        tk.Label(parent, text="Current Amount:").pack(fill='x', expand=True)
        self.current_amount_entry = tk.Entry(parent)
        self.current_amount_entry.pack(fill='x', expand=True)

        tk.Label(parent, text="Deadline (YYYY-MM-DD):").pack(fill='x', expand=True)
        self.deadline_entry = tk.Entry(parent)
        self.deadline_entry.pack(fill='x', expand=True)

        tk.Label(parent, text="Description:").pack(fill='x', expand=True)
        self.description_entry = tk.Entry(parent)
        self.description_entry.pack(fill='x', expand=True)

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
        self.saving_goal_id_entry = tk.Entry(parent)
        self.saving_goal_id_entry.pack(fill='x', expand=True)

        tk.Label(parent, text="New Goal Amount:").pack(fill='x', expand=True)
        self.update_goal_amount_entry = tk.Entry(parent)
        self.update_goal_amount_entry.pack(fill='x', expand=True)

        tk.Label(parent, text="New Current Amount:").pack(fill='x', expand=True)
        self.update_current_amount_entry = tk.Entry(parent)
        self.update_current_amount_entry.pack(fill='x', expand=True)

        tk.Label(parent, text="New Deadline (YYYY-MM-DD):").pack(fill='x', expand=True)
        self.update_deadline_entry = tk.Entry(parent)
        self.update_deadline_entry.pack(fill='x', expand=True)

        tk.Label(parent, text="New Description:").pack(fill='x', expand=True)
        self.update_description_entry = tk.Entry(parent)
        self.update_description_entry.pack(fill='x', expand=True)

        update_button = tk.Button(parent, text="Update Savings Goal", command=self.update_saving_goal)
        update_button.pack(fill='x', expand=True, pady=4)

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