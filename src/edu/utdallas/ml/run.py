from embeddings import GloveEmbedding

from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.preprocessing.text import Tokenizer
from keras import backend as K

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, precision_recall_fscore_support

from collections import OrderedDict

import numpy as np

seed = 7
np.random.seed(seed)
ID_TEXT_DELIMITER = " <:sep:> "

print("Using # GPU's: ", K.tensorflow_backend._get_available_gpus())

"""
    0. initialize twitter word embeddings
"""
glove = GloveEmbedding(name="twitter", d_emb=50,  show_progress=True)

"""
    1. Index tweets and it labels for error analysis
"""
labels = OrderedDict()
tweets = OrderedDict()
fp = open("../../../../resources/n-tweets-id_tokens.txt", 'r')
idx = 0
for sample in fp.readlines():
    label, tweet = sample.split(ID_TEXT_DELIMITER)
    if label.strip() == 'YES':
        labels[idx] = 1
    elif label.strip() == 'NO':
        labels[idx] = 0
    tokens_as_string = ''
    for tok in tweet.strip().replace("[", "").replace(']', "").replace("'", "").split(", "):
        tokens_as_string = tokens_as_string + tok + " "
    tweets[idx] = tokens_as_string
    idx = idx + 1
fp.close()

"""
    Keras text preprocessor
"""

# tknzr = Tokenizer()
# tknzr.fit_on_texts(tweets.values())
#
# word_idx = tknzr.word_index
# max_word_idx = max(word_idx.values())
#
# print("Total Number of Unique words", max_word_idx)
#
# words_wo_embd = list()
# for word in word_idx.keys():
#     embd = glove.emb(word)
#     if None in embd:
#         words_wo_embd.append(word)
#
# if len(words_wo_embd) > 0:
#     print("words w/o embd\n", len(words_wo_embd), words_wo_embd)
# else:
#     print("all words have embeddings")
#
# word_idx[":EMPTOK:"] = max_word_idx+1

"""
    Feature Engineering
        - add word embeddings of all words in a sentence -> 50 featured vector
"""
samples_list = list()
labels_list = list()
for idx, tweet in tweets.items():
    sample = np.zeros([50, 1], dtype=np.float32)
    for tok in tweet.split(" "):
        embd = glove.emb(tok)
        if None in embd:
            embd = np.zeros([50, 1], dtype=np.float32)
        else:
            embd = np.asarray(embd)
            embd = embd.reshape([50, 1])
        sample = sample + embd
    x = [[idx]]
    x.extend(sample.tolist())
    samples_list.append(x)
    labels_list.append(labels[idx])

data_set = [np.asarray(samples_list).squeeze(), np.asarray(labels_list)]

print("No of samples X No of features:", data_set[0].shape)
print("No of samples X 1:", data_set[1].shape)

"""
    Neural Net: Train
"""
X_train, X_test, y_train, y_test = train_test_split(data_set[0], data_set[1], test_size=0.30, random_state=seed)

print("Train: No of samples X No of features:", X_train[0:, 1:X_train.shape[1]].shape)
print("Train: No of samples X 1:", y_train.shape)

print("Test: No of samples X No of features:", X_test[0:, 1:X_test.shape[1]].shape)
print("Test: No of samples X 1:", y_test.shape)

BATCH_SIZE = 25
EPOCHS = 1

# configure the model
model = Sequential()
model.add(Dense(30, input_dim=50, activation='sigmoid'))
model.add(Dropout(0.2))
model.add(Dense(15, input_dim=30, activation='sigmoid'))
model.add(Dropout(0.2))
model.add(Dense(5, input_dim=15, activation='sigmoid'))
model.add(Dropout(0.2))
model.add(Dense(1, activation='sigmoid'))
# Compile model
model.compile(loss='binary_crossentropy', optimizer='adadelta', metrics=['accuracy'])
# Train model
model.summary()
model.fit(X_train[0:, 1:X_train.shape[1]], y_train,
          batch_size=BATCH_SIZE,
          epochs=EPOCHS,
          verbose=1)

"""
    Neural Net: Test
"""
y_pred = model.predict_classes(X_test[0:, 1:X_test.shape[1]])

"""
    Neural Net: Stats
"""
precision, recall, f1measure, support = precision_recall_fscore_support(y_test, y_pred, average="binary")

print("\nIs a toxic tweet?\nConfusion Matrix\n", confusion_matrix(y_test, y_pred))
print("Toxic Class: Precision", precision)
print("Toxic Class: Recall", recall)
print("Toxic Class: F1-Measure", f1measure)

"""
    Neural Net: Error Analysis
"""
for idx in range(y_pred.shape[0]):
    if y_pred[idx] != y_test[idx]:
        print("Ground Truth: ", y_test[idx], " prediction: ", y_pred[idx], " tweet: ", tweets[X_test[idx, 0]])
