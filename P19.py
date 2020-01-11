# -*- coding: utf-8 -*-

# Implement UPGMA
# http://rosalind.info/problems/ba7d


# imports
import math
from copy import deepcopy


# Helper Functions
def clusters_distance(D, c1, c2):
    sum_d = 0

    for c1_node in c1:
        for c2_node in c2:
            sum_d += D[c1_node][c2_node]

    return sum_d / (len(c1) * len(c2))


def UPGMA(D):
    C = deepcopy(D)
    clusters = { i: (i,) for i in range(len(C)) }
    T = { i: [] for i in range(len(C)) }
    age = { i: 0 for i in range(len(C)) }
    new_cluster_index = len(C)

    while len(clusters.keys()) > 1:
        # find the two closest clusters Ci and Cj
        min_distance = math.inf
        min_clusters = None
        for key_i in clusters.keys():
            for key_j in clusters.keys():
                if key_i != key_j:
                    c_distance = clusters_distance(D, clusters[key_i], clusters[key_j])
                    if c_distance < min_distance:
                        min_distance = c_distance
                        min_clusters = (key_i, key_j)

        # merge Ci and Cj into a new cluster Cnew with |Ci| + |Cj| elements
        Ci, Cj = min_clusters
        Cnew = new_cluster_index
        new_cluster_index += 1
        clusters[Cnew] = clusters[Ci] + clusters[Cj]

        # add a new node labeled by cluster Cnew to T
        # connect node Cnew to Ci and Cj by directed edges
        T[Cnew] = [Ci, Cj]
        T[Ci].append(Cnew)
        T[Cj].append(Cnew)

        # Age(Cnew) ← DCi,Cj / 2
        age[Cnew] = min_distance / 2

        # remove the rows and columns of D corresponding to Ci and Cj
        # not needed

        # remove Ci and Cj from Clusters
        del clusters[Ci]
        del clusters[Cj]

        # add a row/column to D for Cnew by computing D(Cnew, C) for each C in Clusters
        C.append([0 for i in range(len(C))])
        for i in range(len(C)):
            C[i].append(0)

        for c_key in clusters.keys():
            if c_key != Cnew:
                C[c_key][Cnew] = C[Cnew][c_key] = clusters_distance(D, clusters[c_key], clusters[Cnew])

    return T, age


# Main
n = int(input())
D = []
for i in range(n):
    D.append(list(map(float, input().split(' '))))

tree, age = UPGMA(D)

for v in tree.keys():
    for w in tree[v]:
        print(f'{v}->{w}:{abs(age[v] - age[w]):.3f}')
