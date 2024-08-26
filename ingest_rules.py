import json
from embedding import EmbeddingModel
from vector_store import VectorStore


def ingest_and_store_rules(rules_file, vector_store_file):
    embedding_model = EmbeddingModel()
    vector_store = VectorStore(embedding_model.model.get_sentence_embedding_dimension())

    with open(rules_file, "r") as f:
        rules_data = json.load(f)

    for rule_id, rule_text in rules_data["id_to_text"].items():
        text = prepare_rule_text(rule_id, rule_text)
        vector = embedding_model.embed(text)
        vector_store.add(vector, text)

    vector_store.build()
    vector_store.save(vector_store_file)


def prepare_rule_text(rule_id, rule_text):
    # The rule_text is already formatted, so we can return it as is
    return rule_text


if __name__ == "__main__":
    ingest_and_store_rules("rules_vector_store.json", "rules_vector_store.ann")
