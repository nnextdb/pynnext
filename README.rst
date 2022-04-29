![alt text](https://d135j1zm1liera.cloudfront.net/nnext-logo-wide.png "NNext Logo Wide")

## About

NNext is a
* ⚡ blazingly fast
* 📖 source-available [[Elastic License 2.0]](https://www.elastic.co/licensing/elastic-license)
* 🔍 nearest-neighbors vector search engine

## Quick Start

Here's a quick example showcasing how you can create an index, insert vectors/documents and search it on NNext.

Let's begin by starting the NNext server via Docker:

```
docker run -p 6040:6040 -v/tmp/data:/data nnext/nnext:latest --data-dir /data --api-key=Hu52dwsas2AdxdE
```

We have a [API Client](#api-clients) in python only, but let's use it for this example.

Install the Python client for NNext:

```
pip install nnext
```

We can now initialize the client, create a `test` index


```python
import numpy as np
import nnext
from nnext import _and, _eq, _gte, _in

# Create and initialize the vector client
nnclient = nnext.Client(
    nodes=[
    {'host': 'localhost', 'port': '6040'}
  ])
```


Broadly speaking, you can create two types of indices
### 1. Simple indices
```python
n_dim = 768

# Create an vector index.
nnindex = nnclient.index.create(
    d=n_dim,
    name='test_ANN')

n_vecs = 1000
k = 5
n_queries = 10
vectors = np.random.rand(n_vecs, n_dim)

# Insert vectors into the index.
nnindex.add(vectors)

# Create a query vector set.
q_vectors = np.random.rand(n_queries, n_dim)

# Now search the vectors.
_idx, _res = nnindex.search(q_vectors, k)  # search

# The search operation returns a tuple of vectors and optionally the data
# associated with the vectors.
```

### 2. Compound indices
🚧 WIP 🚧. Not implemented.

NNext is capable of storing additional metadata related to your vectors in a rich format. In this example we will use the
[movie plots dataset from Kaggle](https://www.kaggle.com/datasets/jrobischon/wikipedia-movie-plots).
```python
nnindex = client.index.create({
  "name": "movies",
  "schema": {
      "id" : "string", #⬅ inferred primary key
      "title" : "string",
      "released_year" : "int32",
      "genre" :  "float",
      "wikipage" : "string",
      "plot" : "string",
      "rating" :  "float"
  },
  "index_type": "approximated", #⬅ indexes assumed to be approximated by default.
  "dims": n_dim
})
```


Now, let's add a vector to the collection we just created:

```python
vector = {
 "id": "124",
 "company_name": "Stark Industries",
 "num_employees": 5215,
 "country": "USA",
}

nnindex.documents.create(document)
```

Finally, let's search for the document we just indexed:

```python
q_filter = {
    _and: [
        { "Release Year": { _gte: 2015 } },
        { "Genre": { _eq: "comedy" } },
        { "actors": { _in: ["Russell Crowe"] } }
    ]
}

client.collections['companies'].documents.search(search_parameters)
```

## Contributing

### Introduction
First off, 🙏🏾 thank you for considering contributing to nnext. We value community contributions!

### How can you help?

You may already know what you want to contribute -- a fix for a bug you encountered, or a new feature your team wants to use.

If you don't know what to contribute, keep an open mind! Here's some examples of helpful contributions that mean 
less work for you
* Improving documentation
* bug triaging
* writing tutorials

Checkout [guide to contributing](https://github.com/redis/redis-py/blob/master/CONTRIBUTING.md) to learn more.


## Documentation

All NNext Server and Client documentation, including pynext integration articles and helpful recipes, can be found at:

[https://nnext.ai/docs/](https://nnext.ai/docs)
