# get all asr from the folders in this document
import re
import os
from stemming.porter3 import PorterStemmer
import threading
from multiprocessing import Lock

# ================================= #
class ASRProcessor(threading.Thread):
	video_prefix = "HVC"
	conf_ext = ".conf"
	num_digits = 6
	training = {}
	lock = Lock()
	# list of janus outputs that do not correspond to words
	non_words = ['+noise+','+breath+','+filler+','mhm']
	
	# ============================================ #	
	def __init__(self,lcd,ls,tif,otrain,otest,comp):
		super(ASRProcessor,self).__init__()
		
		# INSTANCE VARIABLES...
		self.local_conf_dir = lcd
		self.labelset = ls
		self.test_idx_file = tif # REQUIRED PARAMETER...
		self.stemmer = PorterStemmer()
		
		# CLASS VARIABLES
		self.train_file = open(otrain,"a")
		self.test_file = open(otest,"a")
		self.composite_file = open(comp,"a")
		
		# empty arrays...
		self.video_asr_map = {}
		self.asr_data = []
		self.evl = {}
		self.used = {}
		
		# training set
		for x in open(self.labelset).readlines(): 
			ASRProcessor.training[int(x.strip())] = x
			
	# ============================================ #
	def strip_chars(self,string):
		return re.sub('[{(0123456789._!?)}]',' ',string).replace('"','').lower().split()
	
	# ============================================ #	
	def do_stemming(self, key):
		werds = self.video_asr_map[key]
		for i in range(0,len(werds)):
			werds[i] = self.stemmer.stem(werds[i],0,len(werds[i])-1)
		self.video_asr_map[key] = werds
			
	# ============================================ #
	def sync_write(self,output_file,data): output_file.write(data)
		
	# ============================================ #
	# THREAD RUN METHOD
	def run(self): 
		print("Dispatching worker thread on "+self.local_conf_dir+"...")
		# ============================================ #
		# get data for evaluation set
		for idx in open(self.test_idx_file).readlines():
			try:
				idx = int(idx.strip())
				self.evl[idx] = idx # evaluation list...
				fullpath = os.sep.join([self.local_conf_dir,f])
				if os.path.isfile(fullpath):
					try:
						test = self.used[f] # already seen this file
						#print("Already seen: "+test+"...")
					except KeyError:
						self.used[f] = f
						print("ID "+str(idx)+" found in "+fullpath+"...")
						for line in open(fullpath).readlines():
							# ----------------- #
							self.asr_data.append(line)
							# ----------------- #
			except KeyError: continue
			
		# ============================================ #	
		# get all ASR data if we're training a new model...
		if ASRProcessor.training: # will be false if empty...
			for root, dirs, files in os.walk(self.local_conf_dir):
				for x in self.used.keys():files.remove(x)
				for f in files:
					if f.endswith(ASRProcessor.conf_ext):
						print("Loading data from "+f+"...")
						# ----------------------------------------------- #
						self.asr_data += open(os.sep.join([root,f])).readlines()
						# ----------------------------------------------- #
						
		# ============================================ #				
		print("Cleaning up data...")
		for a in self.asr_data:
			a = a.split()
			#debug(a)
			video = a[0].split("_")[0]
			del a[0]
			words = []
			for item in a:
				item = self.strip_chars(item)
				for i in item: 
					if not i in ASRProcessor.non_words:
						words.append(i.strip())
			#debug(words)
			try:
				v = self.video_asr_map[video]
			except KeyError:
				self.video_asr_map[video] = []
		
			# add vocab words	
			for w in words: self.video_asr_map[video].append(w)
			#debug("Cleaned: " + ",".join(words))
			#debug(video_asr_map[video])
			
		# ============================================ #
		# DO PORTER STEMMING
		# ============================================ #
		print("Doing porter stemming...")
		for k in self.video_asr_map.keys(): self.do_stemming(k)
		
		# ============================================ #
		# print shit to f...	
		print("Printing ASR output to file...")
		ASRProcessor.lock.acquire()
		train_count =  0
		test_count = 0
		vks = self.video_asr_map.keys()
		for i in range(0,len(vks)):
			vid = vks[i]
			index = int(vid.strip(ASRProcessor.video_prefix))
			terms = self.video_asr_map[vid]
			vid = ASRProcessor.video_prefix + str(index).zfill(self.num_digits)
			data = str(i) + "," + vid + "," + " ".join(terms) + "\n"
			self.sync_write(self.composite_file, data)
			try:
				# If the line comes from the evaluation set...
				test = self.evl[index]
				#print(test)
				line = str(test_count)
				test_count += 1
				line = line + "," + vid + "," + " ".join(terms) + "\n"
				self.sync_write(self.test_file, line)
			except Exception: pass
			try:
				# If the line comes from the training set...
				train = self.training[index]
				#print(train)
				line = str(train_count)
				train_count += 1
				line = line + "," + vid + "," + " ".join(terms) + "\n"
				self.sync_write(self.train_file, line)
			except Exception: pass
		
		# close the streams
		self.train_file.close()
		self.test_file.close()
		self.composite_file.close()
		ASRProcessor.lock.release()
		
		# ============================================ #
		print("Cleaning up subfolders...")
		os.system("mv "+self.local_conf_dir+os.sep+"*.conf "+self.local_conf_dir.split(os.sep)[0]+" && rmdir "+self.local_conf_dir)
		# ============================================ #
		# END RUN METHOD
		# ============================================ #
		
		
			
			
			
			
			
			
			
			
			
			
			
			
				
			
			
			
			
			
			
			
			
			
			
			
