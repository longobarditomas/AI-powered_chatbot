import os
import json
import openai

from pathlib import Path

from util.config import OPENAI_API_KEY, PERSIST_DIR

from langchain_openai import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory, ChatMessageHistory
from langchain.schema import messages_to_dict, messages_from_dict

def chat_open_ai_conversation(query='', conversationID=0, doc=''):
    if conversationID and exists_conversation(conversationID):
        loaded_messages = read_conversation(conversationID)
        loaded_messages = loaded_messages[-4:]
        history = ChatMessageHistory(messages=messages_from_dict(loaded_messages))
        memory  = ConversationBufferMemory(chat_memory=history, return_messages=True)
        memory.buffer
    else:
        memory = ConversationBufferMemory(return_messages=True)
    return get_chat_open_ai_answer(query, conversationID, doc, memory)


def get_chat_open_ai_answer(question='', conversationID=0, doc='', memory=None):
    if memory is None:
        memory = []
    
    try: 
        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(doc),
            MessagesPlaceholder(variable_name="history"),
            HumanMessagePromptTemplate.from_template("{input}")
        ])
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        conversation = ConversationChain(memory=memory, prompt=prompt, llm=llm, verbose=True)
        conversation.predict(input=question)
        messages = messages_to_dict(conversation.memory.chat_memory.messages)
        store_conversation(conversationID, messages)
        return create_json_data(conversationID, messages)

    except openai.RateLimitError as e:
        return f"API call failed after retries: {str(e)}"


def store_conversation(conversationID=0, messages=[]):
    if int(conversationID) == 0:
        return False
    
    folder_path = 'conversations/'
    file_name   = conversationID+'.json'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        os.chmod(folder_path, 0o774)
    file_path = os.path.join(folder_path, file_name)
    with Path(file_path).open("w") as f:
        json.dump(messages, f, indent=4)
    os.chmod(file_path, 0o774)
    return conversationID


def read_conversation(conversationID=0):
    file_path = 'conversations/'+conversationID+'.json'
    with Path(file_path).open("r") as f:
        loaded_messages = json.load(f)
    return loaded_messages


def exists_conversation(conversationID=0):
    file_path = 'conversations/'+conversationID+'.json'
    return Path(file_path).exists()


def create_json_data(conversationID, conversation):
    data = {
        "conversationID": conversationID,
        "conversation"  : conversation
    }
    json_data = json.dumps(data)
    return json_data