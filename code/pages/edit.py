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
from sections.budget_section import Budget

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

class EditPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.user_id = None 

        self.top_frame = tk.Frame(self)
        self.top_frame.pack(side='top', fill='x', expand=False)
        tk.Label(self.top_frame, text="Edit Page", font=('Helvetica', 16)).pack(side='top', fill='x', pady=10)

        self.user_id_label = tk.Label(self.top_frame, text="User ID: Not Set", font=('Helvetica', 12), fg='red')
        self.user_id_label.pack(side='right', padx=10, pady=10)

        tk.Button(self.top_frame, text="Go to Graph Page", command=lambda: controller.show_frame("GraphPage")).pack(side='right', padx=10, pady=10)
        tk.Button(self.top_frame, text="Go Back to Splash Page", command=lambda: controller.show_frame("SplashPage")).pack(side='left', padx=10, pady=10)

        self.view_spending_btn = tk.Button(self, text="View Monthly Spending", command=self.show_monthly_spending)
        self.view_spending_btn.pack(pady=10)

        self.sections_frame = tk.Frame(self)
        self.sections_frame.pack(fill='both', expand=True)
        self.setup_ui()

    def setup_ui(self):
        test_conn_button = tk.Button(self, text="Test Database Connection", command=self.test_connection, bg='blue', fg='white')
        test_conn_button.pack(fill='x', expand=True, pady=4)

    def setup_sections(self):
        # Clear existing sections if any
        for widget in self.sections_frame.winfo_children():
            widget.destroy()
        
        # Setup sections dynamically, now with updated self.user_id
        self.setup_section(Income, "Income Section", self.user_id)
        self.setup_section(Expense, "Expense Section", self.user_id)
        self.setup_section(Savings_Goal, "Savings Goal Section", self.user_id)  
        self.setup_section(Savings_Goal_Per_Cat, "Savings Goal Per Category Section", self.user_id)  
        self.setup_section(Spending_Limit, "Spending Limit Section", self.user_id)
        self.setup_section(Budget, "Budget Section", self.user_id)    

    def setup_section(self, section_class, title, user_id):
        frame = tk.Frame(self.sections_frame, borderwidth=2, relief="groove")
        frame.pack(fill='both', expand=True, side='left', padx=5, pady=5)
        db_connection = create_db_connection()
        section = section_class(frame, db_connection, user_id)

    def update_for_user(self, user_id):
        print(f"Updating EditPage with user ID: {user_id}")
        self.user_id = user_id
        self.user_id_label.config(text=f"User ID: {self.user_id}")
        self.setup_sections()  
        
    def test_connection(self):
        connection = create_db_connection()  # Directly call the standalone function
        if connection is not None and connection.is_connected():
            messagebox.showinfo("Connection Test", "Connected to MySQL database")
            connection.close()
        else:
            messagebox.showerror("Connection Test", "Failed to connect to database")
    
    def show_monthly_spending(self):
        self.controller.show_frame("MonthlySpendingPage")

    def setup_menu(self):
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)
        view_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Monthly Spending", command=lambda: self.show_frame("MonthlySpendingPage"))

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
