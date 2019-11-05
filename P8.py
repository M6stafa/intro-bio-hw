# -*- coding: utf-8 -*-

# Finding a Protein Motif
# http://rosalind.info/problems/mprt

# imports
from urllib.request import urlopen


# Constants
MOTIF = ['=N', '!P', ['S', 'T'], '!P']

# Helper Functions
def parse_input():
    protein_ids = []

    while True:
        try:
            new_line = input()
        except EOFError:
            break
        else:
            protein_ids.append(new_line)

    return protein_ids


def get_protein_sequence(id):
    f = urlopen('https://www.uniprot.org/uniprot/{}.fasta'.format(id))
    lines = f.readlines()
    return ''.join(map(lambda x: str(x[0:-1], 'utf-8'), lines[1:]))


def check_motif(amino_acid, motif, motif_index):
    motif_check = motif[motif_index]

    if type(motif_check) is list:  # check multiple match
        return amino_acid in motif_check
    if motif_check[0] == '=':  # check exact match
        return amino_acid == motif_check[1]
    if motif_check[0] == '!':  # check not match
        return amino_acid != motif_check[1]

    assert False  # code must not reachs here

# Main
protein_ids = parse_input()

for protein_id in protein_ids:
    seq = get_protein_sequence(protein_id)

    occurrences = []
    checks = []

    for i in range(len(seq)):
        amino_acid = seq[i]
        remove_checks = []

        if check_motif(amino_acid, MOTIF, 0):
            checks.append(0)

        for c in range(len(checks)):
            if check_motif(amino_acid, MOTIF, checks[c]):
                checks[c] += 1
                if checks[c] == len(MOTIF):  # motif has been saw
                    remove_checks.append(checks[c])
                    occurrences.append(i - len(MOTIF) + 2)
            else:
                remove_checks.append(checks[c])

        for check in remove_checks:
            checks.remove(check)

    if len(occurrences) > 0:
        print(protein_id)
        print(' '.join(map(str, occurrences)))
