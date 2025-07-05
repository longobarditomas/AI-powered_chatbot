import os

from dotenv import load_dotenv
load_dotenv()

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir( base_dir )

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
PERSIST_DIR    = base_dir+'/db/'

ELASTICSEARCH_URL = os.environ.get("ELASTICSEARCH_URL")
ELASTICSEARCH_INDEX_NAME = os.environ.get("ELASTICSEARCH_INDEX_NAME")
ELASTICSEARCH_DOCS_FILE = os.environ.get("ELASTICSEARCH_DOCS_FILE")

ELASTIC_CLOUD_ID = os.environ.get("ELASTIC_CLOUD_ID")
ELASTIC_CLOUD_URL = os.environ.get("ELASTIC_CLOUD_URL")
ELASTIC_CLOUD_API_KEY = os.environ.get("ELASTIC_CLOUD_API_KEY")
ELASTIC_CLOUD_INDEX_NAME = os.environ.get("ELASTIC_CLOUD_INDEX_NAME")
ELASTIC_CLOUD_DOCS_FILE = os.environ.get("ELASTIC_CLOUD_DOCS_FILE")
