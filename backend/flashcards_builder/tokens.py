from functools import lru_cache

import tiktoken


@lru_cache(maxsize=1)
def _get_encoding():
    return tiktoken.get_encoding("cl100k_base")


def count_tokens(text):
    encoding = _get_encoding()
    return len(encoding.encode(text))


def truncate_text(text: str, token_limit: int | None) -> str:
    if len(text) == 0 or token_limit is None:
        return text
    encoding = _get_encoding()
    tokens = encoding.encode(text)
    return encoding.decode(tokens[:token_limit])
