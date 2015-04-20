#!/bin/sh

# -N : the name of the job
# -S : the shell you want to use
# -l : resource request list
#      nodes=1:ppn=1 : the job needs one machine and one core (ppn) from that machine
#      pmem=50mb     : the jobs needs 50MB of physical memory
#      walltime      : the maximum running time is 1 hour
# -o : the path for stdout
# -d : the working dir for the job
# -j eo : merge stdout and stderr together and dump everything to stdout
# -j oe : merge stdout and stderr together and dump everything to stderr
# janus likes -j eo
#qsub -j eo -S /bin/bash -o . -N nwolfe -l nodes=1:ppn=4,pmem=10240mb,walltime="1:00:00" -d . ./$2 
qsub -j eo -S /bin/bash -o . -N nwolfe-medtest -l nodes=1:ppn=4,pmem=10240mb,walltime="12:00:00" -d . ./$1
