#!/bin/bash

for file in {.,}*;
do
    echo "$file";
    cwl-runner "$file" data.json;
done