import sys
import os
import time
import argparse
import random
from progress import Progress


# Loads a graph from a text file
def load_graph(args):

    file = open("school_web2024-1.txt")
    contains = []
    G = {}

    # Iterate through the file line by line
    for line in file:
        # And split each line into two URLs
        node, target = line.split()
        if node not in contains:
            G[node] = [target]
            contains.append(node)
        else:
            G[node].append(target)
    return G

# Prints the amount of nodes and edges in a graph
def print_stats(graph):
    print("Nodes =", len(graph))
    edges = 0
    for i in graph.values():
        edges += len(i)
    print("Edges =", edges)

def stochastic_page_rank(graph, args):
    
    c = 0
    visited = []
    totals = {}
    node_key = random.choice(list(graph.keys()))
    while c < args[0]:
        node_values = graph[node_key]
        if len(node_values) > 0:
            node_key = random.choice(node_values)
            visited.append(node_key)
        else:
            node_key = random.choice(list(graph.keys()))
        c += 1
    for i in graph:
        totals[i] = visited.count(i)

    return totals[args[1]]


def distribution_page_rank(graph, args):

    c = 0
    initial_p = 1 / len(graph)
    node_p = {}
    next_p = {}
    for i in graph:
        node_p[i] = initial_p
    while c < args[0]:
        for i in graph:
            next_p[i] = 0
        for i in graph:
            out_edges = graph[i]
            out_edges_size = len(out_edges)
            p = node_p[i] / out_edges_size
            for j in out_edges:
                next_p[j] = p + next_p[j]
        for i in graph:
            node_p[i] = next_p[i]
        c += 1
    
    return node_p[args[1]]

"""

parser = argparse.ArgumentParser(description="Estimates page ranks from link information")
parser.add_argument('datafile', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
                    help="Textfile of links among web pages as URL tuples")
parser.add_argument('-m', '--method', choices=('stochastic', 'distribution'), default='stochastic',
                    help="selected page rank algorithm")
parser.add_argument('-r', '--repeats', type=int, default=1_000_000, help="number of repetitions")
parser.add_argument('-s', '--steps', type=int, default=100, help="number of steps a walker takes")
parser.add_argument('-n', '--number', type=int, default=20, help="number of results shown")

if __name__ == '__main__':
    args = parser.parse_args()
    algorithm = distribution_page_rank if args.method == 'distribution' else stochastic_page_rank

    graph = load_graph(args)

    print_stats(graph)

    start = time.time()
    ranking = algorithm(graph, args)
    stop = time.time()
    time = stop - start
    top = sorted(ranking.items(), key=lambda item: item[1], reverse=True)
    sys.stderr.write(f"Top {args.number} pages:\n")
    print('\n'.join(f'{100*v:.2f}\t{k}' for k,v in top[:args.number]))
    sys.stderr.write(f"Calculation took {time:.2f} seconds.\n")

"""