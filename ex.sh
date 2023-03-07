#!/bin/sh

cd $1/cyclone/tmp/$3
export LD_LIBRARY_PATH=$1/cyclone/
timeout 15 java -jar ../../cyclone.jar --nocolor $2
