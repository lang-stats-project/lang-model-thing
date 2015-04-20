import sys
import os
import threading
import multiprocessing
import gc
import re  
from dbg import debug

# get numpy
sys.path.append("/home/iyu/sfep/asr_noisemes/base/lib/python2.7/site-packages")
import numpy

# ========================================================= #
# Script requires 4 arguments...
#
# 1. Directory of the TMT output folder
# 2. File used in testing the TM
# 3. output directory for the BOF files
# 4. name of the file where we'll put the list of bof files
# 5. The original .idx file so we can make blank .bof files
# ========================================================= # 
model_directory = os.path.abspath(sys.argv[1])
testing_file = sys.argv[2]
output_dir = sys.argv[3]
list_file = sys.argv[4]
test_idx_file = sys.argv[5]

feature_file_prefix = "HVC"
feature_file_ext = ".bof"
num_digits = 6
topic_term_distributions = "topic-term-distributions.csv.gz"
video_topic_distributions = testing_file.replace(".csv","") + "-document-topic-distributions.csv"
write_batch_size = 1000
num_simultaneous_processes = int(multiprocessing.cpu_count())
print("There are %d cores available... Starting %d threads..." % (num_simultaneous_processes, num_simultaneous_processes))

# ========================================================= #
# CLASS DEF: worker thread to compute .bof features on a 
# subset of the data, stores the result and prints to
# file when commanded. 
# ========================================================= #
class workerThread(threading.Thread):
    def __init__(self, asr, vtd, ttd, outdir):
        super(workerThread,self).__init__()
        self.asr_data = asr
        self.VTD = vtd
        self.TTD = ttd
        self.output_files = {} # store of processed feature files
        self.output_directory = outdir # where to write files
    # attempt to clear memory contents when done
    def __del__(self):
        print("Destroying thread...")
        del self.asr_data
        del self.TTD
        self.output_files.clear()
        del self.output_files
    # ========================================================= #    
    def run(self): self.calculate_bof_and_output()
    # ========================================================= #
    # Function def: write a buffer of files, append to list file
    # ========================================================= #
    def write_buffer_to_file(self):
        for filename in self.output_files:
            vec = self.output_files[filename]
            f = open(self.output_directory + filename,"w")
            string = ""
            for i in xrange(0,len(vec)):
                string += str(i+1) + ":" + str(vec[i]) + " "
            print("Writing file "+filename+"...")
            f.write(string)
            f.close()
    # ========================================================= #
    # Function def: normalize a vector
    # ========================================================= #
    def normalize_vec(self,vec):
        total = sum(vec)
        vec = [v/total for v in vec]
        return vec
    # ========================================================= #
    # get the video word distribution, which will be the dot 
    # product of multiplying the video topic distribution by 
    # the topic word distribution, or [n x t] * [t x v], 
    # resulting in a matrix which is [n x v], where n is the 
    # number of videos (documents), and v is the number of words
    # in the vocabulary
    # ========================================================= #    
    def calculate_bof_and_output(self):
        print("Calculating video word distribution and generating SVM feature vectors...")
        video_word_distributions = numpy.dot(self.VTD, self.TTD)
        del self.VTD # free up the memory...
        for i in xrange(0,len(self.asr_data)):
            video = self.asr_data[i][1] 
            vec = video_word_distributions[i].tolist()
            # fill the buffer
            if not numpy.isnan(vec[0]):
                self.output_files[video + feature_file_ext] = self.normalize_vec(vec)
            else: self.output_files[video + feature_file_ext] = []
        # call the print method
        self.write_buffer_to_file()

# --------------------------------------------------------- #
# ========================================================= #        
# PROGRAM START...
# ========================================================= #
# --------------------------------------------------------- # 
print("Loading video ASR data...")
asr_data_list = [str(l).strip().split(",") for l in open(testing_file).readlines()]

print("Creating blank .bof files...")
idx_files = [feature_file_prefix + idx.strip().zfill(num_digits) + feature_file_ext for idx in open(test_idx_file).readlines()]

# fix up output dir variable...
output_dir = re.sub('\/$','',output_dir) 
if os.path.isabs(output_dir): output_dir = output_dir + os.sep
else: output_dir = os.path.abspath(".") + os.sep + output_dir + os.sep
for f in idx_files:
    bof_file = open(output_dir + f,"a")
    bof_file.write("")
    bof_file.close()


# ========================================================= #
# get the topic word distribution, which is [t x v], where
# t is the number of topics and v is the size of the vocab
# on which the topics are built...
# ========================================================= # 
print("Loading topic word distribution...")
for root, dirs, files in os.walk(model_directory):
    last_iter = max(dirs)
    f = os.sep.join([model_directory, last_iter, topic_term_distributions])
    f = os.path.abspath(f)
    if not os.path.isfile(f.strip(".gz")):
        os.system("gunzip -c " + f + " > " + f.strip(".gz"))
    topic_term_distributions = [[float(x) for x in l.strip().split(",")] for l in open(f.strip(".gz")).readlines()]
    break

# ========================================================= #
# get video topic distribution, which is [n x t], where n
# is the number of videos (documents) and t is the number of 
# topics we are modeling... 
# ========================================================= # 
print("Loading video topic distribution...")
f = os.sep.join([model_directory,video_topic_distributions])
video_topic_distributions = [[float(x) for x in l.strip().split(",")[1:]] for l in open(f).readlines()]

q = [] # process queue
asr_data = []
vtd_buffer = []
last_index = len(asr_data_list)-1
print("Here we go...")
for i in xrange(len(asr_data_list)):
   
    # check if we've already done this computation, i.e.
    # a .bof file already exists...
    video = asr_data_list[i][1]
    fname = output_dir.strip("./") + os.sep + video + feature_file_ext
    if not os.path.isfile(fname): # file exists!
        
        # fill buffers...
        asr_data.append(asr_data_list[i]) 
        vtd_buffer.append(video_topic_distributions[i])
    
    else: print(video + feature_file_ext + " already exists! Skipping...")
        
    # free memory in the arrays as we go...
    asr_data_list[i] = None
    video_topic_distributions[i] = None
    
    # create worker thread batches based on batch size
    if asr_data and len(asr_data) % write_batch_size == 0 or i == last_index:
        worker = workerThread(asr_data, vtd_buffer, topic_term_distributions, output_dir)
        q.append(worker)
        asr_data = []
        vtd_buffer = []

# run threads in batches...
running = []
count = 0
while q:
    count += 1
    worker = q.pop()
    print("Starting process " + str(count) + " with " + str(write_batch_size) + " files...")
    worker.start()
    running.append(worker)
    if count % num_simultaneous_processes == 0 or len(q) == 0:
        print("Writing thread batch to file...")
        for r in running: r.join()
        while running:
            wkr = running.pop()
            del wkr
        gc.collect()

print("Generating .bof list file...")
os.system("find " + output_dir + "*" + feature_file_ext + " > " + list_file)

print("Done generating bag of feature files!")
    
    

