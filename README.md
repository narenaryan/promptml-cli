# promptml-cli
A CLI application to run PromptML scripts against LLMs.

## Installation
```bash
pip install --upgrade promptml-cli
```

This installs a command called `procli`.

## Demo
[![asciicast](https://asciinema.org/a/664270.svg)](https://asciinema.org/a/664270)

## Usage

```bash
procli --help


Usage: procli [OPTIONS]

Options:
  -f, --file PATH                 Path to the PromptML(.pml) file  [required]
  -m, --model TEXT                Model to use for the completion
  -s, --serializer [xml|json|yaml]
                                  Serializer to use for the completion.
                                  Default is `xml`
  -p, --provider [openai|google|ollama]
                                  GenAI provider to use for the completion.
                                  Default is `openai`
  --no-stream                     Get whole GenAI response. Default is
                                  streaming response.
  --raw                           Return raw output from LLM (best for saving
                                  into files or piping)
  --help                          Show this message and exit.

For more details of composing PromptML files, visit: https://promptml.org/
```
## Example

1. Create a PromptML file `character.pml` with the following content:

```promptml
@prompt
    @context
        You are a millitary general in Roman army.
    @end

    @objective
        Describe a regular day in your life.
    @end

    @instructions
        @step
            Be cheeky and sarcastic.
        @end
    @end

    @category
        Simulation
    @end
@end
```
See PromptML [documentation](https://www.promptml.org/) for more details about the syntax.

2. Set your OpenAI API key as an environment variable:

```bash
export OPEN_AI_API_KEY=your-openai-api-key
```

or if you are using Google GenAI.

```bash
export GOOGLE_API_KEY=your-google-api-key
```
or if you are using Local Ollama GenAI, No API key is required.

3. Run the PromptML file with the following command in terminal:

```bash
procli -f character.pml -p ollama -m phi3
```

You will see the respective output on terminal:

```info
Ah, so you want a glimpse into the life of a Roman general, do you? Well, let me spin you a tale, dripping with sarcasm and cheeky remarks, because obviously, my life is a walk in the park. Shall we?

The day usually starts with the soothing sounds of soldiers clanging their swords and shields together at some ungodly hour. Rather than waking up to the gentle cooing of doves, I get to hear the charming war cries of recruits who still can't tell their gladius from their left foot. Delightful, isn't it?

After I drag myself out of what I'm convinced is a sack filled with rocks they call a bed, it's straight to the strategy tent. Here, I enjoy the riveting discussions about which barbarian horde is threatening our borders this week. It's like choosing the lesser of two evils: invasions from the north or mutiny from the ranks. Decisions, decisions!

Next on the agenda is overseeing training. Oh yes, I just love watching greenhorns stumble through basic drills. The way they handle their weapons – you'd think a lopsided stick had suddenly become the deadliest thing in their hands. But hey, a general's got to humor them, right?

Then there's the daily feast of dried meat and stale bread, washed down with wine that's likely been used as paint thinner. Ah, the joys of Roman culinary delights. I'm sure Bacchus himself is weeping with laughter somewhere.

Afternoons are reserved for dealing with the Senate's missives, those beautifully crafted scrolls filled with ‘helpful’ suggestions and veiled threats. It's like mail time with a hint of doomsday. And who can forget the thrill of addressing the legion, trying to maintain morale while standing in armor that weighs more than some of the new recruits?

As evening falls, I get to review the day's progress with my centurions, who conveniently bring me the freshest of problems right before bedtime. If I’m lucky, I'll dodge an assassination attempt or two – keeps life exciting, don’t you think?

Finally, I retire for the night, eager to wake up and do it all over again. Really, what's not to love? So there you have it! Just another average day in the life of a Roman general – a blend of strategy, sarcasm, and just a dash of masochism.

Time taken: 26.04 seconds
```

## Streaming & Non-streaming Responses

By default, procli streams the response from the GenAI model. You can force CLI tool to collect whole response by using the `--no-stream` flag.


```bash
# Streaming response
promptml-cli -f character.pml -p google
```

```bash
# Non-streaming response
promptml-cli -f character.pml -p google --no-stream
```

## Raw Output

You can also get the raw output from the GenAI model by using the `--raw` flag. This will return the raw output from the model without any formatting.

```bash
# Raw Markdown output
promptml-cli -f character.pml -p openai --raw
```

Note: Raw output is useful when you want to save the output to a file or pipe it to another command.

## TODO
- Add support for Claude, Cohere & A21 Labs GenAI models
- Add tests
