# -*- coding: utf-8 -*-

# Implement BetterBWMatching
# http://rosalind.info/problems/ba9m


# Helper Functions
def reverse_bwt(bwt):
    last_col = list(bwt)
    first_col = sorted(last_col)

    text = ''
    symbol = '$'
    count = 0
    for i in range(len(bwt) - 1):
        for si, s in enumerate(last_col):
            if s == symbol:
                if count == 0:
                    symbol = first_col[si]
                    text += symbol
                    for j in range(si):
                        if first_col[j] == symbol:
                            count += 1
                    break
                else:
                    count -= 1

    return text + '$'


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


def better_bwmatching(pattern, first_occurrences, counts, last_column):
    pattern = list(pattern)
    top = 0
    bottom = len(last_column) - 1
    while top <= bottom:
        if len(pattern) > 0:
            symbol = pattern.pop()
            has_symbol = False
            for i in range(top, bottom + 1):
                if last_column[i] == symbol:
                    has_symbol = True
                    break
            if has_symbol:
                top = first_occurrences[symbol] + counts[symbol][top]
                bottom = first_occurrences[symbol] + counts[symbol][bottom + 1] - 1
            else:
                return 0
        else:
            return bottom - top + 1


# Main
bwt = input()
substrings = input().split(' ')

text = reverse_bwt(bwt)
first_occurrences, counts, last_column = get_auxiliaries(bwtable(text))

matches = []
for substring in substrings:
    matches.append(str(better_bwmatching(substring, first_occurrences, counts, last_column)))

print(' '.join(matches))
