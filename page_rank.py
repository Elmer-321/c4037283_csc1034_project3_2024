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

        # Checks if a node has been counted before
        if node not in contains:
            # If it hasn't, adds it and then adds the site it links to as an edge
            G[node] = [target]
            contains.append(node)
        else:
            # If the node is already in the dictionary, the site it links to is added as a value to that node
            G[node].append(target)
    return G

# Prints the amount of nodes and edges in a graph
def print_stats(graph):

    # Prints the amount of nodes by finding the length of the graph
    print("Nodes =", len(graph))

    # Initialises edges as 0
    edges = 0

    # Counts every value for every node, then prints the amount of edges
    for i in graph.values():
        edges += len(i)
    print("Edges =", edges)


# Returns the page rank by using random walkers to check how many times each node is visited
def stochastic_page_rank(graph, args):
    
    # Initialises counter, an array of how many times each node has been visited, and a totals dictionary to be outputted
    c = 0
    visited = []
    totals = {}

    # Generates a random node to start at
    node_key = random.choice(list(graph.keys()))

    # Loops the amount of times inputted
    while c < args[0]:

        # Checks if the amount of sites linked to by the current node is greater than 0
        node_values = graph[node_key]
        if len(node_values) > 0:

            # If yes, sets the node to a random out of the possible options, and adds this node to the visited array
            node_key = random.choice(node_values)
            visited.append(node_key)
        else:

            # If not, visits a new random node
            node_key = random.choice(list(graph.keys()))
        c += 1

    # Finds the total amount each node has been visited by counting how many times it appears in the array
    for i in graph:
        totals[i] = visited.count(i)

    # Returns the total number of times the inputted site has been visited
    return totals[args[1]]

# Returns the page rank by using distribution to work out how likely each site is to be visited
def distribution_page_rank(graph, args):

    # Initialises counter, the initial probability of each node to be visited (which depends on the size of the graph), the current node probability and the next node probability
    c = 0
    initial_p = 1 / len(graph)
    node_p = {}
    next_p = {}

    # Sets the probability of each node to the initial probability
    for i in graph:
        node_p[i] = initial_p

    # Loops the amount of times inputted
    while c < args[0]:

        # Resets the probability for the next node to be visited to 0
        for i in graph:
            next_p[i] = 0

        # For each node, counts the amount of out edges, works out the probability for each to be visited and adds this to those nodes probability
        for i in graph:
            out_edges = graph[i]
            out_edges_size = len(out_edges)
            p = node_p[i] / out_edges_size
            for j in out_edges:
                next_p[j] = p + next_p[j]

        # For each node, sets their current probability to their probability to be visited
        for i in graph:
            node_p[i] = next_p[i]
        c += 1
    
    # Returns the distribution page rank of the inputted site
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



graph = load_graph(())
print_stats(graph)
stochastic_page_rank(graph, (10000, "http://www.ncl.ac.uk/computing/news/"))
distribution_page_rank(graph, (10000, "http://www.ncl.ac.uk/computing/news/"))