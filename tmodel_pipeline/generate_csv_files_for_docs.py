import sys
import os
from stemming.porter3 import PorterStemmer
'''
Created on Apr 25, 2015

@author: nwolfe
'''

def fix_line(line, stemmer):
    arr = []
    for word in line.split():
        word = word.lower().replace("'","").replace(".","").replace(",","")
        arr.append(stemmer.stem(word, 0, len(word)-1))
    return " ".join(arr)

def main(directory):
    superscript = open("run-all.sh","w")
    stemmer = PorterStemmer()
    count = 0
    test_count = 0
    train_count = 0
    for root, dirs, files in os.walk(directory, topdown=True):
        for f in files:
            f = os.path.join(root, f)
            print(f)
            document = " ".join([l.strip() for l in open(f).readlines()])
            special_symbols = ['<s>','</s>']
            csvfile = open(os.path.join(directory,'all-data-train.csv'),'a')
            csvtest = open(os.path.join(directory,'all-data-test.csv'),'a')
            csvall = open(os.path.join(directory,'all-data.csv'),'a')
            for s in special_symbols: document = document.replace(s,'')
            document = fix_line(document, stemmer)
            count += 1
            if(count % 10  != 0):
                csv = ",".join([str(train_count),f.replace('.txt','').split(os.sep)[-1],document.strip(),'\n'])
                csvfile.write(csv)
                csvall.write(csv)
                train_count += 1
            else:
                csv = ",".join([str(test_count),f.replace('.txt','').split(os.sep)[-1],document.strip(),'\n'])
                csvtest.write(csv)
                csvall.write(csv)
                test_count += 1
            csvfile.close()
            csvall.close()
            csvtest.close()
            #superscript.write(" ".join(["./run.sh",sys.argv[2],f,f,"\n"]))
    
if __name__ == '__main__':
    main(sys.argv[1])
    
    
        


