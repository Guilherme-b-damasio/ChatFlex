import openai
import time

assistente_id = ""
assistente_id2 = ""
api_key = ""

openai.api_key = api_key



def submit_message(id_ass, thread, usuario_input):
    openai.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=usuario_input
    )
    return openai.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=id_ass,
    )

def get_response(thread):
    return openai.beta.threads.messages.list(thread_id=thread.id, order="asc")

def create_thread_and_run(user_input, assistant_id):
    thread = openai.beta.threads.create()
    run = submit_message(assistant_id, thread, user_input)
    return thread, run

def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = openai.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.4)
    return run

def select_assistant(assistant_name):
    if assistant_name == "Assitente 1":
        return assistente_id
    elif assistant_name == "Assistente 2":
        return assistente_id2
    else:
        return assistente_id  # ou retorne um ID padrão