import pandas as pd
import nltk
from nltk.tokenize import TweetTokenizer
import json as js
import re

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


"""
pre process the data
"""


def pre_process(text_string):
    """
    Accepts a text string and replaces:
    1) urls with URLHERE
    2) lots of whitespace with one instance
    3) mentions with MENTIONHERE

    This allows us to get standardized counts of urls and mentions
    Without caring about specific people mentioned
    """
    space_pattern = '\s+'
    giant_url_regex = ('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|'
        '[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    mention_regex = '@[\w\-]+'
    parsed_text = re.sub(space_pattern, ' ', text_string)
    parsed_text = re.sub(giant_url_regex, ' ', parsed_text)
    parsed_text = re.sub(mention_regex, ' ', parsed_text)
    return parsed_text


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
                id_text_.write(str(tweet["id"]) + ID_TEXT_DELIMITER + pre_process(tweet["text"]))
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


"""
    Main Method
"""
if __name__ == '__main__':
    write_n_tweets(100, "../../../../resources/raw-tweets.json")
    extract_and_write_id_text_to_file("../../../../resources/n-raw-tweets.txt")
    tokenize_tweets("../../../../resources/n-tweets-id_text.txt")
