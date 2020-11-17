#!/bin/bash

##################################
# Turning Parameters
# Default values

#TILE SIZE (MUST BE POWER OF TWO)
SPATSIZE=128
SPECSIZE=128

#BLOCK SIZE
PROJBLOCK=128
BACKBLOCK=128

#BUFFER SIZE
PROJBUFF=8
BACKBUFF=8

##################################

MPI_NUMPROC=16
OMP_NUM_THREADS=1

##################################


POSITIONAL=()
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -np)
    MPI_NUMPROC="$2"
    shift # past argument
    shift # past value
    ;;
    -nt)
    OMP_NUM_THREADS="$2"
    shift # past argument
    shift # past value
    ;;
    -SPATSIZE)
    SPATSIZE="$2"
    shift # past argument
    shift # past value
    ;;
    -SPECSIZE)
    SPECSIZE="$2"
    shift # past argument
    shift # past value
    ;;
    -PROJBLOCK)
    PROJBLOCK="$2"
    shift # past argument
    shift # past value
    ;;
    -BACKBLOCK)
    BACKBLOCK="$2"
    shift # past argument
    shift # past value
    ;;
    -PROJBUFF)
    PROJBUFF="$2"
    shift # past argument
    shift # past value
    ;;
    -BACKBUFF)
    BACKBUFF="$2"
    shift # past argument
    shift # past value
    ;;
    *)    # unknown option
    POSITIONAL+=("$1") # save it in an array for later
    shift # past argument
    ;;
esac
done
set -- "${POSITIONAL[@]}" # restore positional parameters


##################################
DATASET=$1

#I/O FILES
THEFILE=~/datasets/${DATASET}_theta.bin
SINFILE=~/datasets/${DATASET}_sinogram.bin
OUTFILE=./recon/recon_${DATASET}.bin

LOGFILE=./logs/`date +%s`.log

##################################
# Dataset Domain Size

case $DATASET in
    ADS1)
        NUMTHE=360
        NUMRHO=256
        ;;
    ADS2)
        NUMTHE=750
        NUMRHO=512
        ;;
    ADS3)
        NUMTHE=1500
        NUMRHO=1024
        ;;
    ADS4)
        NUMTHE=2400
        NUMRHO=2048
        ;;
    RDS1)
        NUMTHE=1501
        NUMRHO=2048
        ;;
    RDS2)
        NUMTHE=4501
        NUMRHO=11283
        ;;
esac

##################################
# Constant

PIXSIZE=1
NUMITER=24

##################################
# Executing

if [ -z $1 ]
then
    echo Must specify dataset !
else
    mpirun \
    -np $MPI_NUMPROC \
    -x NUMTHE=$NUMTHE \
    -x NUMRHO=$NUMRHO \
    -x PIXSIZE=$PIXSIZE \
    -x NUMITER=$NUMITER \
    -x SPATSIZE=$SPATSIZE \
    -x SPECSIZE=$SPECSIZE \
    -x PROJBLOCK=$PROJBLOCK \
    -x BACKBLOCK=$BACKBLOCK \
    -x PROJBUFF=$PROJBUFF \
    -x BACKBUFF=$BACKBUFF \
    -x THEFILE=$THEFILE \
    -x SINFILE=$SINFILE \
    -x OUTFILE=$OUTFILE \
    -x OMP_NUM_THREADS=$OMP_NUM_THREADS \
    --output-filename $LOGFILE \
    --tag-output \
    ./memxct
fi
