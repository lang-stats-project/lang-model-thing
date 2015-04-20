import os
import sys
import errno
from dbg import debug
from get_asr_output import ASRProcessor
import multiprocessing

# script arguments...
local_conf_dir = sys.argv[1]
labelset = sys.argv[2]
test_idx_file = sys.argv[3]
output_training_file = sys.argv[4]
output_testing_file = sys.argv[5]
composite_train_test_file = sys.argv[6]

# WARNING! TIGHT COUPLING! #
script_name = "get_asr_output.py"
conf_ext = ".conf"
num_cores = float(multiprocessing.cpu_count()) * 20
num_files = len(os.listdir(os.path.abspath(local_conf_dir)))
chunk_size = max(int(num_files/num_cores),10)
print("Chunk size is... "+str(chunk_size))

# create dirs if they exist, ignore otherwise...
def make_dir(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

# divide data into groups of "chunk_size" files each, dispense thread to work on them.
for root, dirs, files in os.walk(local_conf_dir):
    files = [os.path.abspath(os.sep.join([root,f])) for f in files if f.endswith(conf_ext)]
    count = 0
    folder_count = 1
    temp_group = []
    for f in files:
        count += 1
        temp_group.append(f)
        if count % chunk_size == 0:
            new_path = os.sep.join([local_conf_dir,str(folder_count)])
            make_dir(new_path)
            print("created folder "+new_path+"...")
            # rename
            for t in temp_group:
                name = t.strip().split(os.sep)[-1]
                os.rename(t, new_path + os.sep + name)
            folder_count += 1
            temp_group = []
    
    # handle the leftovers which don't form a group of chunk_size...
    if count % chunk_size != 0:
        last_path = os.sep.join([local_conf_dir,str(folder_count)])
        make_dir(last_path)
        print("created folder "+last_path+"...")
        os.system("mv "+local_conf_dir+os.sep+"*"+conf_ext+" "+last_path)

    # launch Process to handle each subfolder...
    q = [] # multiproc list
    while folder_count > 0:
        subset = os.sep.join([local_conf_dir,str(folder_count)])
        folder_count += -1
        p = ASRProcessor(subset,labelset, test_idx_file,
                         output_training_file, output_testing_file, composite_train_test_file)
        q.append(p)
    
    # start all threads
    for p in q: p.start()
    
    # join all threads...
    for p in q: p.join()

# fix any duplicates that may have occurred...
def merge_duplicates_number_file(output_file):
    temp = {}
    for l in open(output_file).readlines():
        l = l.split(",")
        if len(l) > 2: 
            #print(l)
            video = l[1]
            text = ",".join(l[2:])
            try:
                test = temp[video]
                if test.strip() != text.strip():
                    temp[video] = " ".join([test.strip(),text.strip()])
            except KeyError:
                temp[video] = text
        else: debug(l)
    print("Fixing numbering on "+output_file+"...")
    count = 0
    out = []
    for t in temp:
        string = ",".join([str(count),t,temp[t]]).strip() + ",\n"
        count += 1
        out.append(string)
    outfile = open(output_file,"w")
    for o in out: outfile.write(o)
    outfile.close()

# merge duplicates in the output files...
merge_duplicates_number_file(output_training_file)
merge_duplicates_number_file(output_testing_file)
merge_duplicates_number_file(composite_train_test_file)
