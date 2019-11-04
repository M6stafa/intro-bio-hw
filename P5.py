# -*- coding: utf-8 -*-

# Find All Approximate Occurrences of a Pattern in a String
# http://rosalind.info/problems/ba1h

def is_match(str1, str2, max_mismatch):
    mismatch_counter = 0
    for i in range(len(str1)):
        if str1[i] != str2[i]:
            mismatch_counter += 1
        if mismatch_counter > max_mismatch:
            return False

    return True


pattern = input()
genome = input()
max_mismatch = int(input())

indicies = []
pattern_length = len(pattern)

for i in range(len(genome) - pattern_length + 1):
    if is_match(genome[i:i+pattern_length], pattern, max_mismatch):
        indicies.append(str(i))

print(' '.join(indicies))
