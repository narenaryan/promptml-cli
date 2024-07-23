""" Command Line Interface tool to run PromptML files with popular Generative AI models """

import argparse
import time

import click
from promptml.parser import PromptParserFromFile
from rich.markdown import Markdown
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.style import Style
from rich import box
from promptml_cli.generation import get_sync_response, get_stream_response
from promptml_cli.client import Provider, Model

@click.group()
def cli():
    pass

@cli.command()
@click.option('-f', '--file', required=True, type=click.Path(exists=True), help='Path to the PromptML(.pml) file')
@click.option('-m', '--model', default='gpt-4o', type=click.STRING, help='Model to use for the completion')
@click.option('-s', '--serializer', default='xml', type=click.Choice(['xml', 'json', 'yaml']), help='Serializer to use for the completion. Default is `xml`')
@click.option('-p', '--provider', default=Provider.OPENAI.value, type=click.Choice([Provider.OPENAI.value, Provider.GOOGLE.value, Provider.OLLAMA.value]), help='GenAI provider to use for the completion. Default is `openai`')
@click.option('--no-stream', default=False, is_flag=True, help='Get whole GenAI response. Default is streaming response.')
@click.option('--raw', default=False, is_flag=True, help='Return raw output from LLM (best for saving into files or piping)')
def run(file, model, serializer, provider, no_stream, raw):
    console = Console(
        color_system="truecolor",
        record=True,
    )
    neon_blue = Style(color="cyan", bold=True)
    # Parse the PromptML file
    parser = PromptParserFromFile(file)
    parser.parse()

    serialized_data = None

    if serializer == "xml":
        serialized_data = parser.to_xml()
    elif serializer == "json":
        serialized_data = parser.to_json()
    elif serializer == "yaml":
        serialized_data = parser.to_yaml()
    else:
        serialized_data = parser.to_xml()

    now = time.time()
    if no_stream:
        try:
            response = get_sync_response(
                model=model,
                file=file,
                serialized_data=serialized_data,
                provider=provider,
                raw=raw
            )
        except Exception as e:
            console.print(
                e,
                "Error connecting to provider API. Try again! Please turn-off the VPN if needed.",
                style="bold red"
            )
            return
        # Print the completion with rich console
        if raw:
            print(response)
        else:
            console.print(Panel(Markdown(response)))
            time_taken = round(time.time() - now, 2)
            console.print(f"\nTime taken: {time_taken} seconds", style="bold green")
    else:
        with Live(refresh_per_second=4) as live:
            message = ""
            for chunk in get_stream_response(
                    model=model,
                    file=file,
                    serialized_data=serialized_data,
                    provider=provider,
                    raw=raw
            ):
                if chunk:
                    if raw:
                        print(chunk, end="")
                        continue
                    message += chunk
                    markdown_content = Markdown(message, "\n")
                    live.update(markdown_content)

            time_taken = round(time.time() - now, 2)
            console.print(f"\nTime taken: {time_taken} seconds", style="bold green")


if __name__ == '__main__':
    cli()
