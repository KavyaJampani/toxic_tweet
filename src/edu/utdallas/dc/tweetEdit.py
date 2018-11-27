import nltk
from nltk.tokenize import TweetTokenizer
import json as js
import re
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

ID_TEXT_DELIMITER = " <:sep:> "

"""
    Take 10000 tweets from the collected tweets
"""

def write_n_tweets(n, raw_tweets_file):
    raw_tweets_ = open(raw_tweets_file, "r")
    c = 0
    n_tweets_ = open("../../../../resources/n-raw-tweets.txt", "w")
    for tw in raw_tweets_.readlines():
        if c <= n:
            n_tweets_.write(tw)
        else:
            n_tweets_.close()
        c = c + 1
    raw_tweets_.close()


def keywords():
    fp = open("../../../../resources/keywords.txt", "r")
    words = [w.strip() for w in fp.readlines() if w.strip() is not None and len(w.strip()) > 0]
    return words

def write_n_ntweets(n, raw_tweets_file):
    raw_tweets_ = open(raw_tweets_file, "r")
    c = 0
    id_text_ = open("../../../../resources/n-ntweets-id_text.txt", "w", encoding='utf-8')
    words = keywords()
    for twt in raw_tweets_.readlines():
         if len(twt.strip()) > 0:
                 tweet = js.loads(twt.strip().replace('\n', " ").replace('\r', ''))
                 try:
                     toxic = 0
                     tweet_words = tweet["text"].split("\\s")
                     for k in tweet_words:
                         for x in words:
                             if k == x:
                                 toxic = 1
                     if toxic == 0:
                        id_text_.write(str(tweet["id"]) + ID_TEXT_DELIMITER + "NO" + ID_TEXT_DELIMITER + pre_process(tweet["text"]))
                        id_text_.write("\n")
                        c = c+1
                     if c>=n:
                         break
                 except KeyError as e:
                     print("Bad Tweet!! " + twt)
    id_text_.close()
    raw_tweets_.close()
"""
pre process the data
"""


def pre_process(text):
    #remove special characters
    text = re.compile(r'[^a-z\d ]',re.IGNORECASE).sub('',text)

    #remove spaces
    space_pattern = '\s+'
    text = re.sub(space_pattern, ' ', text)

    #remove urls
    giant_url_regex = ('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|'
         '[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    text = re.sub(giant_url_regex, ' ',text)

    #remove numbers
    text = re.compile(r'\d+',re.IGNORECASE).sub('n',text)

    #remove stem words
    text = text.split()
    stemmer = SnowballStemmer('english')
    stemmed_words = [stemmer.stem(word) for word in text]
    text = " ".join(stemmed_words)

    return text


"""
    Tokenize a tweet
"""


def tokenize(tweet_text):
    stopwords = None
    try:
        stopwords = nltk.corpus.stopwords.words("english")
        other_exclusions = ["#ff", "ff", "rt"]
        stopwords.extend(other_exclusions)
    except LookupError as lue:
        nltk.download('stopwords')

    tr = TweetTokenizer()
    words = tr.tokenize(tweet_text)
    tweet_words = [word for word in words if word not in stopwords]
    return tweet_words


"""
    Extract Id, text from raw tweets
"""


def extract_and_write_id_text_to_file(n_tweets_file):
    id_text_ = open("../../../../resources/n-tweets-id_text.txt", "w", encoding='utf-8')
    n_tweets_ = open(n_tweets_file, 'r')
    for twt in n_tweets_.readlines():
        if len(twt.strip()) > 0:
            tweet = js.loads(twt.strip().replace('\n', " ").replace('\r', ''))
            try:
                id_text_.write(str(tweet["id"]) + ID_TEXT_DELIMITER + "YES" + ID_TEXT_DELIMITER + pre_process(tweet["text"]) )
                id_text_.write("\n")
            except KeyError as e:
                print("Bad Tweet!! " + twt)
    id_text_.close()
    n_tweets_.close()


"""
    Tokenize tweets using nltk
"""


def tokenize_tweets(id_text_file):
    id_text_ = open(id_text_file, "r", encoding='utf-8')
    id_tokens_ = open("../../../../resources/n-tweets-id_tokens.txt", 'w', encoding='utf-8')
    for txt in id_text_.readlines():
        parts = txt.split(ID_TEXT_DELIMITER)
        if parts is not None and len(parts):
            tokens = tokenize(parts[1])
            print(parts[0], ID_TEXT_DELIMITER, tokens, file=id_tokens_)

def merge_files():
    filenames = ['../../../../resources/n-ntweets-id_text.txt','../../../../resources/n-tweets-id_text.txt']
    with open('../../../../resources/final_tweets-id_text.txt', 'w') as outfile:
        for fname in filenames:
            with open(fname) as infile:
                for line in infile:
                    outfile.write(line)
"""
    Main Method
"""
if __name__ == '__main__':
    write_n_tweets(100, "../../../../resources/tweets1.json")
    write_n_ntweets(100,"../../../../resources/tweets2.json")
    extract_and_write_id_text_to_file("../../../../resources/n-raw-tweets.txt")
    merge_files()
    tokenize_tweets("../../../../resources/final_tweets-id_text.txt")
