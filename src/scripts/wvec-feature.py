#!/usr/bin/env python
'''
  generate unigram features for another baseline
  input : [1] a list of files [2] word vector file [3] file prefix
  output : tsv real-valued numbers
'''
import sys, random, gzip
import numpy as np
from collections import defaultdict



v = {}
UNK='*unknown*'
for line in gzip.open(sys.argv[2]):
	l = line.strip().split()
	token = l[0].lower()
	vec = np.asarray([float(val) for val in l[1:]])
	v[token] = vec


for line in open(sys.argv[1]):
	fname = line.strip()
	out_file = open(sys.argv[3]+fname.split('/')[-1].split('.')[0]+'.f', 'w')

	avg_vec = np.zeros(v[UNK].shape)
	tok = 0
	unk = 0
	for line in open(fname):
		l = line.strip().split()
		for w in l:
			w = w.lower()
			if w == "<s>" or w == "</s>":
				continue
			if w not in v:
				unk +=1
				w = UNK
			avg_vec = avg_vec + v[w]
			tok += 1

	avg_vec = avg_vec / tok
	print >> out_file, "\t".join([str(val) for val in avg_vec])
