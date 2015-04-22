#!/usr/bin/env python
'''
  generate unigram features for another baseline
  input : [1] a document file [2] VOCAB [3] file prefix
  output : tsv real-valued numbers
'''
import sys, random
from collections import defaultdict

out_file = open(sys.argv[3]+sys.argv[1].split('/')[-1].split('.')[0]+'.f', 'w')

i2w = {}
d = set()
for i,line in enumerate(open(sys.argv[2])):
	w = line.strip()
	i2w[i] = w
	d.add(w)

V = len(i2w)

counts = defaultdict(int)
tok = 0
for line in open(sys.argv[1]):
	l = line.strip().split()
	for w in l:
		if w not in d:
			w = '<UNK>'
		counts[w] += 1
		tok += 1.00

out_v = [0]*V
for i in xrange(V):
	w = i2w[i]
	out_v[i] = counts[w]
print >> out_file, "\t".join([str(val) for val in out_v])
