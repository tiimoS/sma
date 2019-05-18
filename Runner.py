
from louvain.Louvain_detection import louvain_method
from louvain.Louvain_detection import visualize_network



def main():
    communities = louvain_method()
    visualize_network("sample.pdf", communities)


if __name__ == '__main__':
    main()
