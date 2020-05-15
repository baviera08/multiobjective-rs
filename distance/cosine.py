import time
import logging
from implicit.nearest_neighbours import (CosineRecommender)

def calculate_distance_matrix(dataset):
    logging.debug("Calculating similar items matrix. This might take a while")
    # generate a recommender model based off the input params
    model = CosineRecommender()
    # train the model
    logging.debug("calculating distant matrix")
    start = time.time()
    model.fit(dataset)
    similarity_matrix = model.similarity
    logging.debug("trained model '%s' in %s", 'cosine', time.time() - start)

    return similarity_matrix
