#!/bin/bash
export ZEPPELIN_PORT=8090
export ZEPPELIN_JAVA_OPTS="-Dspark.driver.memory=1g -Dspark.executor.memory=2g"
export MASTER="spark://spark-master:7077"
# echo "spark.jars.packages graphframes:graphframes:0.7.0-spark2.4-s_2.11" > /opt/spark/conf/spark-defaults.conf
# echo "export SPARK_HOME=/opt/spark" > /zeppelin/conf/zeppelin-env.sh
# echo "export SPARK_SUBMIT_OPTIONS=\"--packages graphframes:graphframes:0.7.0-spark2.4-s_2.11\"" >> /zeppelin/conf/zeppelin-env.sh
# echo "PYTHONPATH=$PYTHONPATH:/zeppelin/.ivy2/jars/graphframes_graphframes-0.7.0-spark2.4-s_2.11.jar" > /opt/spark/conf/spark-env.sh
# chmod +x /zeppelin/conf/zeppelin-env.sh
# chmod +x /opt/spark/conf/spark-defaults.conf
