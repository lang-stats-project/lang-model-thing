import sys
import os
'''
EXAMPLE
author=nwolfe
experimentname=150-topic_model_smoothed_asr_bow
abstract=150 topics, bag of features topic-based word distribution SVM model
workingdir=/home/nwolfe/clean_EAGEAE_krsvm/EAGEAE_krsvm
labelset=MED14-MEDTEST-EK100
svmcvthreads=1
account=nwolfe
mode=bof
dcthreads=1
bofinputfilelist=/data/MM21/nwolfe/tmt_pipeline/list-tmt-med14-ek100.list
kernel=X2
dimensions=?
dcmethod=SSE
dctimehours=24
classifier=SVM,KR
metric=ap
matlabpath=/opt/matlab/7.12/bin/matlab
'''
mode = "bof" # may someday have to be passed to script. But it is not this day. 
config_name = open(sys.argv[1],"w")
experiment = sys.argv[2]
list_file = sys.argv[3]
label_set = sys.argv[4]
working_dir = sys.argv[5]
kernel = sys.argv[6]
dcmethod = sys.argv[7]
classifier = sys.argv[8]
dimensions = 0

# determine vector dimensions... read one .bof file
list_file = os.path.abspath(".") + os.sep + list_file 
dimensions = 0
for bof_file in open(list_file).readlines():
    bof_file = bof_file.strip()
    if os.path.isfile(bof_file) and os.path.getsize(bof_file):
        data = [int(d.split(":")[0]) for d in open(bof_file.strip()).readlines()[0].strip().split(" ")]
        dimensions = max(data)
        break

print("SVM feature vector dimensions: " + str(dimensions))

# config file parameters
print("Writing config file...")
config_name.write("author=nwolfe" + "\n")
config_name.write("experimentname=" + experiment.replace(" ","") + "\n")
config_name.write("abstract=bag of features topic-based word distribution SVM model" + "\n")
config_name.write("workingdir=" + working_dir + "\n")
config_name.write("labelset=" + label_set + "\n")
config_name.write("svmcvthreads=1" + "\n")
config_name.write("account=nwolfe" + "\n")
config_name.write("mode=" + mode + "\n")
config_name.write("dcthreads=1" + "\n")
config_name.write("bofinputfilelist=" + list_file + "\n")
config_name.write("kernel=" + kernel + "\n")
config_name.write("dimensions=" + str(dimensions) + "\n")
config_name.write("dcmethod=" + dcmethod + "\n")
config_name.write("dctimehours=24" + "\n")
config_name.write("classifier=" + classifier + "\n")
config_name.write("metric=ap" + "\n")
config_name.write("matlabpath=/opt/matlab/7.12/bin/matlab" + "\n")
config_name.close()
print("Done!")
