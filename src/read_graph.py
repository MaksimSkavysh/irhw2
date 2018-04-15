import networkx as nx
import matplotlib.pyplot as plt


def plot_graph(G):
    nx.draw(G, with_labels=True, font_weight='bold')
    plt.show()


def read_graph():
    G = nx.read_gexf('wiki.gexf')
    plot_graph(G)


read_graph()
