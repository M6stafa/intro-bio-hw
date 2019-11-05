# -*- coding: utf-8 -*-

# Motzkin Numbers and RNA Secondary Structures
# http://rosalind.info/problems/motz

# Constants
BASE_COMPLEMENT = {
    'A': 'U',
    'U': 'A',
    'G': 'C',
    'C': 'G',
}

MOTZKIN_NUMBERS = {}


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


def rna_motzkin_number(rna):
    if len(rna) <= 1:  # no base or only one base
        return 1

    # Check cache
    if rna in MOTZKIN_NUMBERS.keys():
        return MOTZKIN_NUMBERS[rna]

    sum = 1  # one for not select anythings
    rna_length = len(rna)

    for i in range(rna_length):
        base = rna[i]

        # Check edges
        for j in range(i + 1, rna_length):
            other_base = rna[j]
            if other_base == BASE_COMPLEMENT[base]:  # this can be edge
                sum += rna_motzkin_number(rna[i + 1:j]) * rna_motzkin_number(rna[j + 1:])

    # Cache
    MOTZKIN_NUMBERS[rna] = sum

    return sum


# Main
rna = input_fasta()

print(rna_motzkin_number(rna) % 1_000_000)
