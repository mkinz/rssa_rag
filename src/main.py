import time
from logging_config import setup_logging
from valid_html import NotValidHTMLException, validate_llm_html
from vector_store import VectorStore
from embedding import EmbeddingModel
from llm_interface import (
    CohereAIProvider,
    LLMProvider,
    OllamaProvider,
    OpenAIProvider,
    AnthropicProvider,
)
from roadmap_output_ingestor import preprocess_roadmap_output

logger = setup_logging()


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        logger.info(f"{method.__name__} took {te - ts:.2f} seconds")
        return result

    return timed


@timeit
def load_vector_store(file_path):
    return VectorStore.load(file_path)


@timeit
def embed_user_data(embedding_model: EmbeddingModel, user_data):
    return embedding_model.embed(user_data)


@timeit
def search_relevant_rules(vector_store: VectorStore, user_vector):
    return vector_store.search(user_vector)


@timeit
def analyze_with_llm(llm, query, context):
    return llm.analyze(query, context)


def main():
    logger.info("Starting main function")

    llm_stragegy = {
        "openai": OpenAIProvider(),
        "anthropic": AnthropicProvider(),
        "ollama": OllamaProvider(),
        "cohere": CohereAIProvider(),
    }

    llm: LLMProvider = llm_stragegy["openai"]

    logger.info(f"Using {llm}")

    try:
        user_data: str = preprocess_roadmap_output("client-exports/norton.json")
    except Exception as e:
        logger.error(f"Error preprocessing user data: {e}")
        return

    """
    # The following code block is used to create the elements needed for RAG:
    # embedding model, vector_store, user_vector, relevant_rules.
    # The vector_store is generated using the rules_ingestor.py script along with a rules.json file.

    embedding_model = EmbeddingModel()

    try:
        vector_store = load_vector_store("rules_vector_store")
    except FileNotFoundError as e:
        logger.error(f"Error loading vector store: {e}")
        return

     user_vector = embed_user_data(embedding_model, user_data)
     relevant_rules = search_relevant_rules(vector_store, user_vector)

    context = f"User Data:\n{user_data}\n\nRelevant Rules:\n" + "\n\n".join(
        relevant_rules
    )
    """

    context = f"User Data:\n{user_data}\n"

    query = """
    Based on the provided user data for both the primary beneficiary and spouse, and the relevant Social Security rules, please provide:
    1. A summary of both individuals' work history and earnings.
    2. An analysis of their estimated Social Security benefits, including any spousal benefits they might be eligible for.
    3. Recommendations for optimizing their Social Security benefits as a couple.
    4. Any additional insights or considerations based on their specific situation, including the age difference between the spouses and their respective earnings histories.
    5. Any insights related to their dependents, if any.
    6. Note any specific rules that you are referencing in your analysis.

    """

    analysis_result = analyze_with_llm(llm, query, context)
    validated: tuple = validate_llm_html(analysis_result)

    if validated[0] is True:
        logger.info("HTML was validated!")
    else:
        logger.error("HTML Validation failed. LLM returned invalid html.")
        logger.error(validated[1])
    logger.info(analysis_result)

    logger.info("Main function completed")


if __name__ == "__main__":
    main()
