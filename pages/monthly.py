import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
import numpy as np
from tkinter import ttk
from calendar import month_name

def fetch_monthly_spending(user_id, db_connection):
    try:
        cursor = db_connection.cursor()
        query = """
            SELECT YEAR(dateOfTransaction) AS year, MONTH(dateOfTransaction) AS month, category, amount
            FROM expense
            WHERE user_id = 1 -- %s
            ORDER BY year DESC, month DESC, category;
        """                
        cursor.execute(query, (user_id,))
        result = cursor.fetchall()
        cursor.close()
        return result
    except Error as e:
        messagebox.showerror("Database Error", f"Failed to fetch monthly spending: {e}")
        return []

class MonthlySpendingPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.user_id = None

        self.top_frame = tk.Frame(self)
        self.top_frame.pack(side='top', fill='x', expand=False)

        self.user_id_label = tk.Label(self.top_frame, text="User ID: Not Set", font=('Helvetica', 12), fg='red')
        self.user_id_label.pack(side='right', padx=10, pady=10)

        tk.Label(self.top_frame, text="Monthly Spending by Category", font=('Helvetica', 16)).pack(side='top', fill='x', pady=10)
        tk.Button(self.top_frame, text="Go to Edit Page", command=lambda: controller.show_frame("EditPage")).pack(side='left', padx=10, pady=10)

        self.spending_tree = None

        self.update_button = tk.Button(self, text="Update", command=self.update_spending)
        self.update_button.pack(pady=10)

    def update_spending(self):
        user_id = self.user_id
        if user_id:
            db_connection = self.controller.create_db_connection()
            if db_connection:
                spending_data = fetch_monthly_spending(user_id, db_connection)
                self.process_and_display_spending(spending_data)
                db_connection.close()
        else:
            messagebox.showinfo("Not logged in", "Please log in to view spending data")

    def process_and_display_spending(self, spending_data):
        if self.spending_tree:
            self.spending_tree.destroy()  

        data_dict = {}
        categories = set()
        for year, month, category, amount in spending_data:
            key = f"{year}-{month_name[month]}"
            if key not in data_dict:
                data_dict[key] = {}
            if category not in data_dict[key]:
                data_dict[key][category] = 0
            data_dict[key][category] += amount
            categories.add(category)

        categories = sorted(categories)
        columns = ['Month & Year'] + categories + ['Total']
        self.spending_tree = ttk.Treeview(self, columns=columns, show='headings')
        for col in columns:
            self.spending_tree.heading(col, text=col)

        for period, values in data_dict.items():
            row = [period] + [values.get(cat, 0) for cat in categories]
            total = sum(values.values())
            row.append(total)
            self.spending_tree.insert('', 'end', values=row)

        self.spending_tree.pack(fill=tk.BOTH, expand=True)


    def set_user_id(self, user_id):
        self.user_id = user_id
        self.user_id_label.config(text=f"User ID: {self.user_id}")
        self.update_spending()

    def update_for_user(self, user_id):
        self.set_user_id(user_id)
