# Research about GraphX and Graphframes

This project contains a simple research about feature and general aspects of [Apache Spark](https://spark.apache.org/) and frameworks [GraphX](https://spark.apache.org/graphx/) and [Graphframes](http://graphframes.github.io/graphframes).

To support this initiative, a spark cluster was build on docker containers and as dataset, it uses [MovieLens](https://grouplens.org/datasets/movielens/latest/) dataset with 1M records of users ratings about different movies.

The following sections describe how to get Spark Cluster up with docker and how to test those frameworks.

## Project structure

* apps: shared folder with both spark cluster, pyspark-shell and zeppelin containing applications
* data: shared folder with both spark cluster, pyspark-shell and zeppelin containing test data
* docker: folder containing DOCKERFILES for different types of containers
  * base: base image with Java and spark
  * spark-master: image from base with spark master specific configurations
  * spark-worker: image from base with spark worker specific configurations
  * spark-submit: image from base with just spark-submit command line to dispatch spark jobs
  * zeppelin: image from apache/zeppelin:0.8.1 with spark libraries to zeppelin to work with spark
* env: Environment variables to spark cluster nodes
* spark-submit: sample spark job submition
* build-images.sh: shell script that builds docker images
* docker-compose.yml: docker compose configuration to run spark cluster
* network.sh: shell script that sets up a bridge docker network
* pyspark.sh: shell script that start a interactive docker image with pyspark prompt
* shell.sh: shell script that start a interactive docker image with bash prompt
* zeppelin.sh: shell script that start a docker image with zeppelin service

## Spark Cluster with Docker & docker-compose

There are 4 nodes or containers instances that represents Spark Cluster as follow:

* spark-master - IP: 172.18.0.2
* spark-worker-1 - IP: 172.18.0.3
* spark-worker-2 - IP: 172.18.0.4
* spark-worker-3 - IP: 172.18.0.5

Those instances have to be started with docker-compose and before extra services.

Also, there are 2 instances with tools to be possible to work with spark:

* pyspark-shell - Interactive container with pyspark shell prompt
* zeppelin - IP: Dynamic

All ports, of spark cluster and zeppelin, are exposed to localhost host machine.

### Containers Preparation

Build docker images as follow:

1. `source ./network.sh` ## Setup a new bridge network
1. `source build-images.sh` ## Build 4 images: spark-base, spark-master, spark-worker, zeppelin

### Getting cluster up and pyspark shell running

First start the cluster:

`docker-compose up --scale spark-worker=3`

This will get up master node and 3 workers with apps and data shared folders mouted at /opt/spark-apps and /opt/spark-data respectively.

Then, start pyspark-shell:

`source ./pyspark.sh`

This will get up a pyspark shell interactive docker image with graphframes package already installed and with apps and data shared folders mouted at /opt/spark-apps and /opt/spark-data respectively.

**NOTE**: To get pyspark shell up with graphframes package installed, host machine need internet access to get this package downloaded.

## Graphrames tests

To test different features of graphframes package, you can use movielens data, already loaded and transformed to parquet on folder /data

* movies.parquet: movie list
* ratings.parquet: user rating for each movie
* users.parquet: user list

Also, this folder contains the original movielens dataset on ml-1m.

File apps/graphframes_sample.py has some code to prepare movielens dataset and also to load and use this dataset with graphframes.

If you are confortable with previously imported data, just copy and paste code instructions that are after "### BEGIN SAMPLE" comment line. Otherwise, run the first fill lines with your datase.
