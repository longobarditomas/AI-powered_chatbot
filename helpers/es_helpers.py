from elasticsearch import Elasticsearch
from langchain_elasticsearch import ElasticsearchStore
from util.config import ELASTIC_CLOUD_API_KEY, ELASTICSEARCH_URL, ELASTICSEARCH_INDEX_NAME, ELASTIC_CLOUD_URL, ELASTIC_CLOUD_INDEX_NAME
from langchain_openai import OpenAIEmbeddings

# Return a configured Elasticsearch client
def get_es_client():
    if ELASTIC_CLOUD_API_KEY:
        return Elasticsearch(
            ELASTIC_CLOUD_URL,
            api_key=ELASTIC_CLOUD_API_KEY
        )
    return Elasticsearch(ELASTICSEARCH_URL)

def get_embeddings():
    return OpenAIEmbeddings()

def get_elasticsearch_store(embedding=None):
    embedding = embedding or get_embeddings()
    if ELASTIC_CLOUD_API_KEY:
        return ElasticsearchStore(
            es_url=ELASTIC_CLOUD_URL,
            es_api_key=ELASTIC_CLOUD_API_KEY,
            index_name=ELASTIC_CLOUD_INDEX_NAME,
            embedding=embedding
        )
    return ElasticsearchStore(
        es_url=ELASTICSEARCH_URL,
        index_name=ELASTICSEARCH_INDEX_NAME,
        embedding=embedding
    )

def create_elasticsearch_store_from_documents(docs, embedding=None):
    embedding = embedding or get_embeddings()
    if ELASTIC_CLOUD_API_KEY:
        return ElasticsearchStore.from_documents(
            docs,
            embedding,
            es_url=ELASTIC_CLOUD_URL,
            es_api_key=ELASTIC_CLOUD_API_KEY,
            index_name=ELASTIC_CLOUD_INDEX_NAME,
        )
    return ElasticsearchStore.from_documents(
        docs,
        embedding,
        es_url=ELASTICSEARCH_URL,
        index_name=ELASTICSEARCH_INDEX_NAME,
    )
