import numpy as np
import json
import networkx as nx
import matplotlib.pyplot as plt
from model.states import States

class Network:

    def __init__(self, file_name:str="") -> None:
        """
        n:= number of nodes in the network
        adjMatrix := adjacency matrix representing connection between nodes
            adjMatrix[i][j] = 1 , i and j are neighbours
            adjMatrix[i][j] = 0 , i and j are not neighbours
        graph:= graph that represents the network (created from adjMatrix)
        init_states = the initial probabilities for every node for every state
        """
        self.load_struc_from_json(file_name)


    def load_struc_from_json(self, file_name):
        """
        Load network from json file not including initial probabilities
        """
        try:
            with open(file_name) as json_file:
                data = json.load(json_file)
                self.n = len(data)
                self.adjMatrix = np.zeros((self.n,self.n), dtype = int)
                for i in range(self.n):
                    self.adjMatrix[i,:] = data[i]['adjList']
                # graph:= graph that represents the network (created from adjMatrix)
                self.graph = nx.Graph(self.adjMatrix)
                self.init_states = np.zeros((4,self.n), dtype=float)
        except FileNotFoundError as fnf:
            mess = str(fnf).split('] ', 1)[1]
            raise FileNotFoundError(mess)
        except Exception as e:
            raise Exception(f"Unable to parse te json file {file_name}")

    def initialize_probs(self, infected_node):
        """
        Initialize the probabilities for each of the nodes for each compartment
        infected_node: node where the infection starts
        """
        self.init_states[States.S.value]=np.ones(self.n, dtype=float)
        self.init_states[States.S.value][infected_node]=0
        self.init_states[States.I.value][infected_node]=1

    def set_nodes_compartment(self,compartments:dict):
        """
        Set each node's compartment (graph's attribute)
        """
        nx.set_node_attributes(self.graph, compartments, "compartment")

    def draw_graph_structure(self):
        """
        Plot the graph structure
        """
        fig = plt.figure(figsize=(6, 6))
        pos = nx.spring_layout(self.graph, seed=3068)
        nx.pos = pos 
        nx.draw(self.graph, pos=pos, with_labels=True)
        plt.axis("equal")
        plt.close()
        return fig