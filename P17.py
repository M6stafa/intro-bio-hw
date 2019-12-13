# -*- coding: utf-8 -*-

# Find All Approximate Occurrences of a Collection of Patterns in a String
# http://rosalind.info/problems/ba9o


# Helper Functions
def bwtable(text):
    text_len = len(text)
    rotations = [text]
    for i in range(1, text_len):
        rotations.append(text[text_len-i:] + text[:text_len-i])
    return sorted(rotations)


def get_auxiliaries(table):
    first_occurrences = {}
    counts = { '$': [0], 'A': [0], 'T': [0], 'C': [0], 'G': [0] }
    total_counts = { '$': 0, 'A': 0, 'T': 0, 'C': 0, 'G': 0 }
    last_column = []

    for row, text in enumerate(table):
        if text[0] not in first_occurrences.keys():
            first_occurrences[text[0]] = row

        total_counts[text[-1]] += 1
        for symbol in counts.keys():
            counts[symbol].append(total_counts[symbol])

        last_column.append(text[-1])

    return first_occurrences, counts, last_column


def approximate_better_bwmatching(pattern, first_occurrences, counts, last_column, max_d):
    pattern = list(pattern)
    # Each branch has (top, botton, symbol index, remaining d)
    branches = [(0, len(last_column) - 1, len(pattern) - 1, max_d)]
    results = []

    while len(branches) > 0:
        top, bottom, symbol_index, rem_d = branches.pop()

        if top <= bottom:
            if symbol_index >= 0:
                symbol = pattern[symbol_index]
                unique_symbols = set(last_column[top:bottom + 1])
                valid_symbols = []
                if rem_d == 0:
                    if symbol in unique_symbols:
                        valid_symbols = [symbol]
                else:
                    valid_symbols = unique_symbols

                for valid_symbol in valid_symbols:
                    new_top = first_occurrences[valid_symbol] + counts[valid_symbol][top]
                    new_bottom = first_occurrences[valid_symbol] + counts[valid_symbol][bottom + 1] - 1
                    branches.append((new_top, new_bottom, symbol_index - 1, rem_d if valid_symbol == symbol else rem_d - 1))
            else:
                results.append((top, bottom))

    return results


# Main
text = input()
patterns = input().split(' ')
d = int(input())

table = bwtable(text + '$')
first_occurrences, counts, last_column = get_auxiliaries(table)
first_column = sorted(last_column)

matches = []
for pattern in patterns:
    ranges = approximate_better_bwmatching(pattern, first_occurrences, counts, last_column, d)
    for r in ranges:
        for i in range(r[0], r[1] + 1):
            matches.append(len(text) - table[i].index('$'))

print(' '.join(map(str, sorted(matches))))
