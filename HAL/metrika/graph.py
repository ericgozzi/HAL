from ..pixels import get_blank_picture
from ..pixels import Picture
from ..pixels import Color

from .rule import Rule

import networkx as nx


class Graph:

    def __init__(self):
       self.graph = nx.Graph()



    @property
    def edges(self):
        return self.graph.edges()

    @property
    def eigenvector_centrality(self) -> dict:
        return nx.eigenvector_centrality(self.graph)
    

    def draw(self) -> Picture:

        pic_size = 2000
        scale_factor = pic_size/2-pic_size/20

        pic = get_blank_picture(pic_size, pic_size, Color.BLACK)
        pos = self.get_nodes_coordinate('KAMADA-KAWAI')
        edges = self.edges
        for edge in edges:
            p1x = (pos[edge[0]][0]) * scale_factor + pic_size/2
            p1y = (pos[edge[0]][1]) * scale_factor + pic_size/2
            p2x = (pos[edge[1]][0]) * scale_factor + pic_size/2
            p2y = (pos[edge[1]][1]) * scale_factor + pic_size/2
            pic.draw_line((p1x, p1y), (p2x, p2y))
        
        for key in pos.keys():
            x = pos[key][0] * scale_factor + pic_size/2
            y = pos[key][1] * scale_factor + pic_size/2
            pic.draw_circle((x, y), 30)
            pic.draw_text(key, (x, y), 20)
        
        return pic



    def add_node(self, node: str):
        """Add a node to the graph."""
        self.graph.add_node(node)

    def add_edge(self, node1: str, node2: str):
        """Add an edge between two nodes."""
        self.graph.add_edge(node1, node2)

    def add_edges_from_connections(self, rules: Rule) -> None:
        for item1, item2 in rules.rules:
            self.graph.add_edge(item1, item2)


    def get_eigenvector_of(self, item) -> float:
        eigenvector_centrality_dictionary = self.eigenvector_centrality
        item_centrality = eigenvector_centrality_dictionary[item]
        return item_centrality
    


    def get_nodes_coordinate(self, method):
        if method == 'SPRING':
            positions = nx.spring_layout(self.graph)

        elif method == 'KAMADA-KAWAI':
            positions = nx.kamada_kawai_layout(self.graph)

        elif method == 'SPECTRAL':
            positions = nx.spectral_layout(self.graph)

        elif method == 'CIRCULAR':
            positions = nx.circular_layout(self.graph)
        
        else:
            positions = nx.random_layout(self.graph)

        return positions
