"""
Code for scraping URLs.
"""
import logging
from dataclasses import dataclass

import httpx
from bs4 import BeautifulSoup


logger = logging.getLogger(__name__)


@dataclass
class Website:
    url: str
    text: str


async def parse_url(url: str) -> str | None:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    if soup.body is None:
        logger.warning(f"Could not find a body for url: {url}")
        return None
    return soup.body.get_text().strip()
