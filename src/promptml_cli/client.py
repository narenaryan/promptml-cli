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

class Provider(enum.Enum):
    """GenAI provider enum class."""
    OPENAI = "openai"
    GOOGLE = "google"

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

        return None
