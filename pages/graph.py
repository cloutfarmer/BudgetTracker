import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import mysql.connector

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

    def set_user_id(self, user_id):
        self.user_id = user_id
        if self.user_id is not None:
            self.user_id_label.config(text=f"User ID: {self.user_id}")
            self.draw_user_financials()
    
    def update_for_user(self, user_id):
        print(f"Updating EditPage with user ID: {user_id}")
        self.user_id = user_id
        self.user_id_label.config(text=f"User ID: {self.user_id}")
        
    def draw_user_financials(self):
        # Dummy data for the example; replace with your actual data retrieval and plotting logic
        data = [10, 20, 30, 40, 50]  # Example data
        fig = Figure(figsize=(5, 4), dpi=100)
        plot = fig.add_subplot(1, 1, 1)
        plot.plot(data, 'r-')
        
        canvas = FigureCanvasTkAgg(fig, master=self)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
