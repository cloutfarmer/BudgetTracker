import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import mysql.connector
from mysql.connector import Error 

class GraphPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.user_id = None  # Initialize with no user_id

        self.top_frame = tk.Frame(self)
        self.top_frame.pack(side='top', fill='x', expand=False)

        self.user_id_label = tk.Label(self.top_frame, text="User ID: Not Set", font=('Helvetica', 12), fg='red')
        self.user_id_label.pack(side='right', padx=10, pady=10)

        tk.Label(self.top_frame, text="Graph Page", font=('Helvetica', 16)).pack(side='top', fill='x', pady=10)
        tk.Button(self.top_frame, text="Go to Edit Page", command=lambda: controller.show_frame("EditPage")).pack(side='left', padx=10, pady=10)
        self.canvas = None

    def set_user_id(self, user_id):
        self.user_id = user_id
        if self.user_id is not None:
            self.user_id_label.config(text=f"User ID: {self.user_id}")
            self.draw_user_financials()

    def update_for_user(self, user_id):
        self.user_id = user_id
        self.user_id_label.config(text=f"User ID: {self.user_id}")
        self.draw_user_financials()

    def draw_user_financials(self):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            
        data = self.fetch_financial_data()
        if not data:
            messagebox.showinfo("No Data", "No financial data found for this user.")
            return
        
        dates = [record[0] for record in data]
        amounts = [record[1] for record in data]
        categories = list(set(record[2] for record in data))

        # Initialize Figure for Matplotlib
        fig = Figure(figsize=(10, 4), dpi=100)

        # Line plot
        ax1 = fig.add_subplot(121)
        ax1.plot(dates, amounts, 'r-')
        ax1.set_title('Financial Line Plot')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Amount')
        ax1.tick_params(axis='x', rotation=45)

        # Bar chart
        category_totals = {category: sum(record[1] for record in data if record[2] == category) for category in categories}
        ax2 = fig.add_subplot(122)
        ax2.bar(category_totals.keys(), category_totals.values(), color='blue')
        ax2.set_title('Expenses by Category')
        ax2.set_xlabel('Category')
        ax2.set_ylabel('Total Amount')
        ax2.tick_params(axis='x', rotation=45)

        fig.tight_layout()
        # Drawing the canvas
        self.canvas = FigureCanvasTkAgg(fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
    def fetch_financial_data(self):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='BudgetTracker',
                user='root',
                password='Database123'
            )
            cursor = connection.cursor()

            # Combine expenses and income in a single result
            query = """
            (SELECT dateOfTransaction AS date, amount, category, 'Expense' AS type FROM expense WHERE user_id = %s)
            UNION ALL
            (SELECT dateOfIncome AS date, TotalAmountOfIncome AS amount, source AS category, 'Income' AS type FROM income WHERE user_id = %s)
            ORDER BY date;
            """
            cursor.execute(query, (self.user_id, self.user_id))
            result = cursor.fetchall()

            return result
        except Error as e:
            messagebox.showerror("Database Error", f"Error fetching data: {e}")
            return []
            