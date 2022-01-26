<p align="center">
  <img src="https://res.cloudinary.com/meilisearch/image/upload/v1587402338/SDKs/meilisearch_python.svg" alt="meilisearch-Python" width="200" height="200" />
</p>

<h1 align="center">meilisearch Python</h1>

<h4 align="center">
  <a href="https://github.com/meilisearch/meilisearch">meilisearch</a> |
  <a href="https://docs.meilisearch.com">Documentation</a> |
  <a href="https://slack.meilisearch.com">Slack</a> |
  <a href="https://roadmap.meilisearch.com/tabs/1-under-consideration">Roadmap</a> |
  <a href="https://www.meilisearch.com">Website</a> |
  <a href="https://docs.meilisearch.com/faq">FAQ</a>
</h4>

<p align="center">
  <a href="https://badge.fury.io/py/meilisearch"><img src="https://badge.fury.io/py/meilisearch.svg" alt="PyPI version"></a>
  <a href="https://github.com/meilisearch/meilisearch-python/actions"><img src="https://github.com/meilisearch/meilisearch-python/workflows/Tests/badge.svg" alt="Test Status"></a>
  <a href="https://github.com/meilisearch/meilisearch-python/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-informational" alt="License"></a>
  <a href="https://app.bors.tech/repositories/28782"><img src="https://bors.tech/images/badge_small.svg" alt="Bors enabled"></a>
</p>

<p align="center">⚡ The meilisearch API client written for Python 🐍</p>

**meilisearch Python** is the meilisearch API client for Python developers.

**meilisearch** is an open-source search engine. [Discover what meilisearch is!](https://github.com/meilisearch/meilisearch)

## Table of Contents <!-- omit in toc -->

- [📖 Documentation](#-documentation)
- [🔧 Installation](#-installation)
- [🚀 Getting Started](#-getting-started)
- [🤖 Compatibility with meilisearch](#-compatibility-with-meilisearch)
- [💡 Learn More](#-learn-more)
- [⚙️ Development Workflow and Contributing](#️-development-workflow-and-contributing)

## 📖 Documentation

See our [Documentation](https://docs.meilisearch.com/learn/tutorials/getting_started.html) or our [API References](https://docs.meilisearch.com/reference/api/).

## 🔧 Installation

**Note**: Python 3.6+ is required.

With `pip3` in command line:

```bash
pip3 install meilisearch
```

### Run meilisearch <!-- omit in toc -->

There are many easy ways to [download and run a meilisearch instance](https://docs.meilisearch.com/reference/features/installation.html#download-and-launch).

For example, using the `curl` command in [your Terminal](https://itconnect.uw.edu/learn/workshops/online-tutorials/web-publishing/what-is-a-terminal/):

```bash
# Install meilisearch
curl -L https://install.meilisearch.com | sh

# Launch meilisearch
./meilisearch --master-key=masterKey
```

NB: you can also download meilisearch from **Homebrew** or **APT** or even run it using **Docker**.

## 🚀 Getting Started

#### Add Documents <!-- omit in toc -->

```python
import meilisearch

client = meilisearch.Client('http://127.0.0.1:7700', 'masterKey')

# An index is where the documents are stored.
index = client.index('movies')

documents = [
      { 'id': 1, 'title': 'Carol', 'genres': ['Romance', 'Drama'] },
      { 'id': 2, 'title': 'Wonder Woman', 'genres': ['Action', 'Adventure'] },
      { 'id': 3, 'title': 'Life of Pi', 'genres': ['Adventure', 'Drama'] },
      { 'id': 4, 'title': 'Mad Max: Fury Road', 'genres': ['Adventure', 'Science Fiction'] },
      { 'id': 5, 'title': 'Moana', 'genres': ['Fantasy', 'Action']},
      { 'id': 6, 'title': 'Philadelphia', 'genres': ['Drama'] },
]

# If the index 'movies' does not exist, meilisearch creates it when you first add the documents.
index.add_documents(documents) # => { "uid": 0 }
```

With the task `uid`, you can check the status (`enqueued`, `processing`, `succeeded` or `failed`) of your documents addition using the [task](https://docs.meilisearch.com/reference/api/tasks.html#get-task).

#### Basic Search <!-- omit in toc -->

``` python
# meilisearch is typo-tolerant:
index.search('caorl')
```

Output:

```json
{
    "hits": [
        {
            "id": 1,
            "title": "Carol",
            "genre": ["Romance", "Drama"]
        }
    ],
    "offset": 0,
    "limit": 20,
    "processingTimeMs": 1,
    "query": "caorl"
}
```

#### Custom Search <!-- omit in toc -->

All the supported options are described in the [search parameters](https://docs.meilisearch.com/reference/features/search_parameters.html) section of the documentation.

```python
index.search(
  'phil',
  {
    'attributesToHighlight': ['*'],
  }
)
```

JSON output:

```json
{
    "hits": [
        {
            "id": 6,
            "title": "Philadelphia",
            "_formatted": {
                "id": 6,
                "title": "<em>Phil</em>adelphia",
                "genre": ["Drama"]
            }
        }
    ],
    "offset": 0,
    "limit": 20,
    "processingTimeMs": 0,
    "query": "phil"
}
```

#### Custom Search With Filters <!-- omit in toc -->

If you want to enable filtering, you must add your attributes to the `filterableAttributes` index setting.

```py
index.update_filterable_attributes([
  'id',
  'genres'
])
```

You only need to perform this operation once.

Note that meilisearch will rebuild your index whenever you update `filterableAttributes`. Depending on the size of your dataset, this might take time. You can track the process using the [task](https://docs.meilisearch.com/reference/api/tasks.html#get-task).

Then, you can perform the search:

```py
index.search(
  'wonder',
  {
    filter: ['id > 1 AND genres = Action']
  }
)
```

```json
{
  "hits": [
    {
      "id": 2,
      "title": "Wonder Woman",
      "genres": ["Action","Adventure"]
    }
  ],
  "offset": 0,
  "limit": 20,
  "nbHits": 1,
  "processingTimeMs": 0,
  "query": "wonder"
}
```

## 🤖 Compatibility with meilisearch

This package only guarantees the compatibility with the [version v0.25.0 of meilisearch](https://github.com/meilisearch/meilisearch/releases/tag/v0.25.0).

## 💡 Learn More

The following sections may interest you:

- **Manipulate documents**: see the [API references](https://docs.meilisearch.com/reference/api/documents.html) or read more about [documents](https://docs.meilisearch.com/learn/core_concepts/documents.html).
- **Search**: see the [API references](https://docs.meilisearch.com/reference/api/search.html) or follow our guide on [search parameters](https://docs.meilisearch.com/reference/features/search_parameters.html).
- **Manage the indexes**: see the [API references](https://docs.meilisearch.com/reference/api/indexes.html) or read more about [indexes](https://docs.meilisearch.com/learn/core_concepts/indexes.html).
- **Configure the index settings**: see the [API references](https://docs.meilisearch.com/reference/api/settings.html) or follow our guide on [settings parameters](https://docs.meilisearch.com/reference/features/settings.html).

## ⚙️ Development Workflow and Contributing

Any new contribution is more than welcome in this project!

If you want to know more about the development workflow or want to contribute, please visit our [contributing guidelines](/CONTRIBUTING.md) for detailed instructions!

<hr>

**meilisearch** provides and maintains many **SDKs and Integration tools** like this one. We want to provide everyone with an **amazing search experience for any kind of project**. If you want to contribute, make suggestions, or just know what's going on right now, visit us in the [integration-guides](https://github.com/meilisearch/integration-guides) repository.
