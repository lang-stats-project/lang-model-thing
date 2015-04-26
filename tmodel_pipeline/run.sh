#!/bin/sh
# =============================================================== #
# SWITCHES
# =============================================================== #
# --------------------------------------------------------------- #
# if you want to create new ASR input for your topic modeling (recommended)
NEW_CSV_FILE=true	 
# --------------------------------------------------------------- #
# CAREFUL! if you want to recreate the ASR output csv files instead of appending to the existing ones
DESTROY_OLD_ASR_CSV_FILES=true
# --------------------------------------------------------------- #
# set if you want to create a NEW topic model and delete the topic model with the same name (recommended)
NEW_TOPIC_MODEL=false 
# --------------------------------------------------------------- #
# set if you want to predict topic distributions for new docs pointed to in $CSVTEST
TEST_TOPIC_MODEL=false 
# --------------------------------------------------------------- #
# CAREFUL! only if you want to REMOVE the old .bof files and erase them. 
DESTROY_OLD_BOF_FILES=false 
# --------------------------------------------------------------- #
# if you want to generate the .bof files to run the evaluation pipeline
NEW_BOF_FILES=false 
# --------------------------------------------------------------- #
#
# =============================================================== #
# CONFIGURE ALL TOPIC MODELING PARAMETERS 
# =============================================================== #
#
NUM_TOPICS=50
ITERATIONS=100
MIN_WORD_LENGTH=2
MIN_DOCUMENT_LENGTH=1
NUM_STOP_WORDS=1
TOP_TERMS=25
TOPIC_MODEL_MEMORY="20480m"
#TOPIC_MODEL_MEMORY="10240m"
#TOPIC_MODEL_MEMORY="32768m" 
#
# --------------------------------------------------------------- #
# location of all .conf files...
# --------------------------------------------------------------- #
#
LOCAL_DATA_DIRECTORY="data"
#
#
#
#
#
#
#
# --------------------------------------------------------------- #
# =============================================================== #
# =============================================================== #
# ===============                                ================ #
# ===============  LEAVE THE STUFF BELOW ALONE!  ================ #
# ===============                                ================ #
# =============================================================== #
# =============================================================== #
#
#
#
#
#
#
# This is the output directory for the .bof generation...
OPTSTRING="Should be: \n\n\trun.sh -->\n\t\t1. [output dir for .bof files] \n\t\t2. [an .idx file w/ list of video ids to generate .bof files from] \n\t\t3. [OPTIONAL: TRAIN_FILE .idx file to train new topic model]\n"
#
# --------------------------------------------------------------- #
# DIRECTORY TO WRITE .BOF FILES OUT TO...
# --------------------------------------------------------------- #
if [ -z "$1" ]; then

	echo "Output directory for .bof files not specified! "
	echo -e $OPTSTRING
	echo "Script will now exit..."
	exit 1

else

	BOF_DIRECTORY=$1

fi
# --------------------------------------------------------------- #
# FILES TO TEST TOPIC MODEL ON...
# --------------------------------------------------------------- #
# This is a list of video ids in an .idx file...

if [ -z "$2" ]; then

	echo "List of test video ids not specified! "
	echo -e $OPTSTRING
	echo "Script will now exit..."
	exit 1

else

	TEST_FILE=$2
	FILE="${TEST_FILE##*/}" 
	TEST_PREFIX="${FILE%.*}" 

fi

# --------------------------------------------------------------- #
# FILES TO TRAIN NEW TOPIC MODEL ON...
# --------------------------------------------------------------- #

MODELFILE="model" # LEAVE THIS ALONE!!!! #

if [ ! -z "$3" ]; then

	TRAIN_FILE=$3
	FILE="${TRAIN_FILE##*/}" 
	TRAIN_PREFIX="${FILE%.*}"
	rm $MODELFILE

	# --------------------------------------------------------------- #
	# THIS IS WHERE WE SET THE NAME OF THE MODEL!
	echo "lda-topic-model-"$TRAIN_PREFIX"-"$NUM_TOPICS >> $MODELFILE
	echo $MODELFILE
	# --------------------------------------------------------------- #
fi
if [ ! -s "$MODELFILE" ]; then

	echo "" >> $MODELFILE
	echo "No current topic model found! Try resetting the value in the 'model' file to the name of an existing model or train a new model."
	echo -e :q$OPTSTRING
	echo "Script will now exit..."
	exit 1

fi
# ----------------------- #
MODEL=$(head -1 $MODELFILE)
# ----------------------- #
#
# =============================================================== #
# LEAVE STUFF BELOW HERE ALONE UNLESS YOU KNOW WHAT YOU ARE DOING. 
# =============================================================== #
#
# (HERE BE DRAGONS)
#
HOME_DIRECTORY=$(pwd)
TMP_MODEL="${MODEL%-*}"
NUM_TOPICS="${MODEL##*-}" # reassign! 
CSVTRAIN=$TRAIN_PREFIX"-train.csv"
CSVTEST=$TEST_PREFIX"-test.csv"
TOPIC_MODEL_OUTPUT=$TMP_MODEL"-"$TEST_PREFIX"-"$NUM_TOPICS"-output.txt"
BOF_LIST_FILE=$TMP_MODEL"-"$TEST_PREFIX"-"$NUM_TOPICS"-bof-list.list"
echo "HOME DIRECTORY: "$HOME_DIRECTORY
echo "TMP_MODEL: "$TMP_MODEL
echo "NUM_TOPICS: "$NUM_TOPICS
echo "CSVTRAIN: "$CSVTRAIN
echo "CSVTEST: "$CSVTEST
echo "TOPIC_MODEL_OUTPUT: "$TOPIC_MODEL_OUTPUT
echo "BOF_LIST_FILE: "$BOF_LIST_FILE
#
#
# =============================================================== #
# START
# =============================================================== #
#
# ...just in case...
chmod +x *.py
mkdir $LOCAL_DATA_DIRECTORY
mkdir $BOF_DIRECTORY
#
# --------------------------------------------------------------- #
#
if [ "$DESTROY_OLD_ASR_CSV_FILES" = true ]; then
		
	echo "Removing old ASR files..."
	cd $HOME_DIRECTORY
	rm -rf $LOCAL_DATA_DIRECTORY
	mkdir $LOCAL_DATA_DIRECTORY
	rm $CSVTRAIN
	rm $CSVTEST	
	echo "Done!"

fi
if [ "$NEW_TOPIC_MODEL" = true ] ; then

	echo "Cleaning up old topic model resources..."
	cd $HOME_DIRECTORY
	rm *term-counts.cache.*
	rm -rf $MODEL
	echo "Done!"

fi 
if [ "$DESTROY_OLD_BOF_FILES" = true ] ; then

	echo "Removing old .bof files..."
	cd $HOME_DIRECTORY
	rm $BOF_LIST_FILE
	cd $BOF_DIRECTORY
	rm *.bof
	cd $HOME_DIRECTORY
	echo "Done!"

fi
# Just to be safe...
cd $HOME_DIRECTORY

# =============================================================== #
# THIS READS ALL OF YOUR .CONF FILES AND GENERATES CSV FILES WITH
# VIDEO NAMES AND CONSOLIDATED ASR OUTPUT FROM .CONF FILES. MAKE
# SURE YOU'RE POINTING TO THE RIGHT DIRECTORY AND BE PATIENT --
# THIS ALSO DOES THE PORTER STEMMING. 
#
# Generates:
#
# 1.) training.csv
# 2.) testing.csv
# 3.) composite-train-test.csv
# =============================================================== #
if [ "$NEW_CSV_FILE" = true ] ; then

	echo "Generating output..."
	python split_data.py $LOCAL_DATA_DIRECTORY $TRAIN_FILE
	python generate_csv_file_from_corpus.py $LOCAL_DATA_DIRECTORY $BOF_DIRECTORY

fi
# ================================================================================== #
# RUN TOPIC MODELING
# ================================================================================== #
if [ "$NEW_TOPIC_MODEL" = true ] ; then

	echo "Generating new topic model with "$TRAIN_FILE"..."
	java -jar -Xmx$TOPIC_MODEL_MEMORY tmt-0.4.0.jar event_topic_modeling_train.scala $MODEL $LOCAL_DATA_DIRECTORY/$CSVTRAIN $NUM_TOPICS $ITERATIONS $MIN_WORD_LENGTH $NUM_STOP_WORDS $MIN_DOCUMENT_LENGTH

fi
# ================================================================================== #
# TEST TOPIC MODEL
# ================================================================================== #
if [ "$TEST_TOPIC_MODEL" = true ] ; then

	echo "Testing topic model "$MODEL"..."
	java -jar -Xmx$TOPIC_MODEL_MEMORY tmt-0.4.0.jar event_topic_modeling_test.scala $MODEL $LOCAL_DATA_DIRECTORY/$CSVTEST $TOP_TERMS

fi
echo "Done!"
exit 0
# =============================================================== #
# BAG OF FEATURE GENERATION
# =============================================================== #
if [ "$NEW_BOF_FILES" = true ] ; then

	echo "Running feature generation..."
	#./gen_topic_model_bof.py $MODEL $CSVTEST $BOF_DIRECTORY $BOF_LIST_FILE $TEST_FILE

fi
# =============================================================== #
# FINISH
# =============================================================== #
echo "Done!"
