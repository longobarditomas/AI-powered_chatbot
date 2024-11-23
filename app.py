import os
from flask import Flask, request
from datetime import datetime
from urllib.parse import unquote

from flask_cors import CORS
app = Flask(__name__)
CORS(app)

from util.langchain_conversation import chat_open_ai_conversation
from util.openai_assistant import get_assistant_conversation
from util.elasticserach import db_search

app = Flask(__name__)

@app.route("/ask")
def ask():
    query = request.args.get('query', '')
    docs  = db_search(query)
    model = ''
    
    conversationID = request.args.get('conversationID', datetime.now().strftime("%Y%m%d%H%M%S"))
    answer = chat_open_ai_conversation(query, conversationID, docs, model)
    return answer


@app.route("/assistant", methods=['POST'])
def assistant():
    query = request.form.get('query')
    instructions = request.form.get('instructions') or "Answer as if you were a co-worker."

    session_id = request.form.get('session_id')
    session_data = get_session_data(session_id)

    filepath = ""
    if 'file' in request.files:
        file = request.files['file']
        if file:
            store_file(file)
            filename = file.filename
            filepath = "tmp/"+filename

    assistant_conversation = get_assistant_conversation(query, session_data["assistant_id"], instructions, session_data["thread_id"], filepath)
    return assistant_conversation


def get_session_data(session_id=""):
    session_data = {
        "assistant_id": "",
        "thread_id": ""
    }
    if session_id: 
        session_id = unquote(session_id)
        explode    = session_id.split('-') 
        if explode[0]:
            session_data["assistant_id"] = explode[0]
        if explode[1]:
            session_data["thread_id"] = explode[1]
    return session_data


def store_file(file):
    UPLOAD_FOLDER = 'tmp'
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
        os.chmod(UPLOAD_FOLDER, 0o774)
    file.save(os.path.join(UPLOAD_FOLDER, file.filename))