"""
Code for interacting with LLMs.
"""
from openai import AsyncOpenAI
from pydantic import BaseModel

from flashcards_builder.settings import TOKEN_LIMIT
from flashcards_builder.tokens import truncate_text


class LLM:
    def __init__(
        self,
        system_prompt: str | None = None,
        model: str = "gpt-4.1",
        response_format: type[BaseModel] | None = None,
        token_limit: int = TOKEN_LIMIT,
    ):
        self.client = AsyncOpenAI()
        self.system_prompt = system_prompt
        self.model = model
        self.response_format = response_format
        self.token_limit = token_limit

    async def __call__(self, message: str):
        messages = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        messages.append({"role": "user", "content": truncate_text(message, self.token_limit)})
        if self.response_format:
            response = await self.client.chat.completions.parse(
                messages=messages,
                model=self.model,
                response_format=self.response_format,
            )
            return response.choices[0].message.parsed
        else:
            response = await self.client.chat.completions.create(
                messages=messages, model=self.model
            )
            return response.choices[0].message.content


class ListResponseModel(BaseModel):
    items: list[str]
