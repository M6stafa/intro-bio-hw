# -*- coding: utf-8 -*-

# Perform a Multiple Sequence Alignment with a Profile HMM
# http://rosalind.info/problems/ba10g


# imports
import math


# Main
text = input()

input()
θ, σ = map(float, input().split(' '))

input()
Σ = input().split(' ')

input()
dnas = []
while True:
    try:
        new_dna = input()
    except EOFError:
        break
    else:
        dnas.append(new_dna)

num_dnas = len(dnas)
dna_length = len(dnas[0])

# Create the HMM
gray_cols = []
for i in range(dna_length):
    num_gaps = sum([1 for j in range(num_dnas) if dnas[j][i] == '-'])
    if num_gaps / num_dnas >= θ:
        gray_cols.append(i)

dna_length -= len(gray_cols)

# Create emission matrix
e = {}
for i in range(dna_length):
    e[f'M{i+1}'] = {}
    e[f'I{i+1}'] = {}
    for char in Σ:
        e[f'M{i+1}'][char] = σ
        e[f'I{i+1}'][char] = σ

e['I0'] = {}
for char in Σ:
    e['I0'][char] = σ

offset = 0
for i in range(dna_length + len(gray_cols)):
    if i in gray_cols:
        if i - 1 in gray_cols:
            continue
        state = f'I{i+offset}'
        emissions = []
        for j in range(i, dna_length + len(gray_cols)):
            if j not in gray_cols:
                break
            offset -= 1
            emissions += [dna[j] for dna in dnas]
    else:
        state = f'M{i+offset+1}'
        emissions = [dna[i] for dna in dnas]

    num_non_gaps = len(emissions) - emissions.count('-')
    for char in Σ:
        e[state][char] += emissions.count(char) / num_non_gaps

for state in e:
    sum_probs = sum(e[state].values())
    for char in Σ:
        e[state][char] = math.log(e[state][char] / sum_probs)

# Create transition matrix
t = {}

t['S'] = {'I0': σ, 'M1': σ, 'D1': σ}
t['I0'] = {'I0': σ, 'M1': σ, 'D1': σ}

for i in range(dna_length - 1):
    t[f'M{i+1}'] = {}
    t[f'D{i+1}'] = {}
    t[f'I{i+1}'] = {}
    for state in [f'I{i+1}', f'M{i+2}', f'D{i+2}']:
        t[f'M{i+1}'][state] = σ
        t[f'D{i+1}'][state] = σ
        t[f'I{i+1}'][state] = σ

t[f'M{dna_length}'] = {f'I{dna_length}': σ, 'E': σ}
t[f'D{dna_length}'] = {f'I{dna_length}': σ, 'E': σ}
t[f'I{dna_length}'] = {f'I{dna_length}': σ, 'E': σ}

curr_states = ['S' for _ in range(num_dnas)]
offset = 0
for i in range(dna_length + len(gray_cols) + 1):
    if i in gray_cols:
        offset -= 1

    next_states = {}
    for dna_i, dna in enumerate(dnas):
        if i == dna_length + len(gray_cols):
            next_states[dna_i] = 'E'
        else:
            if i in gray_cols:
                if dna[i] == '-':
                    continue
                if curr_states[dna_i][0] == 'I':
                    next_states[dna_i] = curr_states[dna_i]
                else:
                    next_states[dna_i] = f'I{i+offset+1}'
            elif dna[i] == '-':
                next_states[dna_i] = f'D{i+offset+1}'
            else:
                next_states[dna_i] = f'M{i+offset+1}'

        t[curr_states[dna_i]][next_states[dna_i]] += 1 / curr_states.count(curr_states[dna_i])

    for dna_i in range(len(dnas)):
        if dna_i in next_states:
            curr_states[dna_i] = next_states[dna_i]

for state in t:
    sum_probs = sum(t[state].values())
    for next_state in t[state]:
        t[state][next_state] = math.log(t[state][next_state] / sum_probs)

# Create Topological order
def topological_order():
    for i in range(dna_length):
        yield (0, f'D{i+1}')
    for i in range(len(text)):
        yield (i + 1, 'I0')
        for j in range(dna_length):
            yield (i + 1, f'M{j+1}')
            yield (i + 1, f'D{j+1}')
            yield (i + 1, f'I{j+1}')
    yield (len(text) + 1, 'E')

# Get parents
def is_state_exists(col_state):
    col, state = col_state

    if state == 'S':
        return col == 0

    mode, number = state[0], int(state[1:])
    if mode == 'I':
        return col > 0 and number >= 0
    if mode == 'M':
        return col > 0 and number >= 1
    if mode == 'D':
        return col >= 0 and number >= 1

def get_parents(col_state):
    col, state = col_state

    if state == 'E':
        return [
            (len(text), f'M{dna_length}'),
            (len(text), f'D{dna_length}'),
            (len(text), f'I{dna_length}'),
        ]

    number = int(state[1:])

    if col == 0:
        if number == 1:
            return [(0, 'S')]
        return [(0, f'D{number-1}')]

    if state == 'I0':
        if col == 1:
            return [(0, 'S')]
        return [(col-1, 'I0')]

    if state == 'M1':
        if col == 1:
            return [(0, 'S')]
        return [(col-1, 'I0')]

    if state[0] == 'M':
        check_states = [
            (col-1, f'M{number-1}'),
            (col-1, f'D{number-1}'),
            (col-1, f'I{number-1}'),
        ]
        return [check_state for check_state in check_states if is_state_exists(check_state)]

    if state[0] == 'D':
        check_states = [
            (col, f'M{number-1}'),
            (col, f'D{number-1}'),
            (col, f'I{number-1}'),
        ]
        return [check_state for check_state in check_states if is_state_exists(check_state)]

    if state[0] == 'I':
        check_states = [
            (col-1, f'M{number}'),
            (col-1, f'D{number}'),
            (col-1, f'I{number}'),
        ]
        return [check_state for check_state in check_states if is_state_exists(check_state)]

# Viterbi Algorithm
max_parents = {}
S = {(0, 'S'): 0}
for col_state in topological_order():
    col, state = col_state
    parents = get_parents(col_state)

    values = {}
    for parent_col_state in parents:
        parent_col, parent_state = parent_col_state
        values[parent_col_state] = t[parent_state][state] + S[parent_col_state]

    max_parent = max(values, key=values.get)
    max_parents[col_state] = max_parent

    emission = 0
    if state[0] == 'M' or state[0] == 'I':
        emission = e[state][text[col-1]]
    S[col_state] = emission + values[max_parent]

# Create path
π = [max_parents[(len(text) + 1, 'E')]]
while π[-1][1] != 'S':
    π.append(max_parents[π[-1]])

print(' '.join([col_state[1] for col_state in π[-2::-1]]))
