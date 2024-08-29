from src.llm_interface import CohereAIProvider, OpenAIProvider
# from ../src/llm_interface import CohereAIProvider, OpenAIProvider


def test_cohere_object_is_instantiated():
    dut = CohereAIProvider()
    assert isinstance(dut, CohereAIProvider)


def test_openai_object_is_instantiated():
    dut = OpenAIProvider()
    assert isinstance(dut, OpenAIProvider)
