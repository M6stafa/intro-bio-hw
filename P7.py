# -*- coding: utf-8 -*-

# RNA Splicing
# http://rosalind.info/problems/splc


# Constants
PROTEIN_CODE_STOP = 'STOP'
PROTEIN_CODE_TABLE = {
    'GCA': 'A',
    'GCC': 'A',
    'GCG': 'A',
    'GCT': 'A',

    'AGA': 'R',
    'AGG': 'R',
    'CGA': 'R',
    'CGC': 'R',
    'CGG': 'R',
    'CGT': 'R',

    'GAC': 'D',
    'GAT': 'D',

    'AAC': 'N',
    'AAT': 'N',

    'TGC': 'C',
    'TGT': 'C',

    'GAA': 'E',
    'GAG': 'E',

    'CAA': 'Q',
    'CAG': 'Q',

    'GGA': 'G',
    'GGC': 'G',
    'GGG': 'G',
    'GGT': 'G',

    'CAC': 'H',
    'CAT': 'H',

    'ATA': 'I',
    'ATC': 'I',
    'ATT': 'I',

    'TTA': 'L',
    'TTG': 'L',
    'CTA': 'L',
    'CTC': 'L',
    'CTG': 'L',
    'CTT': 'L',

    'AAA': 'K',
    'AAG': 'K',

    'ATG': 'M',

    'TTC': 'F',
    'TTT': 'F',

    'CCA': 'P',
    'CCC': 'P',
    'CCG': 'P',
    'CCT': 'P',

    'AGC': 'S',
    'AGT': 'S',
    'TCA': 'S',
    'TCC': 'S',
    'TCG': 'S',
    'TCT': 'S',

    'ACA': 'T',
    'ACC': 'T',
    'ACG': 'T',
    'ACT': 'T',

    'TGG': 'W',

    'TAC': 'Y',
    'TAT': 'Y',

    'GTA': 'V',
    'GTC': 'V',
    'GTG': 'V',
    'GTT': 'V',

    'TAA': PROTEIN_CODE_STOP,
    'TAG': PROTEIN_CODE_STOP,
    'TGA': PROTEIN_CODE_STOP,
}

# Helper Functions
def input_fasta():
    labels = []
    bases = []

    while True:
        try:
            new_line = input()
        except EOFError:
            break
        else:
            if new_line[0] == '>':
                labels.append(new_line[1:])
                bases.append('')
            else:
                bases[-1] += new_line

    return labels, bases

def dna_to_protein(dna):
    protein = ''
    for i in range(0, len(dna), 3):
        new_protein = PROTEIN_CODE_TABLE[dna[i:i+3]]

        if new_protein == PROTEIN_CODE_STOP:
            break

        protein += new_protein

    return protein

# Main
_, bases = input_fasta()

dna = bases[0]
patterns = bases[1:]

occurrence_ranges = []
curr_pattern_index = [0] * len(patterns)

for i in range(len(dna)):
    base = dna[i]

    for p in range(len(patterns)):
        pattern = patterns[p]

        if base == pattern[curr_pattern_index[p]]:
            curr_pattern_index[p] += 1
            if curr_pattern_index[p] == len(pattern):  # all pattern bases has been saw
                curr_pattern_index[p] = 0
                occurrence_ranges.append((i - len(pattern) + 1, i + 1))
        else:
            if base == pattern[0]:
                curr_pattern_index[p] = 1
            else:
                curr_pattern_index[p] = 0

start = 0
new_dna = ''
for occurrence_range in occurrence_ranges:
    new_dna += dna[start:occurrence_range[0]]
    start = occurrence_range[1]

new_dna += dna[start:]

print(dna_to_protein(new_dna))
