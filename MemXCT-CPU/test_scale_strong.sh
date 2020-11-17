#!/bin/bash

for TILESIZE in 32
do
for BLOCKSIZE in 128
do
for BUFFSIZE in 8
do
for NP in `seq 16 -1 1`
do
for DATASET in ADS1
do

# echo RUNNING $TILESIZE $BLOCKSIZE $BUFFSIZE $NP $DATASET

./run.sh \
-np $NP \
-nt 1 \
--hosts ib2,ib1 \
-SPATSIZE $TILESIZE \
-SPECSIZE $TILESIZE \
-PROJBLOCK $BLOCKSIZE \
-BACKBLOCK $BLOCKSIZE \
-PROJBUFF $BUFFSIZE \
-BACKBUFF $BUFFSIZE \
-NUMITER 30 \
$DATASET -v

done
done
done
done
done
