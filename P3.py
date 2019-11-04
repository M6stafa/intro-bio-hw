# -*- coding: utf-8 -*-

# Find All Occurrences of a Pattern in a String
# http://rosalind.info/problems/ba1d

import re


pattern = input()
genome = input()

indicies = [m.start() for m in re.finditer('(?={})'.format(pattern), genome)]

print(' '.join(map(str, indicies)))
