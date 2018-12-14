Steps to set up the python virtual env for this project
+++++++++++++++++++++++++++++++++++++++++++++++++++++++
1. create a conda based virtual env using pycharm or follow below steps
    1. conda create -n toxic-tweets python=3.6
    2. source activate toxic-tweets
    3. conda install tensorflow keras pandas
    4. pip install embeddings tweepy sklearn nltk
2. If above steps are followed, select the python in the toxic-tweets as your interpreter
3. All the project dependencies should be resolved if above steps are executed correctly.
4. Add HOME=C:\Users\(USERNAME) and EMBEDDINGS_ROOT=C:\Users\(USERNAME)\.embeddings environment variables as local and system.

# Data Collection and preprocessing
 Run tweetCollect.py in src/edu/utdallas/dc folder to collect the tweets.
 Run tweetPreprocess.py in src/edu/utdallas/dc to preprocess the collected tweets.

# Machine learning models
Run NeuralNetwork.py in src/edu/utdallas/ml/NeuralNetwork.py to run the Neural network model on the processed data.
Run RandomForest.py in src/edu/utdallas/ml/RandomForest.py to run the Random Forest model on the processed data.
Run SVM.py in src/edu/utdallas/ml/SVM.py to run the Neural network model on the processed data.

