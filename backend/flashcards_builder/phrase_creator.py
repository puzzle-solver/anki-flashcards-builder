"""
Code for creating the phrases for flashcards

1. User provides a set of keywords based on which to scrape the Internet
2. LLM generates queries for Google search based on the keywords
3. For each query, we scrape Internet websites
4. From each website we extract useful phrases
5. We translate each phrase to English
6. We add additional explanation of LLM of the phrase
"""

import asyncio
import logging
import time
from dataclasses import dataclass

import googlesearch

from flashcards_builder.llm import LLM, ListResponseModel
from flashcards_builder.web_scraping import parse_url, Website
from flashcards_builder.settings import LLM_TIMEOUT, MAX_CONCURRENCY


logger = logging.getLogger(__name__)

query_llm = LLM(
    "Given a keyword provided by a user, please provide 10 queries to a Google search engine about that "
    "subject. Return responses in Italian",
    response_format=ListResponseModel,
)

phrase_llm = LLM(
    "You are a tutor for an Italian language. "
    "Given a text, return a list of at most 20 useful phrases for a language learner. "
    "Phrases should be short, no more than a 10 words. "
    "Only extract phrases in Italian. If there are None, return an empty list."
    "Return exact phrases from the text, without any modifications (including punctuation)",
    response_format=ListResponseModel,
)

translator_llm = LLM("Given a text in Italian, translate it to English.")

tutor_llm = LLM(
    f"The user provides you with a phrase in Italian and the corresponding English translation."
    f"Explain the phrase and give alternatives if possible. Return just the explanation and alternatives"
)

semaphore = asyncio.Semaphore(MAX_CONCURRENCY)


async def timed_llm_call(llm: LLM, message: str, timeout: int = LLM_TIMEOUT, name: str = ""):
    """
    Waits a `timeout` seconds for calling an llm with a given message. In case of a TimeoutError, returns None.
    """
    try:
        async with asyncio.timeout(timeout), semaphore:
            logger.info("Started calling an LLM")
            start = time.time()
            response = await llm(message)
            total = time.time() - start
            logger.info(f"Finished calling an LLM with a time of {total:.2f} s.")
            return response
    except TimeoutError:
        logger.warning(f"Call to llm {name} timed-out with a timeout of: {timeout}. Returning None")

        return None


@dataclass
class Phrase:
    phrase: str
    translation: str
    explanation: str
    url: str
    query: str | None = None
    keyword: str | None = None


async def create_phrases_from_website(website: Website):
    phrases_response = await phrase_llm(website.text)
    phrases_items = phrases_response.items
    translations = await asyncio.gather(
        *[timed_llm_call(translator_llm, phrase) for phrase in phrases_items]
    )
    combined_texts = [
        f"English: {translation} \n\n --- \n\n Italian: {phrase}"
        for translation, phrase in zip(translations, phrases_items)
    ]
    explanations = await asyncio.gather(*[timed_llm_call(tutor_llm, text) for text in combined_texts])

    return [
        Phrase(phrase, translation, explanation, website.url)
        for phrase, translation, explanation in zip(
            phrases_items, translations, explanations
        )
        if translation is not None and explanation is not None
    ]


async def extract_websites_from_query(query: str, num_websites: int):
    urls = list(googlesearch.search(query, num_results=num_websites, unique=True, lang="it"))
    urls = [url for url in urls if url.startswith("http://") or url.startswith("https://")]
    texts = await asyncio.gather(*[
        parse_url(url) for url in urls
    ])
    websites = [Website(url=url, text=text) for url, text in zip(urls, texts) if text is not None]
    return websites


async def create_phrases_from_query(query: str, num_websites: int):
    """
    :param query: query to a search engine
    :param num_websites: number of websites to search for each query
    :return: a list of extracted phrases for the query from multiple websites
    """
    websites = await extract_websites_from_query(query, num_websites)
    phrases_list = await asyncio.gather(*[
        create_phrases_from_website(website) for website in websites
    ])
    phrases = [phrase for phrases in phrases_list for phrase in phrases]
    for phrase in phrases:
        phrase.query = query
    return phrases


async def create_queries(keyword: str):
    queries_response = await query_llm(keyword)
    queries = queries_response.items
    return queries


async def create_phrases(keyword: str, num_websites: int = 10):
    queries = await create_queries(keyword)
    phrases_list = await asyncio.gather(*[
        create_phrases_from_query(query, num_websites=num_websites) for query in queries
    ])
    phrases = [phrase for phrases in phrases_list for phrase in phrases]
    for phrase in phrases:
        phrase.keyword = keyword
    return phrases
