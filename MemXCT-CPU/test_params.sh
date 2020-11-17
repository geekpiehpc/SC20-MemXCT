#!/bin/bash

for SPATSIZE in 64 128 256
do
for SPECSIZE in 64 128 256
do
for PROJBLOCK in 64 128 256
do
for BACKBLOCK in 64 128 256
do
for PROJBUFF in 8 12 16
do
for BACKBUFF in 8 12 16
do

echo RUNNING $SPATSIZE $SPECSIZE $PROJBLOCK $BACKBLOCK $PROJBUFF $BACKBUFF

./run.sh \
-SPATSIZE $SPATSIZE \
-SPECSIZE $SPECSIZE \
-PROJBLOCK $PROJBLOCK \
-BACKBLOCK $BACKBLOCK \
-PROJBUFF $PROJBUFF \
-BACKBUFF $BACKBUFF \
ADS3 1>/dev/null

done
done
done
done
done
done
