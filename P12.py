# -*- coding: utf-8 -*-

# Construct the De Bruijn Graph of a String
# http://rosalind.info/problems/ba3d


# Helper functions
def find_edges(k1_mer, k1_mers):
    edges = []
    for mer in k1_mers:
        if mer == k1_mer:
            continue
        if k1_mer[1:] == mer[:-1]:
            edges.append(mer)

    return edges


# Main
k = int(input())
dna = input()

k1_mers = []  # k-1 mers
for i in range(0, len(dna) - (k - 2)):
    new_mer = dna[i:i+k-1]
    if new_mer not in k1_mers:
        k1_mers.append(new_mer)

for k1_mer in k1_mers:
    edges = find_edges(k1_mer, k1_mers)
    if len(edges) > 0:
        print('{} -> {}'.format(k1_mer, ','.join(edges)))
