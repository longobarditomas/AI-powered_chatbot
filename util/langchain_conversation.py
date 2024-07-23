import os
import json

from pathlib import Path

from util.config import OPENAI_API_KEY, PERSIST_DIR

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.chat_history import InMemoryChatMessageHistory, BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage
from langchain_core.messages import AIMessage


def chat_open_ai_conversation(query='', conversationID=0, doc=''):
    if conversationID and exists_session(conversationID):
        loaded_messages = read_session(conversationID, "sessions")
    else:
        loaded_messages = []
    return get_chat_open_ai_answer(query, conversationID, doc, loaded_messages)

def get_chat_open_ai_answer(question='', conversationID=0, doc='', store={}):
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a friendly and polite assistant. Always respond in a kind and respectful manner."),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
        ]
    )

    chain = prompt | ChatOpenAI(model="gpt-4o")
    
    session_history = read_session(conversationID, "sessions")

    def get_session_history(session_id: str) -> BaseChatMessageHistory:
        return InMemoryChatMessageHistory(messages=session_history)

    wrapped_chain = RunnableWithMessageHistory(chain, get_session_history)

    config = {"configurable": {"session_id": conversationID}}

    result = wrapped_chain.invoke(
        [HumanMessage(content=question)],
        config,
    )

    store_session(conversationID, session_history + [HumanMessage(content=question), AIMessage(content=result.content)], "sessions")

    return create_json_data(conversationID, result.content)


def store_session(session_id, messages, folder='sessions'):
    if not os.path.exists(folder):
        os.makedirs(folder)
        os.chmod(folder, 0o774)
    filepath = os.path.join(folder, f'{session_id}.json')
    with open(filepath, 'w') as file:
        json.dump([message.dict() for message in messages], file)
    os.chmod(filepath, 0o774)


def read_session(session_id, folder='sessions'):
    filepath = os.path.join(folder, f'{session_id}.json')
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            messages = json.load(file)
            return [HumanMessage(**msg) if msg['type'] == 'human' else AIMessage(**msg) for msg in messages]
    else:
        return []


def exists_session(conversationID=0):
    file_path = 'sessions/'+conversationID+'.json'
    return Path(file_path).exists()


def create_json_data(conversationID, conversation):
    data = {
        "conversationID": conversationID,
        "conversation"  : conversation
    }
    json_data = json.dumps(data)
    return json_data
