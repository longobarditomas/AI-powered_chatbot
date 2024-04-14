import os
import math

from langchain_elasticsearch import ElasticsearchStore
from langchain_openai import OpenAIEmbeddings

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter

def db_search(filepath='', query=''):
    loader = TextLoader(filepath)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()

    db = ElasticsearchStore.from_documents(
        docs,
        embeddings,
        es_url="http://localhost:9200",
        index_name="test-basic",
    )

    db.client.indices.refresh(index="test-basic")

    results = db.similarity_search(query)

    concatenated_content = ""

    for result in results[:2]:
        concatenated_content += result.page_content + "\n"

    return concatenated_content

