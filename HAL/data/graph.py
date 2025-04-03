

import networkx as nx

class Graph:

    def __init__(self):
       self.graph = nx.Graph()


    @property
    def eigenvector_centrality(self) -> dict:
        return nx.eigenvector_centrality(self.graph)



    def add_edges_from_connections(self, connections: list[tuple]) -> None:
        for item1, item2 in connections:
            self.graph.add_edge(item1, item2)



    def get_eigenvector_of(self, item) -> float:
        eigenvector_centrality_dictionary = self.eigenvector_centrality
        item_centrality = eigenvector_centrality_dictionary[item]
        return item_centrality
