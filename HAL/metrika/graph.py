

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
