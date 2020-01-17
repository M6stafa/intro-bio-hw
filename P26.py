# -*- coding: utf-8 -*-

# Implement the Viterbi Algorithm
# http://rosalind.info/problems/ba10c


# imports
import math


# Main
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

# Viterbi Algorithm
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

print(π[::-1])
