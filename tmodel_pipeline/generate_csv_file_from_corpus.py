import sys
import os
'''
Created on Apr 25, 2015

@author: nwolfe
'''
corpus = [l.strip() for l in open(sys.argv[1]).readlines()]
count = 0
test_count = 0
train_count = 0
special_symbols = ['<s>','</s>']
csvfile = open(sys.argv[1].replace('.txt','-train.csv'),'w')
csvtest = open(sys.argv[1].replace('.txt','-test.csv'),"w")
for l in corpus:
    for s in special_symbols: l = l.replace(s,'')
    count += 1
    if(count % 10  != 0):
        csv = ",".join([str(train_count),sys.argv[1].replace('.txt','').split(os.sep)[-1],l.strip(),'\n'])
        csvfile.write(csv)
        train_count += 1
    else:
        csv = ",".join([str(test_count),sys.argv[1].replace('.txt','').split(os.sep)[-1],l.strip(),'\n'])
        csvtest.write(csv)
        test_count += 1
csvfile.close()
    
    
    
        


