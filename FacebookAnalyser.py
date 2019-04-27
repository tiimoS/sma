import networkx as nx


def main():
    load_graph();


def load_graph():
    G = nx.read_edgelist('facebook_combined.txt')
    print(nx.info(G));


if __name__ == '__main__':
    main()


