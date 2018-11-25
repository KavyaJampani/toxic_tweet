import pandas as pd
import nltk
from nltk.tokenize import TweetTokenizer
import json as js
import re


# take 10000 tweets from the collected tweets

# fp = open("../../../../resources/tweets1.json", "r")
#
# c = 0
# fp1 = open("../../../../resources/tweets_10k.txt", "w")
# for tweet in fp.readlines():
#     if c <= 10000:
#         fp1.write(tweet)
#     else:
#         fp1.close()
#     c = c + 1
# fp.close()


# #preprocess the data
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


fp2 = open("../../../../resources/tweets_10k_id_text.txt", "w")
tweets_file = open("../../../../resources/tweets_10k.txt", 'r')
for twt in tweets_file.readlines():
    if len(twt.strip()) > 0:
        tweet = js.loads(twt.strip().replace('\n', " ").replace('\r', ''))
        try:
            fp2.write(str(tweet["id"])+ " text: "+ pre_process(tweet["text"]))
            fp2.write("\n")
        except KeyError as e:
            print("Bad Tweet!! " + twt)
fp2.close()


# #tokenize the data

# def tokenize(txt):
#     stopwords = nltk.corpus.stopwords.words("english")
#     other_exclusions = ["#ff", "ff", "rt"]
#     stopwords.extend(other_exclusions)
#     tr = TweetTokenizer()
#     words = tr.tokenize(txt)
#     ref_words = [word for word in words if word not in stopwords]
#     return ref_words
#
#
# fp2 = open("../../../../resources/tweets_10k_id_text.txt", "r")
# final_tweet = dict()
# for line in fp2.readlines():
#     items = line.split(" text:")
#     final_tweet[items[0]] = tokenize(items[1])
# print(final_tweet)

