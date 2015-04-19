#!/usr/bin/env python
'''
  merges features for given folders.

  input : [1] the list of features under FEATURES/ [2] experiment name EXP_NAME [3] batch name {train | dev | test}
  output : tsv real-valued numbers merged.BATCH_NAME.EXP_NAME
'''
import sys
import os

feature_folders = open(sys.argv[1]).readline().strip().split()
EXP_NAME = sys.argv[2]
labels = {'fake' : '0', 'real' : '1'}

def merge_batch(batch_name):
	cmd='find FEATURES/'+feature_folders[0]+' -name \*'+batch_name+'.*.f | sort | cut -d"/" -f3 > files.'+batch_name+'.'+ EXP_NAME
	os.system(cmd)

	batch_merged = open('merged.'+batch_name+'.'+EXP_NAME,'w')
	for line in open('files.'+batch_name+'.'+ EXP_NAME):
		fname =  line.strip()
		merged = []
		for ff in feature_folders:
			merged += open('FEATURES/'+ff+'/'+fname).readlines()[0].strip().split()
		for i,fval in enumerate(merged):
			merged[i] = str(i+1)+":"+merged[i]
		print >> batch_merged, " ".join([labels[fname.split('.')[1]]]+merged)
	os.system('rm '+'files.'+batch_name+'.'+ EXP_NAME)
merge_batch(sys.argv[3])
