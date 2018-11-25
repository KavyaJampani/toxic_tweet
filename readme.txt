Steps to set up the python virtual env for this project
+++++++++++++++++++++++++++++++++++++++++++++++++++++++
1. create a conda based virtual env using pycharm or follow below steps
    1. conda create -n toxic-tweets python=3.6
    2. source activate toxic-tweets
    3. conda/pip install tensorflow keras pandas embeddings
2. If above steps are followed, select the python in the toxic-tweets as your interpreter
3. All the project dependencies should be resolved if above steps are executed correctly.
4. Add HOME=C:\Users\Kavya and EMBEDDINGS_ROOT=C:\Users\Kavya\.embeddings environment variables as local and system.

#setup
 Run tweetCollect to collect the tweets.
 Run tweet Edit to collect 10000 tweets.
 Comment remaining code and run preprocess for preprocessing the data.



# project steps

# 1. Prepare data set
#   - read tweets from file
#   - clean them using nltk
#   - follow usual text clean up mechanisms used in nlp (see kaggle toxic tweet challenge kernels)

# 2. Pre processing
#   - read Glove word embeddings
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