# -*- coding: utf-8 -*-

# Construct the Burrows-Wheeler Transform of a String
# http://rosalind.info/problems/ba9i


# Helper Functions
def bwtable(text):
    text_len = len(text)
    rotations = [text]
    for i in range(1, text_len):
        rotations.append(text[text_len-i:] + text[:text_len-i])
    return sorted(rotations)


def bwtransform(text):
    table = bwtable(text)

    out = []
    for s in table:
        out.append(s[-1])

    return ''.join(out)


# Main
text = input()
print(bwtransform(text))
