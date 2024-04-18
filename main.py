import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
from pages.splash import SplashPage
from pages.edit import EditPage
from pages.graph import GraphPage


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

class MainApplication(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Budget Tracker")
        self.geometry("800x600")
        self.user_id = None

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (SplashPage, EditPage, GraphPage):
            frame = F(parent=container, controller=self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("SplashPage")


    def show_frame(self, cont):
        frame = self.frames[cont]
        if hasattr(frame, 'update_for_user'):
            frame.update_for_user(self.user_id) 
        frame.tkraise()


def main():
    app = MainApplication()
    app.mainloop()

if __name__ == "__main__":
    main()
