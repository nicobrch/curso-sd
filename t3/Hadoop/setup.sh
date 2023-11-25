#!/bin/bash

# Create directories in HDFS
hdfs dfs -mkdir /user
hdfs dfs -mkdir /user/hduser
hdfs dfs -mkdir input

# Change ownership
sudo chown -R hduser .

# Change to the 'trabajo' directory
cd trabajo

# Upload files to HDFS
hdfs dfs -put docs_1/*.txt input
hdfs dfs -put docs_2/*.txt input

# List contents of the 'input' directory in HDFS
hdfs dfs -ls input

# Run MapReduce job
mapred streaming -files mapper.py,reducer.py -input /user/hduser/input/*.txt -output hduser/outhadoop/ -mapper ./mapper.py -reducer ./reducer.py

# Retrieve results from HDFS
hdfs dfs -get /user/hduser/hduser/outhadoop/ /home/hduser/trabajo
