from HAL.pixels import Picture, get_blank_picture, Color

from HAL.metrika import Rule, Graph

cnts = [('a', 'b'), ('b', 'c'), ('a', 'c'), ('c', 'd'), ('d', 'd'), ('a', 'a'), ('l', 'a'), ('p', 'b'), ('w', 'z'), ('a', 'd'), ('a', 'z'), ('a', 'w'), ('p', 'l')]
conn = Rule(cnts)
print(conn)
graph = Graph()
graph.add_edges_from_connections(conn)
graph.draw().show()