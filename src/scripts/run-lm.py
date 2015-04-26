#!/usr/bin/env python
'''
  generate unigram features for another baseline
  input : [1] a document file [2] lm file [3] file prefix 
  output : tsv real-valued numbers
'''
import sys, os

lm_format = 'binary'
if sys.argv[2].split('.')[1] == 'arpa':
	lm_format='arpa'

out_file = sys.argv[3]+sys.argv[1].split('/')[-1].split('.')[0]+'.f'
text_file = sys.argv[1]
lm_file = sys.argv[2]

cmd = 'echo -e "perplexity -text '+ text_file + '" | evallm -'+ lm_format + ' ' + lm_file + ' 2> /dev/null | grep Perplexity | cut -d "," -f1 | awk \'{print $3}\' >'+out_file
os.system(cmd)

