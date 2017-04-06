import networkx as nx
import os,sys
import random


class GraphSampling:

    def __init__(self,gnx):
        self.graph = gnx

    def sample_nodes(self, sampling_size = 10):
        nodes = self.graph.nodes()
        set_of_nodes = set()
        while len(set_of_nodes) < sampling_size:
            set_of_nodes.add(random.choice(nodes))
        sub = self.graph.subgraph(set_of_nodes)
        if nx.is_directed(self.graph):
            maximal_connected = max(nx.weakly_connected_component_subgraphs(sub), key=len)
        else:
            maximal_connected = max(nx.connected_component_subgraphs(sub), key=len)
        print maximal_connected.nodes()
        print maximal_connected.edges()
        print len(maximal_connected.edges())
        print len(maximal_connected.nodes())
        return maximal_connected

    def sample_edges(self, sampling_size = 10):
        edges = self.graph.edges()
        set_of_edges = set()
        while len(set_of_edges) < sampling_size:
            set_of_edges.add(random.choice(edges))
        if nx.is_directed(self.graph):
            sub = nx.DiGraph()
            sub.add_edges_from(set_of_edges)
            maximal_connected = max(nx.weakly_connected_component_subgraphs(sub), key=len)
        else:
            sub = nx.Graph()
            sub.add_edges_from(set_of_edges)
            maximal_connected = max(nx.connected_component_subgraphs(sub), key=len)
        print maximal_connected.nodes()
        print maximal_connected.edges()
        print len(maximal_connected.edges())
        print len(maximal_connected.nodes())
        return maximal_connected
