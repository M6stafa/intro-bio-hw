# -*- coding: utf-8 -*-

# Implement AdditivePhylogeny
# http://rosalind.info/problems/ba7c

# imports
import math


# Helper Functions
def limb(D, n):
    limb_length = math.inf

    for i in range(n):
        for k in range(i + 1, n):
            length = (D[i][n] + D[n][k] - D[i][k]) / 2
            if length < limb_length:
                limb_length = length

    return limb_length


def find_path(T, start, end):
    num_nodes = len(T)
    visited = [False] * num_nodes
    visited[start] = True
    parent = { start: None }
    stack = [start]
    while len(stack) > 0:
        node = stack.pop()
        for i in range(num_nodes):
            if not visited[i] and T[i][node] != 0:
                visited[i] = True
                parent[i] = node

                if i == end:
                    path = []
                    p_node = end
                    while p_node != None:
                        path.append(p_node)
                        p_node = parent[p_node]

                    return path[::-1]

                stack.append(i)

    return False


def find_mid_node(T, i, k, x):
    path = find_path(T, i, k)
    rem_x = x
    for i in range(1, len(path)):
        rem_x -= T[path[i]][path[i - 1]]
        if rem_x == 0:
            return True, (path[i])
        if rem_x < 0:
            return False, (path[i - 1], T[path[i]][path[i - 1]] + rem_x, path[i], -rem_x)

    return False, (i, x, k, T[i][k] - x)


def additive_phylogeny(D, n):
    if n == 1:
        T = [[0 for i in range(len(D))] for j in range(len(D))]
        T[0][1] = T[1][0] = D[0][1]
        return T

    limb_length = limb(D, n)
    for j in range(n):
        D[j][n] = D[n][j] = D[j][n] - limb_length

    x = None
    for i in range(n):
        for k in range(i + 1, n):
            if D[i][k] == D[i][n] + D[n][k]:
                x = D[i][n]
                break
        if x is not None:
            break

    T = additive_phylogeny(D, n - 1)

    has_mid_node, data = find_mid_node(T, i, k, x)
    if has_mid_node:
        mid_node, = data
    else:
        prev_node, prev_node_len, next_node, next_node_len = data
        T[prev_node][next_node] = T[next_node][prev_node] = 0
        # Create new node
        T.append([0] * len(T))
        for row in range(len(T)):
            T[row].append(0)
        mid_node = len(T) - 1
        T[prev_node][mid_node] = T[mid_node][prev_node] = prev_node_len
        T[next_node][mid_node] = T[mid_node][next_node] = next_node_len

    T[mid_node][n] = T[n][mid_node] = limb_length

    return T


# Main
n = int(input())
D = []
for i in range(n):
    D.append(list(map(int, input().split(' '))))

tree = additive_phylogeny(D, n - 1)

for i in range(len(tree)):
    for j in range(len(tree)):
        if i != j and tree[i][j] > 0:
            print(f'{i}->{j}:{int(tree[i][j])}')
