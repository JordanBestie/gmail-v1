"""Util that calls Google Search."""
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Extra, root_validator

from langchain.utils import get_from_dict_or_env
from langchain.llms.loading import load_llm
from langchain.llms.openai import OpenAI


class GmailAPIWrapper(BaseModel):

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid

    def _write_new_mail(self,content: str) -> str:
        try:
            llm = OpenAI(engine="text-davinci-003",temperature=0.71,
                    max_tokens=150,top_p=1,frequency_penalty=0.36,presence_penalty=0.75)
            response = llm(content)
            return response
        except Exception as e:
            print(e)

    def _write_response_mail(self, content: str) -> str:
        try:
            llm = OpenAI(temperature=0.71,
                             max_tokens=150, top_p=1, frequency_penalty=0.36, presence_penalty=0.75)
            response = llm(content)
            return response
        except Exception as e:
            print(e)


    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that api key and python package exists in environment."""
        openai_api_key = get_from_dict_or_env(
            values, "openai_api_key", "OPENAI_API_KEY"
        )
        try:
            import openai

            openai.api_key = openai_api_key
            values["client"] = openai.Completion
        except ImportError:
            raise ValueError(
                "Could not import openai python package. "
                "Please it install it with `pip install openai`."
            )
        return values