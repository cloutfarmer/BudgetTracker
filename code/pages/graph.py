import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

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
        self.user_id = user_id
        self.user_id_label.config(text=f"User ID: {self.user_id}")
        self.draw_user_financials()

    def draw_user_financials(self):
        fig = Figure(figsize=(10, 4), dpi=100)

        # Line plot
        ax1 = fig.add_subplot(121)
        data1 = np.random.rand(10)
        ax1.plot(data1, 'r-')
        ax1.set_title('Random Line Plot')
        ax1.set_xlabel('X axis')
        ax1.set_ylabel('Y axis')

        # Bar chart
        ax2 = fig.add_subplot(122)
        data2 = np.random.randint(1, 10, size=5)
        ax2.bar(np.arange(len(data2)), data2, color='blue')
        ax2.set_title('Random Bar Chart')
        ax2.set_xlabel('Categories')
        ax2.set_ylabel('Values')

        # Drawing the canvas
        canvas = FigureCanvasTkAgg(fig, master=self)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

