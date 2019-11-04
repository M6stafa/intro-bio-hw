# -*- coding: utf-8 -*-

# Counting DNA Nucleotides
# http://rosalind.info/problems/dna

DNA = input()

nucleotidesCount = {
    'A': 0,
    'C': 0,
    'G': 0,
    'T': 0,
}

for n in DNA:
    nucleotidesCount[n] += 1

print(nucleotidesCount['A'], nucleotidesCount['C'], nucleotidesCount['G'], nucleotidesCount['T'])
