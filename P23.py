# -*- coding: utf-8 -*-

# Implement RandomizedMotifSearch
# http://rosalind.info/problems/ba2f


# imports
import random


# Helper Functions
def get_hamming_distance(s1, s2):
    d = 0
    for i in range(len(s1)):
        d += 1 if s1[i] != s2[i] else 0

    return d


def get_profile(motifs):
    profile = [{'A': 1, 'C': 1, 'G': 1, 'T': 1} for _ in range(k)]
    for i in range(k):
        for motif in motifs:
            profile[i][motif[i]] += 1
        chars_sum = sum(profile[i].values())
        for char in profile[i].keys():
            profile[i][char] /= chars_sum

    return profile


def get_motif_prob(motif, profile):
    prob = 1
    for i in range(len(motif)):
        prob *= profile[i][motif[i]]
    return prob


def get_consensus(profile):
    consensus = [None] * len(profile)
    for i in range(len(profile)):
        consensus[i] = max(profile[i], key=profile[i].get)

    return ''.join(consensus)


def get_score(motifs, profile=None):
    profile = profile or get_profile(motifs)
    consensus = get_consensus(profile)

    score = 0
    for motif in motifs:
        score += get_hamming_distance(motif, consensus)

    return score


# RANDOMIZED MOTIF SEARCH
def RMS(dnas, k, t):
    # randomly select k-mers Motifs = (Motif1, …, Motift) in each string from Dna
    # BestMotifs ← Motifs
    best_motifs = []
    for dna in dnas:
        i = random.randint(0, len(dna) - k)
        best_motifs.append(dna[i:i+k])
    best_score = get_score(best_motifs)

    # while forever
    while True:
        # Profile ← Profile(Motifs)
        # init with 1 because of the pseudocounts
        profile = get_profile(best_motifs)

        # Motifs ← Motifs(Profile, Dna)
        motifs = [None for _ in range(t)]
        motif_probs = [0 for _ in range(t)]
        for dna_i, dna in enumerate(dnas):
            for i in range(0, len(dna) - k + 1):
                motif_prob = get_motif_prob(dna[i:i+k], profile)
                if motif_prob > motif_probs[dna_i]:
                    motifs[dna_i] = dna[i:i+k]
                    motif_probs[dna_i] = motif_prob

        # if Score(Motifs) < Score(BestMotifs)
        #     BestMotifs ← Motifs
        # else
        #     return BestMotifs
        new_score = get_score(motifs)
        if new_score < best_score:
            best_score = new_score
            best_motifs = motifs
        else:
            return best_motifs, best_score


# Main
k, t = map(int, input().split(' '))
dnas = []
for _ in range(t):
    dnas.append(input())

best_motifs = None
best_score = k * t + 1
for _ in range(1000):
    new_motifs, new_score = RMS(dnas, k, t)

    if new_score < best_score:
        best_motifs = new_motifs
        best_score = new_score

print('\n'.join(best_motifs))
