from promptml_cli.client import Provider, ClientFactory, Model
from openai import NotFoundError

def get_sync_response(**kwargs) -> str:
    response = ""
    provider = kwargs.get('provider')
    model = kwargs.get('model')
    serialized_data = kwargs.get('serialized_data')

    if provider == Provider.GOOGLE.value:
        if model == Model.GPT_4O.value:
            model = Model.GEMINI_1_5_FLASH_LATEST.value

        g_client = ClientFactory(Provider.GOOGLE.value, model=model).get_client()
        response = g_client.generate_content(serialized_data).text
    elif provider == Provider.OPENAI.value:
        openai_client = ClientFactory(Provider.OPENAI.value, model=model).get_client()
        chat_completion = openai_client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": serialized_data,
                },
            ],
            model=model,
        )
        response = chat_completion.choices[0].message.content
    elif provider == Provider.OLLAMA.value:
        olla_client = ClientFactory(Provider.OLLAMA.value).get_client()
        chat_completion = olla_client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": serialized_data,
                },
            ],
            model=model,
        )
        response = chat_completion.choices[0].message.content

    return response

def get_stream_response(**kwargs):
    provider = kwargs.get('provider')
    model = kwargs.get('model')
    serialized_data = kwargs.get('serialized_data')

    if provider == Provider.GOOGLE.value:
        if model == Model.GPT_4O.value:
           model = Model.GEMINI_1_5_FLASH_LATEST.value

        g_client = ClientFactory(Provider.GOOGLE.value, model=model).get_client()
        response = g_client.generate_content(serialized_data, stream=True)

        for chunk in response:
            yield chunk.text
    elif provider == Provider.OPENAI.value:
        openai_client = ClientFactory(Provider.OPENAI.value, model=model).get_client()
        response = openai_client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": serialized_data,
                },
            ],
            model=model,
            stream=True,
        )

        chunk_message = ""
        for chunk in response:
            chunk_message = chunk.choices[0].delta.content  # extract the message
            yield chunk_message

    elif provider == Provider.OLLAMA.value:
        try:
            olla_client = ClientFactory(Provider.OLLAMA.value).get_client()
            response = olla_client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": serialized_data,
                    },
                ],
                model=model,
                stream=True,
            )

            chunk_message = ""
            for chunk in response:
                chunk_message = chunk.choices[0].delta.content
                yield chunk_message
        except NotFoundError as e:
            print("Error: Ollama model not found. Use command `ollama list` to see available models in your system.")
