import json
import openai

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
    memory = ConversationBufferMemory(return_messages=True)
    return get_chat_open_ai_answer(query, conversationID, doc, memory)


def get_chat_open_ai_answer(question='', conversationID='', doc='', memory=None):
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
        return create_json_data(conversationID, messages)

    except openai.RateLimitError as e:
        return f"API call failed after retries: {str(e)}"


def create_json_data(conversationID, conversation):
    data = {
        "conversationID": conversationID,
        "conversation"  : conversation
    }
    json_data = json.dumps(data)
    return json_data