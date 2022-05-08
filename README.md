
# <a href="https://nnext.ai/"><img src="https://d135j1zm1liera.cloudfront.net/nnext-logo-wide.png" height="100" alt="Apollo Client"></a>

## About

This repository houses the source code for pynnext, the python client associated with NNext server.

NNext is a
* ⚡ blazingly fast
* 📖 source-available [[Elastic License 2.0]](https://www.elastic.co/licensing/elastic-license)
* 🔍 nearest-neighbors vector search engine

<a href="https://tiny.one/nnext-slk-comm-gh"><img src="https://img.shields.io/badge/chat-slack-orange.svg?logo=slack&style=flat"></a>
<a href="https://twitter.com/intent/follow?screen_name=nnextai"><img src="https://img.shields.io/badge/Follow-nnextai-blue.svg?style=flat&logo=twitter"></a>

[Installation](#installation) |  [Quick Start](#quick-start) | [Documentation](#documentation) | [Contributing](#contributing)

## Installation
You will need to setup and run an NNext server to utilize this client, or [outsource server management to someone else](https://nnext.ai).
For detailed server installation instructions, please see the [nnext repo](https://github.com/nnext-ai/nnext).

To install the pynnext client, activate a virtual environment, and install via pip:

1. In editable mode from source:
```zsh
git clone https://github.com/nnext-ai/pynnext
cd pynnext
pip install -e .
```

or 

2. From PyPI:

```zsh
pip install nnext
```

## Quick Start

Here's a quick example showcasing how you can create an index, insert vectors/documents and search among them via NNext.

Let's begin by installing the NNext server.

```shell
NNEXT_PKG=nnext-0.0.12-amd64.deb
NNEXT_URL=https://trove.nnext.io/downloads
wget $NNEXT_URL/$NNEXT_PKG
wget $NNEXT_URL/$NNEXT_PKG.sha512
shasum -a 512 -c $NNEXT_PKG.sha512
sudo dpkg -i $NNEXT_PKG
```

Run nnext
```shell
sudo nnext
```

You should see something like this:
```shell
...
...
[2022-04-27 13:02:10.029] [info] 🏁 Started NNext at ▸ 127.0.0.1:6040
```

Install the Python client for NNext:

```shell
pip install nnext
```

Finally, to follow the examples below, install numpy:

1.  From the souce here

```shell
pip install -r requirements.txt
```

or

2. Via PyPi

```shell
pip install numpy==1.22.3
```

We can now initialize the client and create a index:

```python
import numpy as np
import nnext
from nnext import _and, _eq, _gte, _in

# Create and initialize the vector client.
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
    name='test_index')

# Insert vectors into the index.
n_vecs = 1000
vectors = np.random.rand(n_vecs, n_dim)
nnindex.add(vectors)

# Create a query vector set.
n_queries = 10
q_vectors = np.random.rand(n_queries, n_dim)

# Search for the nearest neighbors of the
# query set among the indexed vectors.
k = 5
_idx, _res = nnindex.search(q_vectors, k, return_vector=True)

# The search operation returns a 2d list of the indices of the nearest neighbors
# for each vector in the query set (i.e. a nested list with shape (n_queries, k)),
# and optionally the data associated with the neighbor vectors themselves 
# (i.e. a nested list of shape (n_queries, k, n_dim))
assert len(_idx) == n_queries
assert len(_idx[0]) == k
assert len(_res) == n_queries
assert len(_res[0]) == k
assert len(_res[0][0]) == n_dim
```

### 2. Compound indices
🚧 WIP 🚧.

Not implemented.

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

## Documentation

All NNext Server and Client documentation, including pynnext integration articles and helpful recipes, can be found at:
<br/>

🚧 WIP 🚧<br>
[https://nnext.ai/docs/](https://nnext.ai/docs)

## FAQs

<details><summary>How does this differ from Faiss, ScaNN and Annoy?</summary>
<p>
First of all, NNext uses Faiss under the hood. All of these libraries have python
packages installable via PIP or Conda, and those are very easy to use, from install to the API. However, while
they allow you to quickly get started, they don't allow for persistence, index growth or high availability. If your
application goes down for whatever reason, so do your search indices and data.
</p>
</details>

<details><summary>How does this differ from Milvus?</summary>
<p>
Milvus is a large piece of software, that takes a non-trivial amount of effort to setup, administer, scale and fine-tune.
It offers you a few thousand configuration parameters that may need to be tuned to get to your ideal configuration. As a result, it's better suited for large teams
who have the bandwidth to get it production-ready, and regularly monitor it and scale it, especially when they have a need to store
billions of documents and petabytes of data (eg: logs).

NNext is built specifically for decreasing the "time to market" for a delightful nearest-neighbor search experience. It 
is a light-weight yet powerful & scaleable alternative that focuses on Developer Happiness and Experience with a 
clean well-documented API, clear semantics and smart defaults so it just works well out-of-the-box, without you having to turn many knobs.

See a side-by-side feature comparison [here](https://typesense.org/typesense-vs-algolia-vs-elasticsearch-vs-meilisearch/).
</p>
</details>

<details><summary>How does this differ from other fully managed solutions like Pinecone?</summary>
<p>
In brief - **no vendor lock-in**. Tired of using NNext cloud? Pack up your vectors and go. Obviously we don't want you 
to go, but if you have to, NNext Cloud allows you to download a compressed zip file containing the latest backup of 
your vectors to your machine. These vectors can then be used with another installation of NNext on premise or on 
another cloud provider.

Pinecone is a proprietary, hosted, nearest-neighbour search-as-a-service product that works well, when cost is not an 
issue. However, fast growing applications will quickly run into search & indexing limits, accompanied by expensive plan
upgrades as they scale.

NNext on the other hand is an open-source product that you can run on your own infrastructure or
use our managed SaaS offering - [NNext Cloud](https://app.nnext.ai).
The open source version is free to use (besides of course your own infra costs).
With NNext Cloud we do not charge by records or search operations. Instead, you get a dedicated cluster
and you can throw as much data and traffic at it as it can handle. You only pay a fixed hourly cost & bandwidth charges
for it, depending on the configuration your choose, similar to most modern cloud platforms.

From a product perspective, NNext is closer in spirit to Jina.ai than Pinecone.

See a side-by-side feature comparison [here](https://nnext.ai/product-matrix?source=gitreadme).
</p>
</details>

<details><summary>Why the Elastic License 2.0?</summary>
<p>
NNext Server is **source available**, **server software** and we expect users to typically run it as a separate daemon, 
and not integrate it 
with their own code. Elastic Licence 2.0 (EL2) covers and allows for this use case **generously**. We aim to set the
minimum limitations necessary to strike a fair balance between freedom to use, share and change the software, and 
preventing actions that will harm the community.

If you have specifics that prevent you from using NNext due to a licensing issue, we're happy to explore this topic 
further with you. Please reach out to us legal@nnext.ai.
</p>
</details>
<details><summary>I heard Elasticsearch and OpenSearch were planning on implementing ANN Search?</summary>
<p>
Fundamentally, Elasticsearch and it's variants, run on the JVM, which by itself can be quite an effort to tune to run 
optimally. NNext, on the other hand, is a single light-weight self-contained native binary, so it's simple to setup and
operate. Furthermore, ANN search on Elasticseach runs as a secondary process, a sidecar, which is not natively 
supported by the main indexing engine.
</p>
</details>

## Who is NNext?

[NNext](https://nnext.io/) builds open-source ML-Ops software to help make development and deployment of machine 
learning applications painless.

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

Checkout the [guide to contributing](#) to learn more.

