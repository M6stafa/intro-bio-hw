# -*- coding: utf-8 -*-

# Perfect Matchings and RNA Secondary Structures
# http://rosalind.info/problems/pmch

# imports
from math import factorial


# Helper Functions
def input_fasta():
    rna = ''

    while True:
        try:
            new_line = input()
        except EOFError:
            break
        else:
            if new_line[0] != '>':
                rna += new_line

    return rna


# Main
rna = input_fasta()

num_a = 0
num_g = 0

for base in rna:
    if base == 'A':
        num_a += 1
    elif base == 'G':
        num_g += 1

print(factorial(num_a) * factorial(num_g))
