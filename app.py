import os
from flask import Flask, request
from datetime import datetime

from util.langchain_conversation import chat_open_ai_conversation
from util.openai_assistant import get_assistant_conversation
from util.elasticserach import db_search

app = Flask(__name__)

@app.route("/ask")
def ask():
    query = request.args.get('query', '')
    docs  = db_search(query)
    
    conversationID = request.args.get('conversationID', datetime.now().strftime("%Y%m%d%H%M%S"))
    answer = chat_open_ai_conversation(query, conversationID, docs)
    return answer


@app.route("/assistant")
def assistant():
    query        = request.args.get('query', '')
    instructions = "Answer as if you were a co-worker."
    filepath     = "data/test.csv"
    #filepath     = ""
    assistant_id = ""
    thread_id    = ""
    assistant_conversation = get_assistant_conversation(query, assistant_id, instructions, thread_id, filepath)
    return assistant_conversation
