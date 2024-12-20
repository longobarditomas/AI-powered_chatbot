import os

from util.config import ELASTICSEARCH_URL, ELASTICSEARCH_INDEX_NAME, DOCS_FILE
from elasticsearch import Elasticsearch
from langchain_elasticsearch import ElasticsearchStore
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter

# Constants
ES_URL     = ELASTICSEARCH_URL
INDEX_NAME = ELASTICSEARCH_INDEX_NAME
DOCS_FILE  = DOCS_FILE

# Global Elasticsearch client
es_client = Elasticsearch(ES_URL)

def setup_index():
    if not es_client.indices.exists(index=INDEX_NAME):
        current_dir  = os.path.dirname(os.path.abspath(__file__))
        base_dir     = os.path.dirname(current_dir)
        filename     = DOCS_FILE
        filepath     = os.path.join( base_dir+'/data', filename)

        loader        = TextLoader(filepath)
        documents     = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0)
        docs          = text_splitter.split_documents(documents)
        embeddings    = OpenAIEmbeddings()

        db = ElasticsearchStore.from_documents(
            docs,
            embeddings,
            es_url=ES_URL,
            index_name=INDEX_NAME,
        )
        es_client.indices.refresh(index=INDEX_NAME)
        print("Index created!!!")
    else:
        print("Index already exists.")
    return True

def query_index(query, top_n=2):
    if not es_client.indices.exists(index=INDEX_NAME):
        raise Exception("Index does not exist. Please set up the index first.")
    
    embeddings = OpenAIEmbeddings()
    db = ElasticsearchStore(
        es_url=ES_URL,
        index_name=INDEX_NAME,
        embedding=embeddings,
    )
    results = db.similarity_search(query)
    concatenated_content = ""
    for result in results[:top_n]:
        concatenated_content += result.page_content + "\n"
    return concatenated_content


def delete_index():
    if not es_client.indices.exists(index=INDEX_NAME):
        raise Exception("Index does not exist. Please set up the index first.")
    
    embeddings = OpenAIEmbeddings()
    db = ElasticsearchStore(
        es_url=ES_URL,
        index_name=INDEX_NAME,
        embedding=embeddings,
    )
    db.client.indices.delete(
        index=INDEX_NAME,
        ignore_unavailable=True,
        allow_no_indices=True,
    )
    print("Index deleted!!!")
    return True


def db_search(query=''):
    if (not es_client.indices.exists(index=INDEX_NAME)):
        setup_index()
        
    result = query_index(query, 2)
    return result

