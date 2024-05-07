import tkinter as tk
from tkinter import messagebox

class ParamsFrame(tk.Frame):
    def __init__(self, master, show_main_menu, show_simulation, file):
        super().__init__(master)

        self.show_simulation = show_simulation
        self.file = file

        self.grid_columnconfigure(1, minsize=140)
        self.grid_columnconfigure(2, minsize=200)
        self.grid_columnconfigure(3, minsize=60)
        self.grid_columnconfigure(4, minsize=140)
        self.grid_columnconfigure(5, minsize=200)
        self.grid_columnconfigure([0,6], weight=1)

        self.grid_rowconfigure([1,3,5,7,9], minsize= 24)
        self.grid_rowconfigure([2,4,6,8], minsize= 20)
        self.grid_rowconfigure([0,10], weight=1)

        tk.Label(self, text="Loss of immunity α:").grid(row=1, column=1, sticky="w")
        tk.Label(self, text="Infectious rate β:").grid(row=3, column=1, sticky="w")
        tk.Label(self, text="Recovery rate γ:").grid(row=5, column=1, sticky="w")
        tk.Label(self, text="Incubation rate δ:").grid(row=7, column=1, sticky="w")

        tk.Label(self, text="Update rate:").grid(row=1, column=4, sticky="w")
        tk.Label(self, text="Scanning rate:").grid(row=3, column=4, sticky="w")
        tk.Label(self, text="Injection rate:").grid(row=5, column=4, sticky="w")

        self.entry_p1 = tk.Entry(self)
        self.entry_p1.grid(row=1, column=2, sticky="ew")
        self.entry_p1.insert(0, "0.5")

        self.entry_p2 = tk.Entry(self)
        self.entry_p2.grid(row=3, column=2, sticky="ew")
        self.entry_p2.insert(0, "0.5")

        self.entry_p3 = tk.Entry(self)
        self.entry_p3.grid(row=5, column=2, sticky="ew")
        self.entry_p3.insert(0, "0.5")

        self.entry_p4 = tk.Entry(self)
        self.entry_p4.grid(row=7, column=2, sticky="ew")
        self.entry_p4.insert(0, "0.5")

        self.entry_p5 = tk.Entry(self)
        self.entry_p5.grid(row=1, column=5, sticky="ew")
        self.entry_p5.insert(0, "0.57")

        self.entry_p6 = tk.Entry(self)
        self.entry_p6.grid(row=3, column=5, sticky="ew")
        self.entry_p6.insert(0, "0.482")

        self.entry_p7 = tk.Entry(self)
        self.entry_p7.grid(row=5, column=5, sticky="ew")
        self.entry_p7.insert(0, "0.15")

        self.btn_frame = tk.Frame(self)
        self.btn_frame.grid(row=9, column=1, columnspan=5, sticky="nsew")

        self.btn_frame.grid_columnconfigure([1,3,5], minsize=100)
        self.btn_frame.grid_columnconfigure([2,4], minsize=40)
        self.btn_frame.grid_columnconfigure([0,6], weight=1)

        tk.Button(self.btn_frame, text="Cancel", command=show_main_menu).grid(row=0, column=1, sticky="ew")
        tk.Button(self.btn_frame, text="Reset", command=self.reset_fields).grid(row=0, column=3, sticky="ew")
        tk.Button(self.btn_frame, text="Visualize", command=self.validate_params).grid(row=0, column=5, sticky="ew")

    def validate_params(self):
        alpha = 0.0
        try:
            alpha = float(self.entry_p1.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid value for α parameter")
            return

        beta = 0.0
        try:
            beta = float(self.entry_p2.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid value for β parameter")
            return

        gamma = 0.0
        try:
            gamma = float(self.entry_p3.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid value for γ parameter")
            return

        delta = 0.0
        try:
            delta = float(self.entry_p4.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid value for δ parameter")
            return

        t_update = 0.0
        try:
            t_update = float(self.entry_p5.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid value for update rate")
            return

        t_scan = 0.0
        try:
            t_scan = float(self.entry_p6.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid value for scan rate")
            return

        t_injection = 0.0
        try:
            t_injection = float(self.entry_p7.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid value for injection rate")
            return
        
        rates = {'alpha': alpha, 'beta':beta, 'delta':delta, 'gamma':gamma,
                 't_update': t_update, 't_scan': t_scan, 't_injection': t_injection}

        self.show_simulation(self.file, rates) 
    
    def reset_fields(self):
        response = messagebox.askyesno("Confirmation", "All fields will be reset. Are you sure?")
        
        if response == False:
            return
        
        self.entry_p1.delete(0, tk.END)
        self.entry_p2.delete(0, tk.END)
        self.entry_p3.delete(0, tk.END)
        self.entry_p4.delete(0, tk.END)
        self.entry_p5.delete(0, tk.END)
        self.entry_p6.delete(0, tk.END)
        self.entry_p7.delete(0, tk.END)