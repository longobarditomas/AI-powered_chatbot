from flask import Flask, request
from datetime import datetime

from util.langchain_conversation import chat_open_ai_conversation

app = Flask(__name__)

@app.route("/ask")
def ask():
    query = request.args.get('query', '')
    conversationID = request.args.get('conversationID', datetime.now().strftime("%Y%m%d%H%M%S"))
    answer = chat_open_ai_conversation(query, conversationID, '')
    return answer
    """ return f"Hello, I'll help you with your query \"{query}\". This is your conversationID {conversationID}, in case you want to continue.\n Answer: \"{answer}\"" """

