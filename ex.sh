#!/bin/sh

cd $1/cyclone
timeout 15 java -jar cyclone.jar --nocolor $2
