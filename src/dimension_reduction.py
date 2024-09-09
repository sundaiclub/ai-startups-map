from sklearn.manifold import TSNE
from sklearn.decomposition import PCA

def reduce_dimensions(embeddings):
    tsne = TSNE(n_components=2, random_state=0, perplexity=50)
    return tsne.fit_transform(embeddings)

# def reduce_dimensions(embeddings):
#     pca = PCA(n_components=2, svd_solver='full', random_state=0)
#     return pca.fit_transform(embeddings)
