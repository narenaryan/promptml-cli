""" Command Line Interface tool to run PromptML files with popular Generative AI models """

import argparse
import time

from openai import APIConnectionError
from promptml.parser import PromptParserFromFile
from rich.markdown import Markdown
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.style import Style
from rich import box

from promptml_cli.client import Provider, ClientFactory, Model


def get_sync_response(args, serialized_data) -> str:
    response = ""
    if args.provider == Provider.GOOGLE.value:
        if args.model == Model.GPT_4O.value:
            args.model = Model.GEMINI_1_5_FLASH_LATEST.value

        g_client = ClientFactory(Provider.GOOGLE.value, model=args.model).get_client()
        response = g_client.generate_content(serialized_data).text
    elif args.provider == Provider.OPENAI.value:
        openai_client = ClientFactory(Provider.OPENAI.value, model=args.model).get_client()
        chat_completion = openai_client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": serialized_data,
                },
            ],
            model=args.model,
        )
        response = chat_completion.choices[0].message.content

    return response

def get_stream_response(args, serialized_data):
    if args.provider == Provider.GOOGLE.value:
        if args.model == Model.GPT_4O.value:
            args.model = Model.GEMINI_1_5_FLASH_LATEST.value

        g_client = ClientFactory(Provider.GOOGLE.value, model=args.model).get_client()
        response = g_client.generate_content(serialized_data, stream=True)

        for chunk in response:
            yield chunk.text
    elif args.provider == Provider.OPENAI.value:
        openai_client = ClientFactory(Provider.OPENAI.value, model=args.model).get_client()
        response = openai_client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": serialized_data,
                },
            ],
            model=args.model,
            stream=True,
        )

        chunk_message = ""
        for chunk in response:
            chunk_message = chunk.choices[0].delta.content  # extract the message
            yield chunk_message

def run():
    console = Console(
        color_system="truecolor",
        record=True,
    )
    neon_blue = Style(color="cyan", bold=True)

    arg_parser = argparse.ArgumentParser(
                prog='promptml-cli',
                description='A Command Line Interface (CLI) tool to run Prompt Markup Language (PromptML) files with popular Generative AI models',
                epilog='For more details of composing PromptML files, visit: https://promptml.org/'
            )

    arg_parser.add_argument('-f', '--file', type=str, help='Path to the PromptML(.pml) file', required=True)
    arg_parser.add_argument('-m', '--model', type=str, help='Model to use for the completion', default='gpt-4o')
    arg_parser.add_argument('-s', '--serializer', type=str, help='Serializer to use for the completion. Default is `xml`', default='xml', choices=['xml', 'json', 'yaml'])
    arg_parser.add_argument('-p', '--provider', type=str, help='GenAI provider to use for the completion. Default is `openai`', default=Provider.OPENAI.value, choices=[Provider.OPENAI.value, Provider.GOOGLE.value])
    arg_parser.add_argument('--stream', help='Stream chunks for the GenAI response. Default is non-streaming response.', action='store_true')
    arg_parser.add_argument('--raw', help='Return raw output from LLM (best for saving into files or piping)', action='store_true')

    args = arg_parser.parse_args()

    # Parse the PromptML file
    parser = PromptParserFromFile(args.file)
    parser.parse()

    serialized_data = None

    if args.serializer == "xml":
        serialized_data = parser.to_xml()
    elif args.serializer == "json":
        serialized_data = parser.to_json()
    elif args.serializer == "yaml":
        serialized_data = parser.to_yaml()
    else:
        serialized_data = parser.to_xml()


    now = time.time()
    if not args.stream:
        try:
            response = get_sync_response(args, serialized_data)
        except APIConnectionError:
            console.print(
                "Error connecting to provider API. Try again! Please turn-off the VPN if needed.",
                style = "bold red"
            )
            return
        # Print the completion with rich console
        if args.raw:
            print(response)
        else:
            console.print(Panel(Markdown(response, "\n")), soft_wrap=True, new_line_start=True)
    else:
        with Live(refresh_per_second=4) as live:
            message = ""
            for chunk in get_stream_response(args, serialized_data):
                if chunk:
                    if args.raw:
                        print(chunk, end="")
                        continue
                    message += chunk
                    markdown_content = Markdown(message, "\n")
                    panel = Panel(markdown_content, border_style=neon_blue, safe_box=True)
                    live.update(panel)

    if not args.raw:
        console.print(f"\nTime taken: {time.time() - now} seconds", style="bold green")

if __name__ == '__main__':
    run()
