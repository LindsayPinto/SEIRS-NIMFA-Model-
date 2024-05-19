import tkinter as tk
from tkinter import ttk
from tkinter import StringVar
from tkinter.ttk import Combobox
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from model.network import Network
from model.sn_model import SNModel

class SimulationFrame(tk.Frame):
    def __init__(self, master, file, rates):
        super().__init__(master)

        self.rates = rates
        self.current_step = 0

        self.grid_rowconfigure(0, minsize= 700)
        self.grid_rowconfigure(1, weight=1)

        # Create network
        self.network = Network(file_name=file)
        self.network2 = Network(file_name=file)

        # Create tab control
        self.tabs = ttk.Notebook(self)
        self.tabs.grid(row=0, column=0, sticky="nsew")

        rates_frame = ttk.Frame(self)  
        rates_frame.grid_columnconfigure([0,12], minsize=120)
        rates_frame.grid_columnconfigure([1,2,4,5,7,8,10,11], minsize=80)
        rates_frame.grid_columnconfigure([3,6,9], minsize=40)

        rates_frame.grid_rowconfigure(0, weight=1)
        rates_frame.grid_rowconfigure(1, weight=1)

        tk.Label(rates_frame, text="Loss of immunity α:").grid(row=0, column=1, sticky="w")
        tk.Label(rates_frame, text="Infectious rate β:").grid(row=0, column=4, sticky="w")
        tk.Label(rates_frame, text="Recovery rate γ:").grid(row=0, column=7, sticky="w")
        tk.Label(rates_frame, text="Incubation rate δ:").grid(row=0, column=10, sticky="w")

        tk.Label(rates_frame, text=self.rates["alpha"]).grid(row=0, column=2, sticky="e")
        tk.Label(rates_frame, text=self.rates["beta"]).grid(row=0, column=5, sticky="e")
        tk.Label(rates_frame, text=self.rates["gamma"]).grid(row=0, column=8, sticky="e")
        tk.Label(rates_frame, text=self.rates["delta"]).grid(row=0, column=11, sticky="e")

        tk.Label(rates_frame, text="Update rate:").grid(row=1, column=1, sticky="w")
        tk.Label(rates_frame, text="Scanning rate:").grid(row=1, column=4, sticky="w")
        tk.Label(rates_frame, text="Injection rate:").grid(row=1, column=7, sticky="w")

        tk.Label(rates_frame, text=self.rates["t_update"]).grid(row=1, column=2, sticky="e")
        tk.Label(rates_frame, text=self.rates["t_scan"]).grid(row=1, column=5, sticky="e")
        tk.Label(rates_frame, text=self.rates["t_injection"]).grid(row=1, column=8, sticky="e")

        rates_frame.grid(row=1, column=0, sticky="nsew")

        # Heatmap Tab
        heat_map_frame = ttk.Frame(self.tabs)  
        heat_map_frame.grid_columnconfigure(1, minsize=280, weight=1)
        heat_map_frame.grid_rowconfigure(0, minsize= 48)
        heat_map_frame.grid_rowconfigure(1, minsize= 48)
        heat_map_frame.grid_rowconfigure(2, weight=1)
        heat_map_frame.grid_rowconfigure(3, minsize= 48)

        self.show_graph(heat_map_frame)

        heat_map_frame.control_frame = tk.Frame(heat_map_frame)
        heat_map_frame.control_frame.grid(row=0, column=1, sticky="nsew")

        heat_map_frame.control_frame.grid_columnconfigure(0, minsize=160, weight=1)
        heat_map_frame.control_frame.grid_columnconfigure(1, minsize=80)
        heat_map_frame.control_frame.grid_rowconfigure(0, minsize= 24)
        heat_map_frame.control_frame.grid_rowconfigure(1, minsize= 24)

        tk.Label(heat_map_frame.control_frame, text="Choose number of time-steps:").grid(row=0, column=0, sticky="w")
        iterations = [x for x in range(1,31)]
        heat_map_frame.time_steps = StringVar()
        self.cbox_time_steps = Combobox(heat_map_frame.control_frame, textvariable=heat_map_frame.time_steps, values=iterations, state="readonly", width=10)
        self.cbox_time_steps.current(14)
        self.cbox_time_steps.grid(row=0, column=1, sticky="ew")
        tk.Button(heat_map_frame.control_frame, command=lambda: self.run_model(self.rates), text="Run").grid(row=1, column=0, columnspan=2)

        self.heat_map_frame = heat_map_frame
        self.tabs.add(heat_map_frame, text="Heat Map")

        # Network Tab
        network_frame = ttk.Frame(self.tabs)
        
        network_frame.grid_columnconfigure(0, minsize=280, weight=1)
        network_frame.grid_columnconfigure(1, minsize=280, weight=1)
        network_frame.grid_rowconfigure(0, minsize= 48)
        network_frame.grid_rowconfigure(1, weight=1)
        network_frame.grid_rowconfigure(2, minsize= 24)

        btn_frame = tk.Frame(network_frame)
        btn_frame.grid(row=2, column=0, sticky="nsew")

        btn_frame.grid_columnconfigure([1,3,7,9], minsize=40)
        btn_frame.grid_columnconfigure([2,4,6,8], minsize=30)
        btn_frame.grid_columnconfigure(5, minsize=80)
        btn_frame.grid_columnconfigure([0,10], weight=1)

        tk.Button(btn_frame, command = lambda:self.change_current_graph("first"), text="<<").grid(row=0, column=1, sticky="ew")
        tk.Button(btn_frame, command = lambda:self.change_current_graph("back"), text="<").grid(row=0, column=3, sticky="ew")
        network_frame.step_label = tk.Label(btn_frame, text="Step #")
        network_frame.step_label.grid(row=0, column=5, sticky="nsew")
        tk.Button(btn_frame, command = lambda:self.change_current_graph("ford"), text=">").grid(row=0, column=7, sticky="ew")
        tk.Button(btn_frame, command = lambda:self.change_current_graph("last"), text=">>").grid(row=0, column=9, sticky="ew")

        btn_frame.grid_remove()
        network_frame.btn_frame = btn_frame

        network_frame.control_frame = tk.Frame(network_frame)
        network_frame.control_frame.grid(row=0, column=1, sticky="nsew")

        network_frame.control_frame.grid_columnconfigure(0, minsize=160, weight=1)
        network_frame.control_frame.grid_columnconfigure(1, minsize=80)
        network_frame.control_frame.grid_rowconfigure(0, minsize= 24)
        network_frame.control_frame.grid_rowconfigure(1, minsize= 24)

        tk.Label(network_frame.control_frame, text="Select initially infected node:").grid(row=0, column=0, sticky="w")
        node_indexes = [x for x in range(0,self.network.n)]
        network_frame.current_device = StringVar()
        self.cbox_devices = Combobox(network_frame.control_frame, textvariable=network_frame.current_device, values=node_indexes, state="readonly", width=10)
        self.cbox_devices.current(0)
        self.cbox_devices.grid(row=0, column=1, sticky="nw")
        tk.Button(network_frame.control_frame, command=lambda: self.run_model2(self.rates), text="Run").grid(row=1, column=0, columnspan=2)

        evolution_tabs = ttk.Notebook(network_frame)
        evolution_tabs.grid(row=1, column=1, rowspan=2, sticky="nsew")

        net_evolution_frame = ttk.Frame(evolution_tabs)
        evolution_tabs.add(net_evolution_frame, text="Network evolution")

        net_evolution_frame.grid_columnconfigure(0, weight=1)
        net_evolution_frame.grid_rowconfigure(0, minsize=48)
        net_evolution_frame.grid_rowconfigure(0, weight=1)

        self.net_evolution_frame = net_evolution_frame

        dev_evolution_frame = ttk.Frame(evolution_tabs)

        dev_evolution_frame.grid_columnconfigure(0, weight=1)
        dev_evolution_frame.grid_rowconfigure(0, minsize=24)
        dev_evolution_frame.grid_rowconfigure(1, minsize=48)
        dev_evolution_frame.grid_rowconfigure(2, weight=1)

        dev_evolution_frame.control_frame = tk.Frame(dev_evolution_frame)
        dev_evolution_frame.control_frame.grid(row=0, column=0, sticky="nsew")

        dev_evolution_frame.control_frame.grid_columnconfigure(0, minsize=160, weight=1)
        dev_evolution_frame.control_frame.grid_columnconfigure(1, minsize=80)
        dev_evolution_frame.control_frame.grid_rowconfigure(0, weight=1)

        tk.Label(dev_evolution_frame.control_frame, text="Select node to watch:").grid(row=0, column=0, sticky="w")
        node_indexes = [x for x in range(0,self.network.n)]
        dev_evolution_frame.current_device = StringVar()
        dev_evolution_frame.cbox_devices = Combobox(dev_evolution_frame.control_frame, textvariable=dev_evolution_frame.current_device, values=node_indexes, state="readonly", width=10)
        dev_evolution_frame.cbox_devices.current(0)
        dev_evolution_frame.cbox_devices.grid(row=0, column=1, sticky="nw")

        dev_evolution_frame.cbox_devices.bind('<<ComboboxSelected>>', self.change_watching_device)

        evolution_tabs.add(dev_evolution_frame, text="Device evolution")
        evolution_tabs.grid_remove()
        self.evolution_tabs = evolution_tabs

        self.dev_evolution_frame = dev_evolution_frame

        self.network_frame = network_frame
        self.tabs.add(network_frame, text="Network")

    def show_graph(self, parent):
        self.fig_graph = self.network.draw_graph_structure()
        canvas = FigureCanvasTkAgg(self.fig_graph, master = parent)
        canvas.draw()
        toolbar = NavigationToolbar2Tk(canvas, parent, pack_toolbar=False)
        toolbar.update()
        toolbar.grid(row=0, column=0)
        canvas.get_tk_widget().grid(row=1, column=0, rowspan=3)

    def show_graph2(self, parent):
        self.fig_evo_graph = self.model2.show_graph(self.current_step)
        canvas = FigureCanvasTkAgg(self.fig_evo_graph, master = parent)
        canvas.draw()
        toolbar = NavigationToolbar2Tk(canvas, parent, pack_toolbar=False)
        toolbar.update()
        toolbar.grid(row=0, column=0)
        canvas.get_tk_widget().grid(row=1, column=0, sticky="nw")
        self.network_frame.step_label.config(text=f"Step: {self.current_step*0.5}")
        self.network_frame.btn_frame.grid()
        self.evolution_tabs.grid()

    def run_model(self, rates):
        self.model = SNModel(self.network, rates)

        time_steps = int(self.heat_map_frame.time_steps.get())
        self.model.run_model_fe_node(time_steps)
        self.show_heatmap(self.model)

    def run_model2(self, rates):
        node = int(self.network_frame.current_device.get())
        self.network2.initialize_probs(node)
        self.model2 = SNModel(self.network2, rates)
        self.model2.run_model()

        self.current_step = len(self.model2.nodes_comp)-1
        self.show_evolution(self.model2, node)
        self.show_graph2(self.network_frame)

    def show_heatmap(self, model):
        self.fig_heatmap = model.show_heatmap()
        canvas = FigureCanvasTkAgg(self.fig_heatmap, master = self.heat_map_frame)
        canvas.draw()
        toolbar = NavigationToolbar2Tk(canvas, self.heat_map_frame, pack_toolbar=False)
        toolbar.update()
        toolbar.grid(row=1, column=1)
        canvas.get_tk_widget().grid(row=2, column=1)

        critical_frame = tk.Frame(self.heat_map_frame)
        tk.Label(critical_frame, text="Critical nodes: " + str(model.critical_nodes)).pack()
        tk.Label(critical_frame, text="Max. infected: " + str(model.max_infected)).pack()
        critical_frame.grid(row=3, column=1)

    def show_evolution(self, model, node):
        self.fig_net_evo = model.plot_network_evolution()
        canvas = FigureCanvasTkAgg(self.fig_net_evo, master = self.net_evolution_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0, sticky="nsew")
        toolbar = NavigationToolbar2Tk(canvas, self.net_evolution_frame, pack_toolbar=False)
        toolbar.update()
        toolbar.grid(row=0, column=0)
        self.dev_evolution_frame.cbox_devices.current(node)
        self.show_device_evolution(model, node)

    def show_device_evolution(self, model, node):
        self.fig_dev_evo = model.plot_node_evolution(node)
        canvas = FigureCanvasTkAgg(self.fig_dev_evo, master = self.dev_evolution_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=2, column=0, sticky="nwse")
        toolbar = NavigationToolbar2Tk(canvas, self.dev_evolution_frame, pack_toolbar=False)
        toolbar.update()
        toolbar.grid(row=1, column=0)

    def change_current_graph(self, direction:str):
        if(direction=="back"):
            self.current_step-=1
        elif(direction=="ford"):
            self.current_step+=1
        elif(direction=="first"):
            self.current_step=0
        else:
            self.current_step=len(self.model2.nodes_comp)-1

        if self.current_step < 0:
            self.current_step = 0
            return
        elif self.current_step > len(self.model2.nodes_comp)-1:
            self.current_step=len(self.model2.nodes_comp)-1
            return
        
        # Update time step label
        self.network_frame.step_label.config(text=f"Step: {self.current_step*0.5}")
        self.show_graph2(self.network_frame)

    def change_watching_device(self, event):
        node = int(self.dev_evolution_frame.current_device.get())
        self.show_device_evolution(self.model2, node)