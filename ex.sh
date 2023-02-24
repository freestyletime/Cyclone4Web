#!/bin/sh

cd $1/cyclone
timeout 30 java -jar cyclone.jar --nocolor $2
