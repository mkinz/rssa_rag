from annoy import AnnoyIndex


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
        return [self.id_to_text[i] for i in indices]
