# -*- coding: utf-8 -*-

# Find the Reverse Complement of a String
# http://rosalind.info/problems/ba1c

DNA = input()

reverse = {
    'A': 'T',
    'C': 'G',
    'G': 'C',
    'T': 'A',
}

for i in range(len(DNA) - 1, -1, -1):
    print(reverse[DNA[i]], end='')

print()
