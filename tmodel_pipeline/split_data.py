import sys
import os
'''
Created on Apr 25, 2015

@author: nwolfe
'''
if __name__ == '__main__':
    directory = sys.argv[1].rstrip("/")
    fname = sys.argv[2].replace(".txt","")
    data = [l.strip() for l in open(fname + ".txt").readlines()]
    data_len = int(len(data)/20.0)
    file_count = 0
    line_count = 0
    f = open(directory + os.sep + fname + "-split" + str(file_count) + ".txt",'w')
    for l in data:
        f.write(l+"\n")
        line_count += 1
        if line_count > data_len:
            file_count += 1
            line_count = 0
            f.close()
            f = open(directory + os.sep + fname + "-split" + str(file_count) + ".txt","w")
            
    f.close()
    
    

