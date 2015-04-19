import sys
import os

conf_files_dir = sys.argv[1]
local_conf_dir = sys.argv[2]
outfile = sys.argv[3]
copy_list = sys.argv[4] # an .idx file
copy_training_files = True

try:
    label_train_set = sys.argv[5] # an optional .idx file
except Exception: copy_training_files = False
     
conf_extension = ".conf"
missing = "missing_confs.idx"

# grabs all files in the conf files directory, copies them
# to a local directory...
if not os.path.isfile(outfile):
    conf_files = {}
    conf_files_dir = os.path.abspath(conf_files_dir)
    print("Entering " + conf_files_dir)
    for root, dirs, files in os.walk(conf_files_dir):
        for f in files:
            if f.endswith(conf_extension):
                filepath = os.sep.join([root,f])
                try:
                    filestuff = open(filepath).readlines()
                    for line in filestuff:
                        label = int(line.split(" ")[0].split("_")[0].strip("HVC"))
                        try:
                            test = conf_files[label]
                        except Exception:
                            conf_files[label] = filepath
                            print("HVC" + str(label) + " file: " + filepath)
                except Exception: continue
    print("Writing " + outfile + "...")
    out = open(outfile,"w")
    for c in conf_files: 
        string = ",".join([str(c),conf_files[c]])
        print("Writing " + string)
        out.write(string + "\n")
    out.close()
        
conf_files = {}
for l in open(outfile).readlines(): conf_files[int(l.split(",")[0])] = l.split(",")[1].strip()

# copy a .conf file to the local directory so we can use it. 
def copy_conf_file(f):
    fname = f.strip().split("/")[-1]
    lcd = os.path.abspath("./" + local_conf_dir)
    cmd = "cp " + f.strip() + " " + lcd + " -v"
    if not os.path.isfile(lcd + "/" + fname):
        os.system(cmd)
        
# copy a list of .conf files based on a list of ids passed to the script (.idx file)
def copy_conf_idx_list(id_list):
    missing = open(id_list.split(os.sep)[-1].replace(".idx","") + "-missing-confs.idx","w")
    print("Checking "+id_list+" file list...")
    try:
        id_list = [int(x) for x in open(id_list).readlines()]
        print("Length training set: " + str(len(id_list)))
        for l in id_list:
            try:
                test = conf_files[l]
                copy_conf_file(test)
            except Exception:
                missing.write(str(l)+"\n")
    except Exception: 
        print("File " + id_list + " not found! Script will now exit...")
        sys.exit(1)
    missing.close()
         
# copy the .idx file list == TRAINING NEW MODEL    
if copy_training_files: copy_conf_idx_list(label_train_set)

# copy the files in the .idx file list == TESTING NEW/EXISTING MODEL
print("Copying .conf files for " + copy_list + "...")
copy_conf_idx_list(copy_list)
