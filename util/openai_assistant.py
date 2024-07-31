import os
import time
import json
from openai import OpenAI
from util.config import OPENAI_API_KEY, PERSIST_DIR

client = OpenAI()


def get_assistant_conversation(query="", instructions="", filepath=""):    
    if filepath:
        file      = upload_assistant_file(filepath)
        assistant = create_assistant(instructions, file.id)
        thread    = create_thread(query, file.id)
    else:
        assistant = create_assistant(instructions)
        thread    = create_thread(query)
    run  = create_thread_run(thread.id, assistant.id)

    time.sleep(10)
    retrieve_thread_run(thread.id, run.id)

    answer = get_thread_assistant_answer(thread.id)
    return create_json_data(answer)


def upload_assistant_file(filepath=""):
    if filepath:
        file = client.files.create(
            file=open(filepath, "rb"),
            purpose='assistants'
        )
        return file
    else:
        return False


def create_assistant(instructions="", file_id=""):
    tools = []
    tool_resources = {}

    if file_id:
        tools.append({"type": "code_interpreter"})
        tool_resources = {
            "code_interpreter": {
                "file_ids": [file_id]
            }
        }
    assistant = client.beta.assistants.create(
        name="Jarvis",
        instructions=instructions,
        model="gpt-4o-mini",
        tools=tools,
        tool_resources=tool_resources
    )
    return assistant


def create_thread(query="", file_id=""):
    attachments = []

    if file_id:
        attachments = [
            {
            "file_id": file_id,
            "tools": [{"type": "code_interpreter"}]
            }
        ]
    thread = client.beta.threads.create(
        messages=[
            {
            "role": "user",
            "content": query,
            "attachments": attachments
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
            if message.content[0].text.annotations[0].file_path.file_id:
                file_id = message.content[0].text.annotations[0].file_path.file_id
                file_extension = os.path.splitext(message.content[0].text.annotations[0].text)[1]
                download_asistant_generated_file(file_id, file_extension)
            return message.content[0].text.value
    return ""


def download_asistant_generated_file(file_id, file_extension):
    image_data = client.files.content(file_id)
    image_data_bytes = image_data.read()

    with open(f"./assistant_data/{file_id}{file_extension}", "wb") as file:
        file.write(image_data_bytes)


def create_json_data(answer=""):
    data = {
        "answer": answer,
    }
    json_data = json.dumps(data)
    return json_data
