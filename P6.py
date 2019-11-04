# -*- coding: utf-8 -*-

# Find Frequent Words with Mismatches and Reverse Complements
# http://rosalind.info/problems/ba1j

from queue import Queue


class Node:
    def __init__(self):
        self.count = 0
        self.childs = {
            'A': None,
            'C': None,
            'G': None,
            'T': None,
        }

class KMers:
    def __init__(self, max_mismatch):
        self.max_mismatch = max_mismatch

        self.root = Node()
        self.kmers = {}
        self.max_count = -1

    def add_word(self, word):
        word_length = len(word)
        branches = Queue()
        # each element contains: (node, created word, remaining mismatch)
        branches.put((self.root, '', self.max_mismatch))

        while not branches.empty():
            node, c_word, rem_mismatch = branches.get()

            if len(c_word) == word_length:
                self.inc_node_count(node, c_word)
            else:
                for child in node.childs.keys():
                    is_match = child == word[len(c_word)]
                    if node.childs[child] is None:
                        node.childs[child] = Node()

                    if is_match or (not is_match and rem_mismatch > 0):
                        branches.put((node.childs[child], c_word + child, rem_mismatch if is_match else rem_mismatch - 1))

    def inc_node_count(self, node, word):
        node.count += 1

        if node.count > self.max_count:
            self.max_count = node.count
            self.kmers = { word: True }
        if node.count == self.max_count:
            self.kmers[word] = True

complement = {
    'A': 'T',
    'C': 'G',
    'G': 'C',
    'T': 'A',
}

def reverse_complement(genome):
    rc = ''
    for i in range(len(genome) - 1, -1, -1):
        rc += complement[genome[i]]

    return rc

# main
genome = input()
k, max_mismatch = map(int, input().split())
kmers = KMers(max_mismatch)

for i in range(len(genome) - k + 1):
    word = genome[i:i+k]
    kmers.add_word(word)
    kmers.add_word(reverse_complement(word))

print(' '.join(kmers.kmers.keys()))
