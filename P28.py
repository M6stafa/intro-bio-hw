# -*- coding: utf-8 -*-

# Implement Viterbi Learning
# http://rosalind.info/problems/ba10i


# imports
import math


# Helper Functions
def read_input():
    iterations = int(input())

    input()
    X = input()

    input()
    Σ = input().split('\t')

    input()
    states = input().split('\t')

    input()
    input()
    t = {}
    for state in states:
        probs = list(map(float, input().split('\t')[1:]))
        t[state] = {}
        for i in range(len(probs)):
            t[state][states[i]] = math.log(probs[i])

    input()
    input()
    e = {}
    for state in states:
        probs = list(map(float, input().split('\t')[1:]))
        e[state] = {}
        for i in range(len(probs)):
            e[state][Σ[i]] = math.log(probs[i])

    return iterations, X, Σ, states, t, e


def viterbi_algorithm(X, Σ, states, t, e):
    S = [{s: e[s][X[0]] + math.log(1 / len(states)) for s in states}]
    parents = [{s: '' for s in states}]

    for i in range(1, len(X)):
        S.append({})
        parents.append({})
        for k in states:
            values = {l: t[l][k] + S[i-1][l] for l in states}
            parents[i][k] = max(values, key=values.get)
            S[i][k] = e[k][X[i]] + values[parents[i][k]]

    π = max(S[-1], key=S[-1].get)

    for i in range(len(X) - 1, -1, -1):
        π += parents[i][π[-1]]

    return π[::-1]


def viterbi_learning(X, Σ, π, states, t, e):
    for state in states:
        for char in Σ:
            e[state][char] = 0.0
        for next_state in states:
            t[state][next_state] = 0.0

    for i in range(len(X)):
        e[π[i]][X[i]] += 1

        if i < len(X) - 1:
            t[π[i]][π[i+1]] += 1

    for state in states:
        num_occurrence_e = sum(e[state].values())
        if num_occurrence_e > 0:
            for char in Σ:
                e[state][char] /= num_occurrence_e

        num_occurrence_t = sum(t[state].values())
        if num_occurrence_t > 0:
            for next_state in states:
                t[state][next_state] /= num_occurrence_t

    return t, e


# Main
iterations, X, Σ, states, t, e = read_input()

# iterations
for _ in range(iterations):
    π = viterbi_algorithm(X, Σ, states, t, e)
    t, e = viterbi_learning(X, Σ, π, states, t, e)

# output
print('\t' + '\t'.join(states))
for state in states:
    print(state, end='\t')
    # with help of https://github.com/ngaude/sandbox/blob/f009d5a50260ce26a69cd7b354f6d37b48937ee5/bioinformatics-002/bioinformatics_chapter16.py#L128
    print('\t'.join(map(lambda f: format('%.3g' % round(f, 3)) if f != 1 else '1.0', t[state].values())))

print('--------')

print('\t' + '\t'.join(Σ))
for state in states:
    print(state, end='\t')
    # with help of https://github.com/ngaude/sandbox/blob/f009d5a50260ce26a69cd7b354f6d37b48937ee5/bioinformatics-002/bioinformatics_chapter16.py#L128
    print('\t'.join(map(lambda f: format('%.3g' % round(f, 3)) if f != 1 else '1.0', e[state].values())))
