from ingestor import ingest_json_data
from preprocessor import preprocess_data
from llm_interface import OllamaProvider
from vector_store import VectorStore
from embedding import EmbeddingModel


def prepare_data(data):
    return "\n".join([f"{k}: {v}" for item in data for k, v in item.items()])


def main():
    # Initialize components
    embedding_model = EmbeddingModel()
    vector_store = VectorStore(embedding_model.model.get_sentence_embedding_dimension())
    llm = OllamaProvider()

    # Ingest and process data
    raw_data = ingest_json_data("sandy_sample.json")
    processed_data = preprocess_data(raw_data)

    # Embed and store data
    for _, item in enumerate(processed_data):
        text = prepare_data([item])
        vector = embedding_model.embed(text)
        vector_store.add(vector, text)
    vector_store.build()

    # Example query
    query = "What are the retirement prospects for this couple based on their earnings history and estimated benefits?"
    query_vector = embedding_model.embed(query)
    relevant_data = vector_store.search(query_vector)

    # Analyze with LLM
    context = "\n\n".join(relevant_data)
    analysis_result = llm.analyze(query, context)

    # Output results
    print("Query:", query)
    print("\nLLM Analysis Results:")
    print(analysis_result)


if __name__ == "__main__":
    main()
