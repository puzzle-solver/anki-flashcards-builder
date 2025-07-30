import pytest

from src.phrase_creator import translator_llm, tutor_llm


@pytest.mark.asyncio
async def test_translator_llm():
    output = await translator_llm("ridere")
    assert "laugh" in output.lower()


@pytest.mark.asyncio
async def test_tutor_llm():
    output = await tutor_llm('Italian: "parere". \n\nEnglish: "to seem like"')
    assert "sembrare" in output.lower()
