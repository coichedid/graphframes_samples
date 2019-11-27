#!/bin/bash
local_path=`pwd`
echo $local_path
docker run -it -p 8090:8090 --network docker-spark-cluster_spark-network --mount type=bind,src=$local_path/data/zeppelin,dst=/zeppelin/data --mount type=bind,src=$local_path/apps/zeppelin/notebook,dst=/zeppelin/notebook --mount type=bind,src=$local_path/apps/zeppelin/logs,dst=/zeppelin/logs zeppelin:latest /bin/bash
