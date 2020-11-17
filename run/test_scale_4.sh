#!/bin/bash

for TILESIZE in 128
do
for BLOCKSIZE in 128
do
for BUFFSIZE in 8
do
for DATASET in ADS1 ADS2
do
for NP in `seq 32 -1 1`
do

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

DATASET_FULL=${DATASET}_${NP}

NUMTHE=`echo "$NUMTHE $NP" | awk '{ print( int( $1 * ($2 ^ (1/3)) ) ); }'`
NUMRHO=`echo "$NUMRHO $NP" | awk '{ print( int( $1 * ($2 ^ (1/3)) ) ); }'`

# echo "RUNNING $TILESIZE $BLOCKSIZE $BUFFSIZE $NP $DATASET_FULL ($NUMTHE x $NUMRHO)"

./run.sh \
-np $NP \
-nt 1 \
--hosts ib1,ib2 \
-SPATSIZE $TILESIZE \
-SPECSIZE $TILESIZE \
-PROJBLOCK $BLOCKSIZE \
-BACKBLOCK $BLOCKSIZE \
-PROJBUFF $BUFFSIZE \
-BACKBUFF $BUFFSIZE \
-NUMITER 30 \
-SIZE $NUMTHE $NUMRHO \
$DATASET_FULL --intel -v -- -ppn=1

done
done
done
done
done
