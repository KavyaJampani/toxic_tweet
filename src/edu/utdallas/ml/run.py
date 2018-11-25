from embeddings import GloveEmbedding

# 1. Prepare data set
#   - read tweets from file
#   - clean them using nltk
#   - follow usual text clean up mechanisms used in nlp (see kaggle toxic tweet challenge kernels)

# 2. Pre processing
#   - read Glove word embeddings
glove = GloveEmbedding(name="twitter", d_emb=50,  show_progress=True)
print(glove.emb("stanford"))
#   - represent tweets as matrices{ 3D matrix (wemd_size x max_tweet_length x #ofexamples)} using word embeddings
#   - provide ground truth for each tweet (toxic(1)/non-toxic(0))
#   - prefix/suffix each tweet to make it constant length.
#   - divide the data into train/valid/test data sets(70/10/20(%'s))

# 3. Train Stage
#   - compose NN architecture using keras
#   - train the model on the train data and validate on valid data

# 4. Inference stage
#   - load the saved models
#   - infer on test data
#       - get probabilities and predicted labels

# 5. Analysis
#    - confusion matrix
