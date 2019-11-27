import pandas as pd

## list of files and columns
files = [
    ('ratings', 'u-1m.data', ['src','dst','Rating','Timestamp']),
    ('movies', 'u-1m.item', ['id', 'Title', 'Genres']),
    ('users', 'users.dat', ['id','Gender','Age','Occupation','Zipcode'])
]
pd_dfs = {}
dfs = {}

## read each file and asign to a key on pd_dfs dict
for name, f, columns in files:
     pd_df = pd.read_csv('/opt/spark-data/ml-1m/{}'.format(f), sep='::', names=columns)
     pd_dfs[name] = pd_df

## Transform dataframe id column to be prefixed with "user_" or "movie",
## depends on what dataset it isself.
## Also do the same thing on ratings dataset
pd_dfs['movies']['id'] = 'movie_' + pd_dfs['movies']['id'].astype(str)
pd_dfs['users']['id'] = 'user_' + pd_dfs['users']['id'].astype(str)
pd_dfs['ratings']['src'] = 'user_' + pd_dfs['ratings']['src'].astype(str)
pd_dfs['ratings']['dst'] = 'movie_' + pd_dfs['ratings']['dst'].astype(str)

## Convert files to parquet and save it
for k in pd_dfs.keys():
     print('Converting pandas {} dataframe to spark dataframe'.format(k))
     pd_df = pd_dfs[k]
     sp_df = spark.createDataFrame(pd_df)
     print('Writing parquet files')
     dfs[k] = sp_df
     sp_df.write.mode('overwrite').parquet('/opt/spark-data/{}.parquet'.format(k))


### BEGIN SAMPLE
###

## Parquet file list
files = [
    ('ratings', 'u-1m.data', ['src','dst','Rating','Timestamp']),
    ('movies', 'u-1m.item', ['id', 'Title', 'Genres']),
    ('users', 'users.dat', ['id','Gender','Age','Occupation','Zipcode'])
]


from graphframes import *

sp_dfs = {}
## Load every dataset with graphframes required format:
## * vertices needs an id named column with unique identifier for each vertice
## * edges needs at least 2 columns named src and dst especifing source and destination vertices ids
for name, f, columns in files:
     print('Reading {}...'.format(name))
     df = spark.read.parquet('/opt/spark-data/{}.parquet'.format(name))
     sp_dfs[name] = df
     df.registerTempTable(name)

## Just union users and movies ids
## Graphframes and GraphX have a limitation: Just one kind of vertice can be used with a single graph.
## So, to use different kinds of vertices, they needs to be concatenated in a single dataframe
## with different ids
ids = spark.sql('''
    select id from movies
    union
    select id from users
''')

## Creating a graph
g = GraphFrame(ids, sp_dfs['ratings'])

## Graph statistics
inDegrees = g.inDegrees
outDegrees = g.outDegrees
inDegrees.show(5)
outDegrees.show(5)

## Motif query with two users rating the same movie
chain4 = g.find("(a)-[ab]->(b); (c)-[cb]->(b)")
chain4[['a', 'b', 'c', 'cb']].show()

sp_dfs['ratings'][(sp_dfs['ratings']['src'] == 'user_1962') & (sp_dfs['ratings']['dst'] == 'movie_2433')]
sp_dfs['ratings'][(sp_dfs['ratings']['src'] == 'user_4013') & (sp_dfs['ratings']['dst'] == 'movie_2433')]

## Graphframes native Page Rank algoritmn implementation
results = g.pageRank(resetProbability=0.15, tol=0.01)
# Display resulting pageranks and final edge weights
# Note that the displayed pagerank may be truncated, e.g., missing the E notation.
# In Spark 1.5+, you can use show(truncate=False) to avoid truncation.
results.vertices.select("id", "pagerank").show()
results.edges.select("src", "dst", "weight").show()
# |user_1048|movie_1517|0.024390243902439025|
sp_dfs['ratings'][(sp_dfs['ratings']['src'] == 'user_1048') & (sp_dfs['ratings']['dst'] == 'movie_1517')].show()
