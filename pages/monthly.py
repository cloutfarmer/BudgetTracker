import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
import numpy as np
from tkinter import ttk
from calendar import month_name

class MonthlySpendingPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.user_id = None
        self.spending_tree = None
        self.setup_ui()

    def setup_ui(self):
        self.top_frame = tk.Frame(self)
        self.top_frame.pack(side='top', fill='x', expand=False)
        self.user_id_label = tk.Label(self.top_frame, text="User ID: Not Set", font=('Helvetica', 12), fg='red')
        self.user_id_label.pack(side='right', padx=10, pady=10)
        tk.Label(self.top_frame, text="Monthly Spending by Category", font=('Helvetica', 16)).pack(side='top', fill='x', pady=10)
        tk.Button(self.top_frame, text="Go to Edit Page", command=lambda: self.controller.show_frame("EditPage")).pack(side='left', padx=10, pady=10)
        self.update_button = tk.Button(self, text="Update", command=self.update_spending)
        self.update_button.pack(pady=10)

    def show_monthly_spending(self):
        self.controller.show_frame("MonthlySpendingPage")
        
    def update_spending(self):
        if self.user_id:
            db_connection = self.controller.create_db_connection()
            if db_connection:
                user_role = self.get_user_role(self.user_id, db_connection)
                spending_data = self.get_monthly_spending(self.user_id, db_connection, user_role)
                self.process_and_display_spending(spending_data, user_role)
                db_connection.close()
        else:
            messagebox.showinfo("Not logged in", "Please log in to view spending data")

    def get_user_role(self, user_id, db_connection):
        cursor = db_connection.cursor()
        cursor.execute("SELECT role FROM userinfo WHERE user_id = %s", (user_id,))
        role = cursor.fetchone()[0]
        cursor.close()
        return role

    def update_for_user(self, user_id):        
        self.user_id = user_id
        self.user_id_label.config(text=f"User ID: {self.user_id}")
        self.update_spending()
        self.show_monthly_spending()

    def get_monthly_spending(self, user_id, db_connection, role):
        cursor = db_connection.cursor()
        monthly_data = {}

        # Users
        query_expenses = """
            SELECT YEAR(dateOfTransaction) AS year, MONTH(dateOfTransaction) AS month, category, SUM(amount) AS amount 
            FROM expense
            WHERE user_id = 1 -- %s
            GROUP BY YEAR(dateOfTransaction), MONTH(dateOfTransaction), category
            ORDER BY year DESC, month DESC, category;
        """
        cursor.execute(query_expenses, (user_id,))
        expenses = cursor.fetchall()

        for year, month, category, amount in expenses:
            key = f"{year}-{month_name[month]}"
            if key not in monthly_data:
                monthly_data[key] = {'expenses': {}, 'income': 0, 'profit': 0, 'budgets': {}}
            monthly_data[key]['expenses'][category] = amount

        # Business owners
        if role == 'businessOwner':
            #print("businessOwner")
            query_income = """
                SELECT YEAR(dateOfIncome) AS year, MONTH(dateOfIncome) AS month, SUM(TotalAmountOfIncome) AS income
                FROM income
                WHERE user_id = 4 -- %s
                GROUP BY YEAR(dateOfIncome), MONTH(dateOfIncome)
                ORDER BY year DESC, month DESC;
            """
            cursor.execute(query_income, (user_id,))
            incomes = cursor.fetchall()
            for year, month, income in incomes:
                key = f"{year}-{month_name[month]}"
                monthly_data[key]['income'] = income
                monthly_data[key]['profit'] = income - sum(monthly_data[key]['expenses'].values())

        # Admins and analysts
        if role in ['admin', 'analyst']:
            #print("admin, analyst")
            query_budgets = """
                SELECT YEAR(budgetDate) AS year, MONTH(budgetDate) AS month, category, SUM(amount) AS amount
                FROM budget
                WHERE user_id = 2 -- %s
                GROUP BY YEAR(budgetDate), MONTH(budgetDate), category
                ORDER BY year DESC, month DESC, category;
            """
            cursor.execute(query_budgets, (user_id,))
            budgets = cursor.fetchall()

            for year, month, category, amount in budgets:
                key = f"{year}-{month_name[month]}"
                if key not in monthly_data:
                    monthly_data[key] = {'expenses': {}, 'income': 0, 'profit': 0, 'budgets': {}}
                monthly_data[key]['budgets'][category] = amount

        cursor.close()
        return monthly_data

    def process_and_display_spending(self, monthly_data, role):
        if self.spending_tree:
            self.spending_tree.destroy()
        categories = set()
        for data in monthly_data.values():
            categories.update(data['expenses'].keys())
            if role in ['admin', 'analyst']:
                categories.update(data['budgets'].keys())

        categories = sorted(categories)

        columns = ['Month & Year'] + [f"{cat} Expense" for cat in categories] + ['Total Expenses']
        if role == 'businessOwner':
            columns += ['Total Income', 'Profit']
        if role in ['admin', 'analyst']:
            columns += [f"{cat} Budget" for cat in categories]

        self.spending_tree = ttk.Treeview(self, columns=columns, show='headings')
        for col in columns:
            self.spending_tree.heading(col, text=col)
            self.spending_tree.column(col, anchor='center')

        for period, data in sorted(monthly_data.items()):
            row = [period]
            total_expenses = 0
            for category in categories:
                expense = data['expenses'].get(category, 0)
                total_expenses += expense
                row.append(expense)
                if role in ['admin', 'analyst']:
                    row.append(data['budgets'].get(category, 0))
            row.append(total_expenses)
            if role == 'businessOwner':
                row += [data['income'], data['profit']]

            self.spending_tree.insert('', 'end', values=row)

        self.spending_tree.pack(fill=tk.BOTH, expand=True)


'''
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
        if self.user_id:
            db_connection = self.controller.create_db_connection()
            if db_connection:                    
                user_role = self.get_user_role(self.user_id, db_connection)
                spending_data = self.get_monthly_spending(self.user_id, db_connection, user_role)
                self.process_and_display_spending(spending_data, user_role)
                db_connection.close()
        else:
            messagebox.showinfo("Not logged in", "Please log in to view spending data")

    ' ''
    def process_and_display_spending(self, monthly_data, role):
        if self.spending_tree:
            self.spending_tree.destroy()
        columns = ['Month & Year', 'Total Expenses']
        if role == 'businessOwner':
            columns += ['Total Income', 'Profit']

        self.spending_tree = ttk.Treeview(self, columns=columns, show='headings')
        for col in columns:
            self.spending_tree.heading(col, text=col)
        for period, data in monthly_data.items():
            if role == 'businessOwner':
                row = [period, sum(data['expenses'].values()), data['income'], data['profit']]
            else:
                row = [period, sum(data['expenses'].values())]
            self.spending_tree.insert('', 'end', values=row)
        self.spending_tree.pack(fill=tk.BOTH, expand=True)
    ' ''
    ' ''
    def process_and_display_spending(self, monthly_data, role):
        if self.spending_tree:
            self.spending_tree.destroy()

        categories = set()
        for data in monthly_data.values():
            categories.update(data['expenses'].keys())
        categories = sorted(categories) 

        columns = ['Month & Year'] + categories + ['Total Expenses']
        self.spending_tree = ttk.Treeview(self, columns=columns, show='headings')
        
        for col in columns:
            self.spending_tree.heading(col, text=col)
            self.spending_tree.column(col, anchor='center')

        for period, data in sorted(monthly_data.items()):
            row = [period]
            total_expenses = 0
            for category in categories:
                expense = data['expenses'].get(category, 0)
                total_expenses += expense
                row.append(expense)
            row.append(total_expenses)

            self.spending_tree.insert('', 'end', values=row)

        self.spending_tree.pack(fill=tk.BOTH, expand=True)
    ' ''
    def process_and_display_spending(self, monthly_data, role):
        role = 'user'
        if self.spending_tree:
            self.spending_tree.destroy()

        categories = set()

        #######
        if role == 'user':
            data_dict = {}
            for year, month, category, amount in monthly_data:
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
        #######

        for data in monthly_data.values():
            categories.update(data['expenses'].keys())
            if role in ['admin', 'analyst']:
                categories.update(data['budgets'].keys())
        categories = sorted(categories)

        columns = ['Month & Year'] + [f"{cat} Expense" for cat in categories]
        if role in ['admin', 'analyst']:
            columns += [f"{cat} Budget" for cat in categories]
        if role == 'businessOwner':
            columns += ['Total Income', 'Profit']
        columns += ['Total Expenses']
        
        self.spending_tree = ttk.Treeview(self, columns=columns, show='headings')
        
        for col in columns:
            self.spending_tree.heading(col, text=col)
            self.spending_tree.column(col, anchor='center')

        for period, data in sorted(monthly_data.items()):
            row = [period]
            total_expenses = 0
            for category in categories:
                expense = data['expenses'].get(category, 0)
                total_expenses += expense
                row.append(expense)
                if role in ['admin', 'analyst']:
                    budget = data['budgets'].get(category, 0)
                    row.append(budget)
            if role == 'businessOwner':
                row += [data['income'], data['profit']]
            row.append(total_expenses)

            self.spending_tree.insert('', 'end', values=row)

        self.spending_tree.pack(fill=tk.BOTH, expand=True)

    def get_user_role(self, user_id, db_connection):
        cursor = db_connection.cursor()
        cursor.execute("SELECT role FROM userinfo WHERE user_id = %s", (user_id,))
        role = cursor.fetchone()[0]
        cursor.close()
        return role

    def get_monthly_spending(self, user_id, db_connection, role):
        cursor = db_connection.cursor()
        monthly_data = {}
        role = 'user'
        # Business Owner
        if role == 'businessOwner':
            query_income = """
                SELECT YEAR(dateOfIncome) AS year, MONTH(dateOfIncome) AS month, SUM(TotalAmountOfIncome) AS income
                FROM income
                WHERE user_id = 4 -- %s
                GROUP BY YEAR(dateOfIncome), MONTH(dateOfIncome)
                ORDER BY year DESC, month DESC;
            """
            cursor.execute(query_income, (user_id,))
            incomes = cursor.fetchall()
            for year, month, income in incomes:
                key = f"{year}-{month_name[month]}"
                if key in monthly_data:
                    monthly_data[key]['income'] = income
                    total_expenses = sum(monthly_data[key]['expenses'].values())
                    monthly_data[key]['profit'] = income - total_expenses

        #  Admin or Analyst
        if role in ['admin', 'analyst']:
            query_budgets = """
                SELECT YEAR(budgetDate) AS year, MONTH(budgetDate) AS month, category, SUM(amount) AS amount
                FROM budget
                WHERE user_id = 2 -- %s
                GROUP BY YEAR(budgetDate), MONTH(budgetDate), category
                ORDER BY year DESC, month DESC, category;
            """
            cursor.execute(query_budgets, (user_id,))
            budgets = cursor.fetchall()
            for year, month, category, amount in budgets:
                key = f"{year}-{month_name[month]}"
                if key not in monthly_data:
                    monthly_data[key] = {'expenses': {}, 'income': 0, 'profit': 0, 'budgets': {}}
                monthly_data[key]['budgets'][category] = amount
        # User
        else:
            query_expenses = """
                SELECT YEAR(dateOfTransaction) AS year, MONTH(dateOfTransaction) AS month, category, amount
                FROM expense
                WHERE user_id = 1 -- %s
                GROUP BY YEAR(dateOfTransaction), MONTH(dateOfTransaction), category
                ORDER BY year DESC, month DESC, category;
            """                
            cursor.execute(query_expenses, (user_id,))
            monthyly_data = cursor.fetchall()

            monthly_data = {}
            for year, month, category, amount in expenses:
                key = f"{year}-{month_name[month]}"
                if key not in monthly_data:
                    monthly_data[key] = {'expenses': {}, 'income': 0, 'profit': 0}
                monthly_data[key]['expenses'][category] = amount

        cursor.close()
        return monthly_data

    def update_for_user(self, user_id):
        self.user_id = user_id
        self.user_id_label.config(text=f"User ID: {self.user_id}")
        self.update_spending()
'''