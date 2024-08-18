import json
from embedding import EmbeddingModel
from vector_store import VectorStore


def ingest_and_store_rules(rules_file, vector_store_file):
    embedding_model = EmbeddingModel()
    vector_store = VectorStore(embedding_model.model.get_sentence_embedding_dimension())

    with open(rules_file, "r") as f:
        rules = json.load(f)

    for rule in rules:
        text = prepare_rule_text(rule)
        vector = embedding_model.embed(text)
        vector_store.add(vector, text)

    vector_store.build()
    vector_store.save(vector_store_file)


def prepare_rule_text(rule):
    # Convert rule dict to string format
    return f"Rule ID: {rule['id']}\nTitle: {rule['title']}\nDescription: {rule['description']}"


if __name__ == "__main__":
    ingest_and_store_rules("social_security_rules.json", "rules_vector_store.ann")
