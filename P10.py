# -*- coding: utf-8 -*-

# Maximum Matchings and RNA Secondary Structures
# http://rosalind.info/problems/mmch

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
num_u = 0
num_g = 0
num_c = 0

for base in rna:
    if base == 'A':
        num_a += 1
    elif base == 'U':
        num_u += 1
    elif base == 'G':
        num_g += 1
    elif base == 'C':
        num_c += 1

print(factorial(max(num_a, num_u)) // factorial(abs(num_a - num_u)) *
      factorial(max(num_g, num_c)) // factorial(abs(num_g - num_c)))
