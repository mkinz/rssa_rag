from annoy import AnnoyIndex
import json


class VectorStore:
    def __init__(self, dimension):
        self.dimension = dimension
        self.index = AnnoyIndex(dimension, "angular")
        self.id_to_text = {}
        self.current_id = 0

    def add(self, vector, text):
        self.index.add_item(self.current_id, vector)
        self.id_to_text[self.current_id] = text
        self.current_id += 1

    def build(self, n_trees=10):
        self.index.build(n_trees)

    def search(self, query_vector, k=5):
        indices, distances = self.index.get_nns_by_vector(
            query_vector, k, include_distances=True
        )
        return [self.id_to_text[str(i)] for i in indices]

    def save(self, file_path):
        # Save the Annoy index
        self.index.save(f"{file_path}.ann")

        # Save the metadata (id_to_text mapping and current_id)
        metadata = {
            "id_to_text": self.id_to_text,
            "current_id": self.current_id,
            "dimension": self.dimension,
        }
        with open(f"{file_path}.json", "w") as f:
            json.dump(metadata, f)

    @classmethod
    def load(cls, file_path):
        # Load the metadata
        with open(f"{file_path}.json", "r") as f:
            metadata = json.load(f)

        # Create a new VectorStore instance
        vector_store = cls(metadata["dimension"])

        # Load the Annoy index
        vector_store.index.load(f"{file_path}.ann")

        # Restore the metadata
        vector_store.id_to_text = metadata["id_to_text"]
        vector_store.current_id = metadata["current_id"]

        return vector_store
