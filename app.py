from flask import Flask, request
from datetime import datetime

app = Flask(__name__)

@app.route("/ask")
def ask():
    query = request.args.get('query', '')
    conversationID = request.args.get('conversationID', datetime.now().strftime("%Y%m%d%H%M%S"))
    return f"Hello, I'll help you with your query \"{query}\". This is your conversationID {conversationID}, in case you want to continue"

