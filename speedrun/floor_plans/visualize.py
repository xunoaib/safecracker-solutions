import matplotlib.pyplot as plt
import networkx as nx
from dependencies import dependency_graph


def visualize_dependency_graph(dependency_graph):
    G = nx.DiGraph()

    for target, sources in dependency_graph.items():
        for source in sources:
            G.add_edge(source, target)

    pos = nx.nx_agraph.graphviz_layout(G, prog='dot')

    plt.figure(figsize=(12, 8))
    nx.draw(
        G,
        pos,
        with_labels=True,
        arrows=True,
        node_size=2000,
        node_color='lightblue',
        font_size=10,
        font_weight='bold'
    )
    plt.title("Dependency Graph")
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    visualize_dependency_graph(dependency_graph)
