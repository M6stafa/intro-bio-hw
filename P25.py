# -*- coding: utf-8 -*-

# Compute the Probability of an Outcome Given a Hidden Path
# http://rosalind.info/problems/ba10b


# Main
X = input()
input()
Σ = input().split('\t')
input()
π = input()
input()
states = input().split('\t')
input()
input()
emission_matrix = {}
for state in states:
    probs = list(map(float, input().split('\t')[1:]))
    emission_matrix[state] = {}
    for i in range(len(probs)):
        emission_matrix[state][Σ[i]] = probs[i]

Pr_x_π = 1
for i in range(len(X)):
    Pr_x_π *= emission_matrix[π[i]][X[i]]

print(Pr_x_π)
