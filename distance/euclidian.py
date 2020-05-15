from scipy import sparse
import sklearn


def calculate_distance_matrix_euclidian(dataset):
    # matrix_csc = dataset.tocsc()

    similarity_matrix = sklearn.metrics.pairwise.pairwise_distances(
        dataset,
        metric='euclidean'
    )
    # convertir a matriz csr
    similarity_matrix = sparse.csr_matrix(similarity_matrix)

    return similarity_matrix

# def calculate_distance_matrix_jaccard(dataset):
#     # matrix_csc = dataset.tocsc()
#
#     similarity_matrix = sklearn.metrics.pairwise.pairwise_distances(
#         dataset,
#         metric='jaccard'
#     )
#     #convertir a matriz csr
#     similarity_matrix = sparse.csr_matrix(similarity_matrix)
#
#     return similarity_matrix

