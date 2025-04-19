from networkx.algorithms.link_prediction import within_inter_cluster
from ..pixels import get_blank_picture
from ..pixels import Picture
from ..pixels import Color

from .rule import Rule

import networkx as nx

import math


class Graph:

    def __init__(self):
       self.graph = nx.DiGraph()



    @property
    def edges(self):
        return self.graph.edges()

    @property
    def eigenvector_centrality(self) -> dict:
        return nx.eigenvector_centrality(self.graph)


    def draw(self, **kwargs) -> Picture:

        graph_type: str = kwargs.get('graph_type', 'KAMADA-KAWAI')

        show_node: bool = kwargs.get('show_node', True)
        node_radius: int = kwargs.get('node_radius', 30)
        node_color: Color = kwargs.get('node_color', Color.WHITE)

        show_label: bool = kwargs.get('show_label', True)
        label_size: bool = kwargs.get('label_size', 20)
        label_color: Color = kwargs.get('label_color', Color.BLACK)

        edge_direction: bool = kwargs.get('edge_direction', True)
        edge_width: int = kwargs.get('edge_width', 2)
        arrowhead_length: int = kwargs.get('arrowhead_length', 20)
        edge_color: Color = kwargs.get('edge_color', Color.WHITE)

        pic_size: int = kwargs.get('pic_size', 2000)
        background_color: Color = kwargs.get('background_color', Color.BLACK)
        invert_colors: bool = kwargs.get('invert_colors', False)


        scale_factor = pic_size/2-pic_size/20
        pic = get_blank_picture(pic_size, pic_size, background_color)
        pos = self.get_nodes_coordinate(graph_type)
        edges = self.edges
        for edge in edges:
            p1x = (pos[edge[0]][0]) * scale_factor + pic_size/2
            p1y = (pos[edge[0]][1]) * scale_factor + pic_size/2
            p2x = (pos[edge[1]][0]) * scale_factor + pic_size/2
            p2y = (pos[edge[1]][1]) * scale_factor + pic_size/2

             # Direction vector
            dx = p2x - p1x
            dy = p2y - p1y
            angle = math.atan(dy/dx)

            if dx < 0:
                xds = -1
                xde = 1
            else:
                xds = 1
                xde = -1

            if dy < 0:
                yds = -1
                yde = 1
            else:
                yds = 1
                yde = -1


            # Move start and end points to the edge of the circles
            start = (p1x + abs(math.cos(angle)) * node_radius * xds,
                     p1y + abs(math.sin(angle)) * node_radius * yds)
            end = (p2x + abs(math.cos(angle)) * node_radius * xde,
                   p2y + abs(math.sin(angle)) * node_radius * yde)

            if edge_direction:
                pic.draw_arrow(start, end, width=edge_width, arrowhead_length=arrowhead_length, color = edge_color)
            else:
                pic.draw_line(start, end, width=edge_width, color=edge_color)

        for key in pos.keys():
            x = pos[key][0] * scale_factor + pic_size/2
            y = pos[key][1] * scale_factor + pic_size/2
            if show_node:
                pic.draw_circle((x, y), node_radius, color=node_color)
            if show_label:
                pic.draw_text(key, (x, y), label_size, color=label_color)

        if invert_colors:
            pic.invert_colors()

        return pic



    def add_node(self, node: str):
        """Add a node to the graph."""
        self.graph.add_node(node)

    def add_edge(self, node1: str, node2: str):
        """Add an edge between two nodes."""
        self.graph.add_edge(node1, node2)

    def build_graph_from_rules(self, rules: Rule) -> None:
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
