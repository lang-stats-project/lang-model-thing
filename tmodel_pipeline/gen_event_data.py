import os
import sys

# Generates the event data file used for ground truth information...
# Format: [ index, video-name, event-label, confidence, synopsis ]
# This is the same as is on the evaluation page

labelsets = sys.argv[1]
labelfile = sys.argv[2]
event_data = sys.argv[3]

directory = os.path.abspath(labelsets)
data = open(directory + "/" + labelfile).readlines()
outfile = open(event_data,"w")

# ============================================================= #
# This code is specific to the format of the labelfile!!
# ============================================================= #

data = [d.replace("\"","").strip() for d in data[1:]]
for i in range(0,len(data)):
    d = data[i].split(",")
    label = d[1]
    if d[2] == "miss": label = "NULL"
    line = str(i) + ",HVC" + d[0] + "," + label + "," + str(float(0)) + "," + d[2] + "\n"
    outfile.write(line)
     
