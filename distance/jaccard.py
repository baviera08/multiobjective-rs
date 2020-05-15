import numpy as np
from scipy.sparse import csr_matrix


def jaccard_similarities(mat):
    # https://na-o-ys.github.io/others/2015-11-07-sparse-vector-similarities.html
    cols_sum = mat.getnnz(axis=0)
    ab = mat.T * mat

    # for rows
    aa = np.repeat(cols_sum, ab.getnnz(axis=0))
    # for columns
    bb = cols_sum[ab.indices]

    similarities = ab.copy()
    similarities.data /= (aa + bb - ab.data)

    return similarities


def calculate_distance_matrix_jaccard(csr, epsilon=1.9999):
    """Computes the Jaccard distance between the rows of `csr`,
    smaller than the cut-off distance `epsilon`.
    """
    # assert(0 < epsilon < 1)
    assert (0 < epsilon < 2)
    csr = csr_matrix(csr).astype(bool).astype(int)

    csr_rownnz = csr.getnnz(axis=1)
    intrsct = csr.dot(csr.T)

    nnz_i = np.repeat(csr_rownnz, intrsct.getnnz(axis=1))
    unions = nnz_i + csr_rownnz[intrsct.indices] - intrsct.data
    dists = 1.0 - intrsct.data / unions

    mask = (dists > 0) & (dists <= epsilon)
    data = dists[mask]
    indices = intrsct.indices[mask]

    rownnz = np.add.reduceat(mask, intrsct.indptr[:-1])
    indptr = np.r_[0, np.cumsum(rownnz)]

    out = csr_matrix((data, indices, indptr), intrsct.shape)
    return out

# def calculate_distance_matrix_jaccard(dataset):
#     matrix_csc = dataset.T.tocsc()
#     similarity_matrix = jaccard_similarities(matrix_csc)
#     return similarity_matrix




# def calculate_distance_matrix_jaccard(X):
#     """Computes the Jaccard distance between the rows of `X`.
#     """
#     X = X.astype(bool).astype(float)
#
#     intrsct = X.dot(X.T)
#     row_sums = intrsct.diagonal()
#     unions = row_sums[:,None] + row_sums - intrsct
#     dist = 1.0 - intrsct / unions
#     return dist
