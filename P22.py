# -*- coding: utf-8 -*-

# Find a Median String
# http://rosalind.info/problems/ba2b


# imports
import itertools


# Helper Functions
def read_dnas():
    dnas = []

    while True:
        try:
            new_line = input()
        except EOFError:
            break
        else:
            dnas.append(new_line)

    return dnas


def hamming_distance(s1, s2):
    d = 0
    for i in range(len(s1)):
        d += 1 if s1[i] != s2[i] else 0

    return d


# Main
k = int(input())
dnas = read_dnas()

min_d = len(dnas) * k + 1
median_string = None

for kmer in itertools.product(['A', 'C', 'G', 'T'], repeat=k):
    kmer = ''.join(kmer)
    ds = [k + 1 for _ in range(len(dnas))]

    for dna_i, dna in enumerate(dnas):
        for i in range(0, len(dna) - k + 1):
            ds[dna_i] = min(ds[dna_i], hamming_distance(kmer, dna[i:i+k]))

    d = sum(ds)
    if d < min_d:
        min_d = d
        median_string = kmer

print(median_string)
