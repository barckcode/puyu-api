from .init import prox


def get_nodes():
    return prox.cluster.config.nodes.get()
