import os
from flask import Flask, request
from datetime import datetime

from util.langchain_conversation import chat_open_ai_conversation
from util.elasticserach import db_search

app = Flask(__name__)

@app.route("/ask")
def ask():
    base_dir  = os.path.dirname(os.path.abspath(__file__))
    filename  = 'state_of_the_union.txt'
    filepath  = os.path.join( base_dir+'/data', filename)
    query     = request.args.get('query', '')
    docs      = db_search(filepath, query)
    
    conversationID = request.args.get('conversationID', datetime.now().strftime("%Y%m%d%H%M%S"))
    answer = chat_open_ai_conversation(query, conversationID, docs)
    return answer


