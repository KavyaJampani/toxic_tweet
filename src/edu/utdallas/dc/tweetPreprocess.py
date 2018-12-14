import nltk
from nltk.tokenize import TweetTokenizer
import re

ID_TEXT_DELIMITER = " <:sep:> "

"""
pre process the data
"""

def pre_process(text):
    # remove urls
    giant_url_regex = ('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|'
                       '[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    text = re.sub(giant_url_regex, ' ', text)

    #remove special characters
    text = re.compile(r'[^a-z\d ]',re.IGNORECASE).sub('',text)

    #remove spaces
    space_pattern = '\s+'
    text = re.sub(space_pattern, ' ', text)

    #remove numbers
    text = re.compile(r'\d+',re.IGNORECASE).sub('n',text)
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


def write_text_to_file(n_tweets_file,n):
    id_text_ = open("../../../../resources/non-toxic-preprocess.txt", "w", encoding='utf-8')
    n_tweets_ = open(n_tweets_file, 'r',encoding='utf-8')
    c = 0
    for twt in n_tweets_.readlines():
        if len(twt.strip()) > 0:
            if(c > n):
                break
            #tweet = js.loads(twt.strip().replace('\n', " ").replace('\r', ''))
            try:
                id_text_.write("NO" + ID_TEXT_DELIMITER + pre_process(twt) )
                id_text_.write("\n")
                c = c+1
            except KeyError as e:
                print("Bad Tweet!! " + twt)
    id_text_.close()
    n_tweets_.close()


def write_toxic_to_file(n_tweets_file,n):
    id_text_ = open("../../../../resources/toxic-preprocess.txt", "w", encoding='utf-8')
    n_tweets_ = open(n_tweets_file, 'r',encoding='utf-8')
    c = 0
    for twt in n_tweets_.readlines():
        if len(twt.strip()) > 0:
            if(c > n):
                break
            #tweet = js.loads(twt.strip().replace('\n', " ").replace('\r', ''))
            try:
                id_text_.write("YES" + ID_TEXT_DELIMITER + pre_process(twt) )
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
    max_length = 0
    for txt in id_text_.readlines():
        parts = txt.split(ID_TEXT_DELIMITER)
        if parts is not None and len(parts):
            tokens = tokenize(parts[1])
            length_of_token = len(tokens)
            if(length_of_token > max_length):
                max_length = length_of_token
            print(parts[0], ID_TEXT_DELIMITER, tokens, file=id_tokens_)
    print(max_length)


def merge_files():
    filenames = ['../../../../resources/toxic-preprocess.txt', '../../../../resources/non-toxic-preprocess.txt']
    with open('../../../../resources/final_tweets-id_text.txt', 'w') as outfile:
        for fname in filenames:
            with open(fname) as infile:
                for line in infile:
                    outfile.write(line)


"""
    Main Method
"""
if __name__ == '__main__':
    write_text_to_file("../../../../resources/non-toxic-tweets.txts",10000)
    write_toxic_to_file("../../../../resources/toxic-tweets.txt",10000)
    merge_files()
    tokenize_tweets("../../../../resources/final_tweets-id_text.txt")
