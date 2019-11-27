#!/bin/bash
local_path=`pwd`
echo $local_path
docker run -it --network docker-spark-cluster_spark-network --mount type=bind,src=$local_path/data,dst=/opt/spark-data --mount type=bind,src=$local_path/apps,dst=/opt/spark-apps spark-base:latest /bin/bash
