# -*- coding: utf-8 -*-

# Implement the Neighbor Joining Algorithm
# http://rosalind.info/problems/ba7e


# imports
import math
from copy import deepcopy


# Helper Functions
def neighbor_joining(D, m, removed = []):
    n = len(D) - len(removed)
    D_len = len(D)

    if n == 2:
        # T ← tree consisting of a single edge of length D1,2
        T = {}
        i, j = [i for i in range(D_len) if i not in removed]
        T[i] = {j: D[i][j]}
        T[j] = {i: D[i][j]}
        return T

    # D* ← neighbor-joining matrix constructed from the distance matrix D
    # find elements i and j such that D*i,j is a minimum non-diagonal element of D*
    total_distance = [0 for i in range(D_len)]
    for i in range(D_len):
        new_sum = 0
        for j in range(D_len):
            if j not in removed:
                new_sum += D[i][j]
        total_distance[i] = new_sum
    Dstar = [[0 for i in range(D_len)] for j in range(D_len)]
    min_value = math.inf
    indexes = None
    for i in range(D_len):
        for j in range(i + 1, D_len):
            if i in removed or j in removed:
                continue

            Dstar[i][j] = Dstar[j][i] = (n - 2) * D[i][j] - total_distance[i] - total_distance[j]
            if Dstar[i][j] < min_value:
                min_value = Dstar[i][j]
                indexes = (i, j)

    # Δ ← (TotalDistanceD(i) - TotalDistanceD(j)) /(n - 2)
    i, j = indexes
    delta = (total_distance[i] - total_distance[j]) / (n - 2)

    # limbLengthi ← (1/2)(Di,j + Δ)
    # limbLengthj ← (1/2)(Di,j - Δ)
    limb_len_i = (D[i][j] + delta) / 2
    limb_len_j = (D[i][j] - delta) / 2

    # add a new row/column m to D so that Dk,m = Dm,k = (1/2)(Dk,i + Dk,j - Di,j) for any k
    D.append([0 for k in range(len(D))])
    for k in range(len(D)):
        D[k].append(0)
    for k in range(len(D) - 1):
        if k in removed:
            continue
        D[k][m] = D[m][k] = (D[k][i] + D[k][j] - D[i][j]) / 2

    # D ← D with rows i and j removed
    # D ← D with columns i and j removed
    removed.append(i)
    removed.append(j)

    # recursive call
    T = neighbor_joining(D, m + 1, removed)

    # add two new limbs (connecting node m with leaves i and j) to the tree T
    # assign length limbLengthi to Limb(i)
    # assign length limbLengthj to Limb(j)
    T[m][i] = limb_len_i
    T[m][j] = limb_len_j
    T[i] = { m: limb_len_i }
    T[j] = { m: limb_len_j }

    return T


# Main
n = int(input())
D = []
for i in range(n):
    D.append(list(map(int, input().split(' '))))

tree = neighbor_joining(D, len(D))

for v in sorted(tree.keys()):
    for w in sorted(tree[v].keys()):
        print(f'{v}->{w}:{tree[v][w]:.3f}')
