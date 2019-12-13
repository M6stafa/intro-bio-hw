# -*- coding: utf-8 -*-

# Find an Eulerian Path in a Graph
# http://rosalind.info/problems/ba3g


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


def find_start_node(in_degree, out_degree):
    for node in in_degree.keys():
        if out_degree[node] - in_degree[node] == 1:
            return node
    return in_degree.keys()[0]


def dfs(start_node, edges, out_degree):
    node_stack = [start_node]
    path = []

    while len(node_stack) > 0:
        head = node_stack[-1]
        if out_degree[head] > 0:
            node_stack.append(edges[head].pop())
            out_degree[head] -= 1
        else:
            path.append(str(node_stack.pop()))

    return reversed(path)


# Main
edges, in_degree, out_degree = parse_input()
start_node = find_start_node(in_degree, out_degree)
path = dfs(start_node, edges, out_degree)

print('->'.join(path))
