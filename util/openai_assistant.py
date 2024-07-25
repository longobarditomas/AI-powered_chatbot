import time
import json
from openai import OpenAI
from util.config import OPENAI_API_KEY, PERSIST_DIR

client = OpenAI()


def get_assistant_conversation(query=''):
    file      = upload_assistant_file()
    assistant = create_assistant(file.id)
    thread    = create_thread(file.id, query)
    run       = create_thread_run(thread.id, assistant.id)

    time.sleep(10)
    retrieve_thread_run(thread.id, run.id)

    answer = get_thread_assistant_answer(thread.id)
    return create_json_data(answer)


def upload_assistant_file():
    file = client.files.create(
        file=open("data/test.csv", "rb"),
        purpose='assistants'
    )
    return file


def create_assistant(file_id=""):
    assistant = client.beta.assistants.create(
        name="Jarvis",
        instructions="Answer as if you were a co-worker.",
        model="gpt-4o-mini",
        tools=[{"type": "code_interpreter"}],
        tool_resources={
            "code_interpreter": {
            "file_ids": [file_id]
            }
        }
    )
    return assistant


def create_thread(file_id="", query=""):
    thread = client.beta.threads.create(
        messages=[
            {
            "role": "user",
            "content": query,
            "attachments": [
                {
                "file_id": file_id,
                "tools": [{"type": "code_interpreter"}]
                }
            ]
            }
        ]
    )
    return thread


def create_thread_run(thread_id="", assistant_id=""):
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
    )
    return run


def retrieve_thread_run(thread_id="", run_id=""):
    run = client.beta.threads.runs.retrieve(
        thread_id=thread_id,
        run_id=run_id,
    )
    return run


def get_thread_messages(thread_id=""):
    messages = client.beta.threads.messages.list(
        thread_id=thread_id,
    )
    for message in reversed(messages.data):
        print(message.role + ": " + message.content[0].text.value)
    return messages.data


def get_thread_assistant_answer(thread_id=""):
    messages = client.beta.threads.messages.list(
        thread_id=thread_id,
    )
    for message in messages.data:
        if message.role == "assistant":
            return message.content[0].text.value
    return ""


def create_json_data(answer=""):
    data = {
        "answer": answer,
    }
    json_data = json.dumps(data)
    return json_data
