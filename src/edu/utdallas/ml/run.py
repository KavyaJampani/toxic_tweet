from embeddings import GloveEmbedding


"""
    word embeddings
"""
glove = GloveEmbedding(name="twitter", d_emb=50,  show_progress=True)
print(glove.emb("stanford"))

