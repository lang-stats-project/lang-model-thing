#!/bin/sh
# =============================================================== #
# SWITCHES
# =============================================================== #
# --------------------------------------------------------------- #
# CAREFUL! set if you want to destroy the previous set of files / config in the LOCAL_DATA_DIRECTORY
# works better if you get the conf files fresh each time...
DESTROY_OLD_CONF_FILES=false
# --------------------------------------------------------------- #
# if you want to create new ASR input for your topic modeling (recommended)
NEW_ASR_FROM_CONF_FILES=false 
# --------------------------------------------------------------- #
# CAREFUL! if you want to recreate the ASR output csv files instead of appending to the existing ones
DESTROY_OLD_ASR_CSV_FILES=false 
# --------------------------------------------------------------- #
# set if you want to create a NEW topic model and delete the topic model with the same name (recommended)
NEW_TOPIC_MODEL=true 
# --------------------------------------------------------------- #
# set if you want to predict topic distributions for new docs pointed to in $CSVTEST
TEST_TOPIC_MODEL=true 
# --------------------------------------------------------------- #
# CAREFUL! only if you want to REMOVE the old .bof files and erase them. 
DESTROY_OLD_BOF_FILES=true 
# --------------------------------------------------------------- #
# if you want to generate the .bof files to run the evaluation pipeline
NEW_BOF_FILES=true 
# --------------------------------------------------------------- #
#
# =============================================================== #
# CONFIGURE ALL TOPIC MODELING PARAMETERS 
# =============================================================== #
#
NUM_TOPICS=250
ITERATIONS=300
MIN_WORD_LENGTH=2
MIN_DOCUMENT_LENGTH=1
NUM_STOP_WORDS=1
TOP_TERMS=50
#TOPIC_MODEL_MEMORY="20480m"
TOPIC_MODEL_MEMORY="10240m"
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
OPTSTRING="Should be: \n\n\trun.sh -->\n\t\t1. [output dir for .bof files] \n\t\t2. [an .idx file w/ list of video ids to generate .bof files from] \n\t\t3. [OPTIONAL: labelset .idx file to train new topic model]\n"
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

	TEST_IDX_FILE=$2
	FILE="${TEST_IDX_FILE##*/}" 
	TEST_PREFIX="${FILE%.*}" 

fi

# --------------------------------------------------------------- #
# FILES TO TRAIN NEW TOPIC MODEL ON...
# --------------------------------------------------------------- #

MODELFILE="model" # LEAVE THIS ALONE!!!! #

if [ ! -z "$3" ]; then

	LABELSET=$3
	FILE="${LABELSET##*/}" 
	TRAIN_PREFIX="${FILE%.*}"
	rm $MODELFILE

	# --------------------------------------------------------------- #
	# THIS IS WHERE WE SET THE NAME OF THE MODEL!
	echo -n "lda-topic-model-"$TRAIN_PREFIX"-"$NUM_TOPICS >> $MODELFILE
	# --------------------------------------------------------------- #

else # nothing to train on... we just use this blank file. 

	NEW_TOPIC_MODEL=false
	NULLFILE="null.idx"
	rm $NULLFILE
	echo -n "" >> $NULLFILE
	LABELSET=$NULLFILE 

fi
if [ ! -s "$MODELFILE" ]; then

	echo -n "" >> $MODELFILE
	echo "No current topic model found! Try resetting the value in the 'model' file to the name of an existing model or train a new model."
	echo -e $OPTSTRING
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
CSVTRAIN=$TMP_MODEL"-train.csv"
CSVTEST=$TEST_PREFIX"-test.csv"
CSVCOMPOSITE=$TMP_MODEL"-"$TEST_PREFIX"-composite-train-test.csv"
TOPIC_MODEL_OUTPUT=$TMP_MODEL"-"$TEST_PREFIX"-"$NUM_TOPICS"-output.txt"
CONFIG_FILE=$TMP_MODEL"-"$TEST_PREFIX"-"$NUM_TOPICS"-config"
BOF_LIST_FILE=$TMP_MODEL"-"$TEST_PREFIX"-"$NUM_TOPICS"-bof-list.list"
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
if [ "$DESTROY_OLD_CONF_FILES" = true ]; then

	echo "Removing old .conf files..."
	cd $HOME_DIRECTORY
	cd $LOCAL_DATA_DIRECTORY
	rm -rf *
	cd $HOME_DIRECTORY
	echo "Done!"

fi
if [ "$DESTROY_OLD_ASR_CSV_FILES" = true ]; then
		
	echo "Removing old ASR files..."
	cd $HOME_DIRECTORY
	rm $CSVTRAIN
	rm $CSVTEST	
	rm $CSVCOMPOSITE
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
if [ "$NEW_ASR_FROM_CONF_FILES" = true ] ; then

	echo "Generating ASR output..."
	./get_asr_output_parallelized.py $LOCAL_DATA_DIRECTORY $LABELSET $TEST_IDX_FILE $CONF_ID_FILE_MAPPING $CSVTRAIN $CSVTEST $CSVCOMPOSITE

fi
# ================================================================================== #
# RUN TOPIC MODELING
# ================================================================================== #
if [ "$NEW_TOPIC_MODEL" = true ] ; then

	echo "Generating new topic model with "$LABELSET"..."
	java -jar -Xmx$TOPIC_MODEL_MEMORY tmt-0.4.0.jar event_topic_modeling_train.scala $MODEL $CSVTRAIN $NUM_TOPICS $ITERATIONS $MIN_WORD_LENGTH $NUM_STOP_WORDS $MIN_DOCUMENT_LENGTH

fi
# ================================================================================== #
# TEST TOPIC MODEL
# ================================================================================== #
if [ "$TEST_TOPIC_MODEL" = true ] ; then

	echo "Testing topic model "$MODEL"..."
	java -jar -Xmx$TOPIC_MODEL_MEMORY tmt-0.4.0.jar event_topic_modeling_test.scala $MODEL $CSVTEST $TOP_TERMS

fi
# =============================================================== #
# BAG OF FEATURE GENERATION
# =============================================================== #
if [ "$NEW_BOF_FILES" = true ] ; then

	echo "Running feature generation..."
	./gen_topic_model_bof.py $MODEL $CSVTEST $BOF_DIRECTORY $BOF_LIST_FILE $TEST_IDX_FILE

fi
# =============================================================== #
# FINISH
# =============================================================== #
echo "Done!"
