import os

from util.config import ELASTICSEARCH_URL, ELASTICSEARCH_INDEX_NAME, ELASTICSEARCH_DOCS_FILE, ELASTIC_CLOUD_API_KEY, ELASTIC_CLOUD_INDEX_NAME, ELASTIC_CLOUD_DOCS_FILE

from helpers.es_helpers import get_es_client, get_elasticsearch_store, create_elasticsearch_store_from_documents
from helpers.document_loader import load_and_split_documents

# Constants
ES_URL     = ELASTICSEARCH_URL
if ELASTIC_CLOUD_API_KEY: 
    INDEX_NAME = ELASTIC_CLOUD_INDEX_NAME
    DOCS_FILE  = ELASTIC_CLOUD_DOCS_FILE
else:
    INDEX_NAME = ELASTICSEARCH_INDEX_NAME
    DOCS_FILE  = ELASTICSEARCH_DOCS_FILE

# Global Elasticsearch client
es_client = get_es_client()

def setup_index():
    if not es_client.indices.exists(index=INDEX_NAME):
        current_dir  = os.path.dirname(os.path.abspath(__file__))
        base_dir     = os.path.dirname(current_dir)
        filename     = DOCS_FILE
        filepath     = os.path.join( base_dir+'/data', filename)

        docs = load_and_split_documents(filepath)

        db = create_elasticsearch_store_from_documents(docs)
        es_client.indices.refresh(index=INDEX_NAME)
        print("Index created!!!")
    else:
        print("Index already exists.")
    return True

def query_index(query, top_n=2):
    if not es_client.indices.exists(index=INDEX_NAME):
        raise Exception("Index does not exist. Please set up the index first.")
    
    db = get_elasticsearch_store()
    results = db.similarity_search(query)
    concatenated_content = ""
    for result in results[:top_n]:
        concatenated_content += result.page_content + "\n"
    return concatenated_content


def delete_index():
    if not es_client.indices.exists(index=INDEX_NAME):
        raise Exception("Index does not exist. Please set up the index first.")
    
    db = get_elasticsearch_store()
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

