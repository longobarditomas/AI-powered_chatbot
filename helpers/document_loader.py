import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter

def load_and_split_documents(filepath, chunk_size=500, chunk_overlap=0):
    loader = TextLoader(filepath)
    documents = loader.load()
    splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_documents(documents)