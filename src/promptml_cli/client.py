
import os
import enum
from typing import Union

from openai import OpenAI
import google.generativeai as genai


class Provider(enum.Enum):
    OPENAI = "openai"
    GOOGLE = "google"

class ClientFactory:
    def __init__(self, provider: str, model: str=""):
        self.provider = provider
        self.model = model

    def get_client(self) -> Union[OpenAI, genai.GenerativeModel, None]:
        if self.provider == Provider.OPENAI.value:
            return OpenAI(
                api_key=os.environ.get("OPENAI_API_KEY"),
            )
        elif self.provider == Provider.GOOGLE.value:
            genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
            return genai.GenerativeModel(self.model)
        else:
            return None
