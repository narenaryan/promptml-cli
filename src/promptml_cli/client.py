"""GenAI client module."""

import os
import enum
from typing import Union

from openai import OpenAI
import google.generativeai as genai

class Model(enum.Enum):
    """GenAI model enum class."""
    GPT_4O = "gpt-4o"
    GEMINI_1_5_FLASH_LATEST = "gemini-1.5-flash-latest"
    PHI_3 = "phi3"
    LLAMA_3 = "llama3"

class Provider(enum.Enum):
    """GenAI provider enum class."""
    OPENAI = "openai"
    GOOGLE = "google"
    OLLAMA = "ollama"

class ClientFactory:
    """GenAI client factory class."""
    def __init__(self, provider: str, model: str=""):
        self.provider = provider
        self.model = model

    def get_client(self) -> Union[OpenAI, genai.GenerativeModel, None]:
        """Get the client based on the provider."""
        if self.provider == Provider.OPENAI.value:
            return OpenAI(
                api_key=os.environ.get("OPENAI_API_KEY"),
            )
        if self.provider == Provider.GOOGLE.value:
            genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
            return genai.GenerativeModel(self.model)

        if self.provider == Provider.OLLAMA.value:
            return OpenAI(
                base_url = 'http://localhost:11434/v1',
                api_key='ollama', # required, but unused
            )

        return None
