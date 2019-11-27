#!/bin/bash
local_path=`pwd`
echo $local_path

docker run -it --network docker-spark-cluster_spark-network --mount type=bind,src=$local_path/data,dst=/opt/spark-data --mount type=bind,src=$local_path/apps,dst=/opt/spark-apps spark-base:latest /spark/bin/pyspark --master spark://spark-master:7077 --packages graphframes:graphframes:0.7.0-spark2.4-s_2.11
