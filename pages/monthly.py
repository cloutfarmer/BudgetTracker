import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
from sections.income_section import Income
from sections.expense_section import Expense
from sections.savings_goal_section import Savings_Goal
from sections.savings_goal_per_cat_section import Savings_Goal_Per_Cat
from sections.spending_limit_section import Spending_Limit
from sections.spending_limit_per_cat_section import Spending_Limit_Per_Cat

import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

def fetch_monthly_spending(user_id, db_connection):
    try:
        cursor = db_connection.cursor()
        query = """
            SELECT YEAR(dateOfTransaction) AS year, MONTH(dateOfTransaction) AS month, SUM(amount) AS total
            FROM expense
            WHERE user_id = %s
            GROUP BY YEAR(dateOfTransaction), MONTH(dateOfTransaction)
            ORDER BY year, month DESC;
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
        '''
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.label = tk.Label(self, text="Monthly Spending")
        self.label.pack(pady=10, padx=10)
        
        self.spending_listbox = tk.Listbox(self)
        self.spending_listbox.pack(fill=tk.BOTH, expand=True)

        self.update_button = tk.Button(self, text="Update", command=lambda: self.update_spending())

        self.update_button.pack()
        '''

        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.user_id = None

        self.top_frame = tk.Frame(self)
        self.top_frame.pack(side='top', fill='x', expand=False)

        self.user_id_label = tk.Label(self.top_frame, text="User ID: Not Set", font=('Helvetica', 12), fg='red')
        self.user_id_label.pack(side='right', padx=10, pady=10)

        tk.Label(self.top_frame, text="Monthly Spending", font=('Helvetica', 16)).pack(side='top', fill='x', pady=10)
        tk.Button(self.top_frame, text="Go to Edit Page", command=lambda: controller.show_frame("EditPage")).pack(side='left', padx=10, pady=10)

        self.spending_listbox = tk.Listbox(self)
        self.spending_listbox.pack(fill=tk.BOTH, expand=True)

        self.update_button = tk.Button(self, text="Update", command=self.update_spending)
        self.update_button.pack()


    def update_spending(self):
        user_id = self.user_id
        if user_id:
            db_connection = self.controller.create_db_connection()
            if db_connection:
                spending_data = fetch_monthly_spending(user_id, db_connection)
                self.spending_listbox.delete(0, tk.END)
                for year, month, total in spending_data:
                    self.spending_listbox.insert(tk.END, f"{year}-{month}: ${total}")
                db_connection.close()
        else:
            messagebox.showinfo("Not logged in", "Please log in to view spending data")

    def set_user_id(self, user_id):
        self.user_id = user_id
        self.user_id_label.config(text=f"User ID: {self.user_id}")
        self.update_spending()

    def update_for_user(self, user_id):
        self.set_user_id(user_id)
