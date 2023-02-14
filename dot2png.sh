#!/bin/sh

cd $1/cyclone/trace
dot -Tpng $2 -o cyclone.png