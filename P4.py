# -*- coding: utf-8 -*-

# Find the Most Frequent Words in a String
# http://rosalind.info/problems/ba1b

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
    def __init__(self):
        self.root = Node()
        self.kmers = {}
        self.maxCount = -1

    def add_word(self, word):
        node = self.root

        for char in word:
            if node.childs[char] is None:
                node.childs[char] = Node()

            node = node.childs[char]

        node.count += 1

        if node.count > self.maxCount:
            self.maxCount = node.count
            self.kmers = { word: True }
        if node.count == self.maxCount:
            self.kmers[word] = True


genome = input()
k = int(input())
kmers = KMers()

for i in range(len(genome) - k + 1):
    kmers.add_word(genome[i:i+k])

print(' '.join(kmers.kmers.keys()))
