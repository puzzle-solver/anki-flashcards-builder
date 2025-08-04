import pytest

from flashcards_builder.web_scraping import parse_url


@pytest.mark.asyncio
async def test_parse_url():
    output = await parse_url("https://www.wikipedia.org")
    assert "Wikipedia" in output
