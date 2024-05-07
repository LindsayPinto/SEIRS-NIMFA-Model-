import tkinter as tk
from view.main_menu_frame import MainMenuFrame
from view.params_frame import ParamsFrame
from view.simulation_frame import SimulationFrame

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SEIRS-NIMFA epidemiologic model")
        self.minsize(1000, 740)
        self.iconbitmap("img/uniandes.ico")

        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.show_main_menu()

    def show_main_menu(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        self.main_menu = MainMenuFrame(self.main_frame, self.show_params, self.quitApp)
        self.main_menu.pack(fill=tk.BOTH, expand=True)
        self.main_menu.update()
        self.main_menu.place(in_=self.main_frame, anchor="center", relx=0.5, rely=0.5)

    def show_params(self, file):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        self.params = ParamsFrame(self.main_frame, self.show_main_menu, self.show_simulation, file)
        self.params.pack(fill=tk.BOTH, expand=True)

    def show_simulation(self, file, rates):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        self.simulation = SimulationFrame(self.main_frame, file, rates)
        self.simulation.pack(fill=tk.BOTH, expand=True)

    def quitApp(self):
        self.destroy()

if __name__ == "__main__":
    app = Application()
    app.mainloop()