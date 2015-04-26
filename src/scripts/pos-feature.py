#!/usr/bin/env python
'''
  generate pos features
  input : [1] a document file [2] VOCAB [3] file prefix [4] berkeley parser [5] grammar 
  output : tsv real-valued numbers
'''
import sys, random, os
from collections import defaultdict

temp_file = sys.argv[3]+sys.argv[1].split('/')[-1].split('.')[0]+'.temp'
out_file = open(sys.argv[3]+sys.argv[1].split('/')[-1].split('.')[0]+'.f', 'w')

i2w = {0 : '<UNK>'}
d = set(['<UNK>'])
for i,line in enumerate(open(sys.argv[2])):
	w = line.strip()
	i2w[i+1] = w
	d.add(w)

V = len(i2w)

cmd='java -jar '+sys.argv[4]+' -gr '+sys.argv[5]+' -inputFile '+sys.argv[1]+'> '+temp_file
os.system(cmd)

counts = defaultdict(int)
tok = 0
for line in open(temp_file):
	if len(line) == 1:
		print
		continue

	right_p = line.strip().split(')')
	for tok_r in right_p:
		left_p = tok_r.split('(')
		for tok_l in left_p:
			token = tok_l.split()
			if len(token) == 2:
				w = token[0]
				if w not in d:
					w = '<UNK>'
				counts[w] += 1
				tok += 1.00

out_v = [0]*V
for i in xrange(V):
	w = i2w[i]
	out_v[i] = counts[w]*1.00 / tok
print >> out_file, "\t".join([str(val) for val in out_v])
os.system('rm -f '+temp_file)
