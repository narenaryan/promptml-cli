import argparse
import enum
import os
import time

from openai import APIConnectionError
from promptml.parser import PromptParserFromFile
from rich.markdown import Markdown
from rich.console import Console
from typing import Union

from promptml_cli.client import Provider, ClientFactory

def run():
    # Take user input of following arguments
    # 1. --file, -f : Path to the PromptML file
    # 2. --model, -m : Model to use for the completion
    # 3. --serializer, -s : Serializer to use for the completion
    console = Console(
        color_system="truecolor"
    )
    arg_parser = argparse.ArgumentParser(
                prog='promptml-cli',
                description='A Command Line Interface tool to run PromptML files with popular Generative AI models',
                epilog='-----------------------------'
            )

    arg_parser.add_argument('-f', '--file', type=str, help='Path to the PromptML(.pml) file', required=True)
    arg_parser.add_argument('-m', '--model', type=str, help='Model to use for the completion', default='gpt-4o')
    arg_parser.add_argument('-s', '--serializer', type=str, help='Serializer to use for the completion. Default is `xml`', default='xml', choices=['xml', 'json', 'yaml'])
    arg_parser.add_argument('-p', '--provider', type=str, help='GenAI provider to use for the completion. Default is `openai`', default=Provider.OPENAI.value, choices=[Provider.OPENAI.value, Provider.GOOGLE.value])


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
    response = ""
    if args.provider == Provider.GOOGLE.value:
        if args.model == "gpt-4o":
            args.model = "gemini-1.5-flash-latest"

        g_client = ClientFactory(Provider.GOOGLE.value, model=args.model).get_client()
        response = g_client.generate_content(serialized_data).text
    elif args.provider == Provider.OPENAI.value:
        openai_client = ClientFactory(Provider.OPENAI.value, model=args.model).get_client()
        try:
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
        except APIConnectionError:
            console.print(
                "Error connecting to OpenAI API. Try again!",
                style = "bold red"
            )
            return

    # Print the completion with rich console
    console.print(Markdown(response, "\n"), soft_wrap=True, new_line_start=True)
    console.print(f"Time taken: {time.time() - now} seconds", style="bold green")

if __name__ == '__main__':
    run()
