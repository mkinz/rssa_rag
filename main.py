import json
import logging
from vector_store import VectorStore
from embedding import EmbeddingModel
from llm_interface import OllamaProvider

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def load_vector_store(file_path):
    return VectorStore.load(file_path)


def prepare_user_data(data):
    return "\n".join([f"{k}: {v}" for k, v in data.items()])


def get_user_social_security_data(file_path):
    with open(file_path, "r", encoding="utf-8-sig") as f:
        data = json.load(f)
    return data


"""def get_user_social_security_data():
    # Mock function to return some sample user data
    return {"name": "John Doe", "age": 62, "years_worked": 35, "average_salary": 50000}
        """


def main():
    # Initialize components
    logger.debug("starting main function")
    logger.debug("initializing embedding model")
    embedding_model = EmbeddingModel()

    logger.debug("loading vector store rules")
    vector_store = load_vector_store("rules_vector_store")

    logger.debug("initializing ollama")
    llm = OllamaProvider()

    # Get user data
    logger.debug("getting mocked user data")
    user_data = get_user_social_security_data("sandy_sample.json")

    logger.debug(user_data)
    # Embed user data and retrieve relevant rules
    logger.debug("creating user vector")
    user_vector = embedding_model.embed(prepare_user_data(user_data))
    logger.debug("finding relevant rules")
    relevant_rules = vector_store.search(user_vector)
    logger.debug(relevant_rules)

    # Analyze with LLM
    logger.debug("defining context")
    context = (
        f"User Data:\n{prepare_user_data(user_data)}\n\nRelevant Rules:\n"
        + "\n\n".join(relevant_rules)
    )
    query = "Analyze this user's social security situation based on the provided rules."
    logger.debug("analyzing output")
    analysis_result = llm.analyze(query, context)

    # Output results
    logger.debug("print results to stdout")
    print("User Data:")
    print(json.dumps(user_data, indent=2))
    print("\nAnalysis Results:")
    print(analysis_result)


if __name__ == "__main__":
    main()
