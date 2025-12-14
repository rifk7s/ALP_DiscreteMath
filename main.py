"""Contoh penggunaan class Graf untuk pembelajaran teori graf."""
from graf import Graf


def main() -> None:
    graph = Graf()

    # Menambah node
    for n in [1, 2, 3, 4, 5]:
        graph.add_node(n)

    # Menambah edge berbobot
    graph.add_edge(1, 2, weight=4.5)
    graph.add_edge(1, 3, weight=3.2)
    graph.add_edge(2, 4, weight=2.7)
    graph.add_edge(3, 4, weight=1.8)
    graph.add_edge(1, 4, weight=6.7)
    graph.add_edge(3, 5, weight=2.7)

    print(graph)
    print("Nodes:", graph.nodes())
    print("Edges:", graph.edges(data=True))

    # Visualisasi graf
    pos = graph.visualize_graph(title="Graf Contoh")

    # Jalur terpendek (berbobot)
    path = graph.shortest_path(1, 5)
    print("Shortest path 1->5:", path)

    # Visualisasi jalur terpendek
    graph.visual_shortest_path(1, 5, pos=pos)


if __name__ == "__main__":
    main()
