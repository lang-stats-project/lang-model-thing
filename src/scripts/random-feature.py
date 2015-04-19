#!/usr/bin/env python
'''
  generate random features for a sample experiment.
  input : [1] a document file [2] #of random features [3] file prefix
  output : tsv real-valued numbers
'''
import sys, random

out_file = open(sys.argv[3]+sys.argv[1].split('/')[-1].split('.')[0]+'.f', 'w')
print >> out_file , "\t".join([str(random.random()) for i in xrange(int(sys.argv[2]))])

