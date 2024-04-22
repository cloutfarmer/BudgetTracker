import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
from pages.splash import SplashPage
from pages.edit import EditPage
from pages.graph import GraphPage
from pages.monthly import MonthlySpendingPage

class MainApplication(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Budget Tracker")
        self.geometry("800x600")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (SplashPage, EditPage, GraphPage, MonthlySpendingPage):
            frame = F(parent=container, controller=self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("SplashPage")
        self.setup_menu()

    def create_db_connection(self):
        """Create and return a database connection."""
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='BudgetTracker',
                user='root',
                password='Louis269*'  # Consider securing your password
            )
            return connection
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to connect to the database: {e}")
            return None

    def show_frame(self, cont):
        """Switch frames in the application."""
        frame = self.frames[cont]
        if hasattr(frame, 'update_for_user'):
            frame.update_for_user(self.user_id)  # Ensure user_id is set correctly elsewhere in your application
        frame.tkraise()

    def setup_menu(self):
        """Setup the application menu."""
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)
        view_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Monthly Spending", command=lambda: self.show_frame("MonthlySpendingPage"))

    def test_connection(self):
        """Test the database connection."""
        try:
            connection = self.create_db_connection()
            if connection.is_connected():
                messagebox.showinfo("Connection Test", "Connected to MySQL database")
            connection.close()
        except Error as e:
            messagebox.showerror("Connection Test", f"Error: {e}")

def main():
    app = MainApplication()
    app.mainloop()

if __name__ == "__main__":
    main()
