# -*- coding: utf-8 -*-

# Generate All Maximal Non-Branching Paths in a Graph
# http://rosalind.info/problems/ba3m


# Helper Functions
def parse_input():
    edges = {}
    in_degree = {}
    out_degree = {}

    while True:
        try:
            new_line = input()
        except EOFError:
            break
        else:
            node, end_nodes = new_line.split(' -> ')
            node = int(node)
            end_nodes = list(map(int, end_nodes.split(',')))

            edges[node] = []
            for end_node in end_nodes:
                edges[node].append(end_node)
                try:
                    in_degree[end_node] += 1
                except:
                    in_degree[end_node] = 1
                try:
                    out_degree[end_node] = out_degree[end_node]
                except:
                    out_degree[end_node] = 0
            out_degree[node] = len(end_nodes)
            try:
                in_degree[node] = in_degree[node]
            except:
                in_degree[node] = 0

    return edges, in_degree, out_degree


def maximal_non_branching_paths(edges, in_degree, out_degree):
    paths = []

    for v in edges.keys():
        if not (in_degree[v] == 1 and out_degree[v] == 1):
            if out_degree[v] > 0:
                for w in edges[v]:
                    new_path = [v, w]
                    while in_degree[w] == 1 and out_degree[w] == 1:
                        u = edges[w][0]
                        new_path.append(u)
                        w = u
                    paths.append(new_path)

    # Find isolated cycles
    isolated_cycles_nodes = []
    for v in edges.keys():
        if in_degree[v] == 1 and out_degree[v] == 1 and v not in isolated_cycles_nodes:
            w = edges[v][0]
            new_path = [v, w]
            while in_degree[w] == 1 and out_degree[w] == 1:
                u = edges[w][0]
                new_path.append(u)
                w = u

                if u == v:
                    paths.append(new_path)
                    isolated_cycles_nodes += new_path
                    break

    return paths


# Main
edges, in_degree, out_degree = parse_input()
paths = maximal_non_branching_paths(edges, in_degree, out_degree)

for path in paths:
    print(' -> '.join(map(str, path)))
