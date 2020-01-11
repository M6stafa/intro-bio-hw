# -*- coding: utf-8 -*-

# Adapt SmallParsimony to Unrooted Trees
# http://rosalind.info/problems/ba7g


# imports
import math
from copy import deepcopy


# Constants
CHARS = ['A', 'C', 'G', 'T']


# Helper Functions
def min_score_k(k, values):
    min_char = None
    min_score = math.inf

    for i in values:
        alpha = 0 if i == k else 1
        if values[i] + alpha < min_score:
            min_score = values[i] + alpha
            min_char = i

    return min_char, min_score


def calc_char(left_values_i, right_values_i):
    min_chars_i = {}
    value_i = {}

    for k in CHARS:
        left_min_char, left_score = min_score_k(k, left_values_i)
        right_min_char, right_score = min_score_k(k, right_values_i)
        min_chars_i[k] = (left_min_char, right_min_char)
        value_i[k] = left_score + right_score

    return min_chars_i, value_i


def calc_dna(left_values, right_values):
    value = [None for _ in range(len(left_values))]
    min_chars = [None for _ in range(len(left_values))]

    for i in range(len(left_values)):
        min_chars[i], value[i] = calc_char(left_values[i], right_values[i])

    return min_chars, value


def small_parsimony(G, leafs):
    visited = {node: False for node in G.keys()}
    dnas = {node: None for node in G.keys()}
    min_chars = {node: None for node in G.keys()}
    values = {node: None for node in G.keys()}
    for leaf in leafs:
        dnas[leaf] = leaf
        values[leaf] = [{c: math.inf for c in CHARS} for _ in range(len(leaf))]
        for i in range(len(leaf)):
            values[leaf][i][leaf[i]] = 0

    stack = ['root']
    visited['root'] = True
    T = {}

    while len(stack) > 0:
        node = stack[-1]
        if node in leafs:
            stack.pop()
            continue

        if node not in T:
            T[node] = []

        is_ripe = True
        for child in G[node]:
            if not visited[child]:
                visited[child] = True
                stack.append(child)
                is_ripe = False
                T[node].append(child)
        if is_ripe:
            stack.pop()
            left_child = T[node][0]
            right_child = T[node][1]
            min_chars[node], values[node] = calc_dna(values[left_child], values[right_child])

    stack = ['root']
    dnas['root'] = ''.join([min(values['root'][i], key=values['root'][i].get) for i in range(len(values['root']))])
    while len(stack) > 0:
        node = stack.pop()
        child_dnas = [min_chars[node][i][dnas[node][i]] for i in range(len(dnas[node]))]
        left_dna = right_dna = ''
        for i in range(len(child_dnas)):
            left_dna += child_dnas[i][0]
            right_dna += child_dnas[i][1]
        dnas[T[node][0]] = left_dna
        dnas[T[node][1]] = right_dna

        if T[node][0] not in leafs:
            stack.append(T[node][0])
        if T[node][1] not in leafs:
            stack.append(T[node][1])

    return dnas


def hamming_distance(dna1, dna2):
    d = 0
    for i in range(len(dna1)):
        d += 1 if dna1[i] != dna2[i] else 0

    return d


# Main
n = int(input())
G = {}
leafs = []
has_root = False
num_edges = 2 ** (int(math.log2(n)) + 1) - 3
for _ in range(2 * num_edges):
    v, w = input().split('->')
    if v not in G:
        G[v] = []
    G[v].append(w)
    if not has_root and v[0] not in CHARS and w[0] not in CHARS:
        G['root'] = [v, w]
        has_root = True
    if v[0] in CHARS and v not in leafs:
        leafs.append(v)

dnas = small_parsimony(G, leafs)
del G['root']

sum_distances = 0
outputs = []
for v in G:
    for w in G[v]:
        hd = hamming_distance(dnas[v], dnas[w])
        sum_distances += hd
        outputs.append(f'{dnas[v]}->{dnas[w]}:{hd}')

print(sum_distances // 2)
print('\n'.join(outputs))
