#!/usr/bin/env python
'''
  merges features for given folders.

  input : [1] the list of features under FEATURES/ 
  output : tsv real-valued numbers merged.BATCH_NAME.EXP_NAME
'''
import sys
import os

feature_folders = open(sys.argv[1]).readline().strip().split()

def merge_batch(batch_name):
	cmd= 'find FEATURES/' + feature_folders[0] + ' -name \*' + batch_name + '.*.f | sort | cut -d"/" -f3 > files.' + batch_name
	os.system(cmd)

	batch_merged = open('merged.'+batch_name,'w')
	for line in open('files.'+batch_name):
		fname =  line.strip()
		merged = []
		for ff in feature_folders:
			merged += open('FEATURES/'+ff+'/'+fname).readlines()[0].strip().split()
		for i,fval in enumerate(merged):
			merged[i] = str(i+1)+":"+merged[i]
		print >> batch_merged, " ".join(['0']+merged)
	os.system('rm '+'files.'+batch_name)
merge_batch('test')
