from sklearn.manifold import TSNE

def reduce_dimensions(embeddings):
    tsne = TSNE(n_components=2, random_state=0, perplexity=2)
    return tsne.fit_transform(embeddings)
