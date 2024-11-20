import os

from dotenv import load_dotenv
load_dotenv()

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir( base_dir )

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
PERSIST_DIR    = base_dir+'/db/'

ELASTICSEARCH_URL = os.environ.get("ELASTICSEARCH_URL")
ELASTICSEARCH_INDEX_NAME = os.environ.get("ELASTICSEARCH_INDEX_NAME")

DOCS_FILE = os.environ.get("DOCS_FILE")