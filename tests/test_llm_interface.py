from src.llm_interface import (
    CohereAIProvider,
    OpenAIProvider,
    OllamaProvider,
    AnthropicProvider,
)


def test_cohere_object_is_instantiated():
    dut = CohereAIProvider()
    assert isinstance(dut, CohereAIProvider)


def test_openai_object_is_instantiated():
    dut = OpenAIProvider()
    assert isinstance(dut, OpenAIProvider)


def test_ollama_object_is_instantiated():
    dut = OllamaProvider()
    assert isinstance(dut, OllamaProvider)


def test_anthropic_object_is_instantiated():
    dut = AnthropicProvider()
    assert isinstance(dut, AnthropicProvider)
