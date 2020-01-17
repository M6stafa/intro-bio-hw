# -*- coding: utf-8 -*-

# Implement GibbsSampler
# http://rosalind.info/problems/ba2g


# imports
import random


# Helper Functions
def get_hamming_distance(s1, s2):
    d = 0
    for i in range(len(s1)):
        d += 1 if s1[i] != s2[i] else 0

    return d


def get_profile(motifs):
    k = len(motifs[0])
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


def get_randomly_motif(dna, profile, k):
    probs = []
    for i in range(0, len(dna) - k + 1):
        probs.append(get_motif_prob(dna[i:i+k], profile))

    i = random.choices(range(len(dna) - k + 1), k=1, weights=probs)[0]
    return dna[i:i+k]


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


# GIBBS SAMPLER
def gibbs_sampler(dnas, k, t, N):
    # randomly select k-mers Motifs = (Motif1, …, Motift) in each string from Dna
    # BestMotifs ← Motifs
    motifs = []
    for dna in dnas:
        i = random.randint(0, len(dna) - k)
        motifs.append(dna[i:i+k])
    best_motifs = motifs[:]
    best_score = get_score(best_motifs)

    # for j ← 1 to N
    for j in range(N):
        # i ← Random(t)
        i = random.randint(0, t - 1)

        # Profile ← profile matrix constructed from all strings in Motifs except for Motif_i
        profile = get_profile(motifs[:i] + motifs[i+1:])

        # Motif_i ← Profile-randomly generated k-mer in the i-th sequence
        motifs[i] = get_randomly_motif(dnas[i], profile, k)

        # if Score(Motifs) < Score(BestMotifs)
            # BestMotifs ← Motifs
        new_score = get_score(motifs)
        if new_score < best_score:
            best_motifs = motifs[:]
            best_score = new_score

    return best_motifs, best_score

# Main
k, t, N = map(int, input().split(' '))
dnas = []
for _ in range(t):
    dnas.append(input())

best_motifs = None
best_score = k * t + 1
for _ in range(50):
    new_motifs, new_score = gibbs_sampler(dnas, k, t, N)

    if new_score < best_score:
        best_motifs = new_motifs
        best_score = new_score

print('\n'.join(best_motifs))
