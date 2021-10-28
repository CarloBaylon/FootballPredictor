import re
import string
import numpy as np
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer


#implementation

all_positive_tweets = []
all_negative_tweets = []


def tweet_process(tweet):
    tweet_edited = re.sub(r'^RT[\s]','', tweet)
    
    tweet_edited = re.sub(r'https?:\/\/.*[\r\n]*','', tweet_edited)
    
        
    tokenizer = TweetTokenizer(preserve_case=False,    strip_handles=True, reduce_len=True)
    
    tweet_tokens = tokenizer.tokenize(tweet_edited)    
        
    stopwords_english = stopwords.words('english') 
    
    tweets_clean = []
    for word in tweet_tokens:
        if word not in stopwords_english and word not in string.punctuation:
            tweets_clean.append(word)
        
    stemmer = PorterStemmer()
    
    tweets_stem = []
    for word in tweets_clean:
        stem_word = stemmer.stem(word)
        tweets_stem.append(stem_word)
        
    return tweets_stem


def build_frequencies(tweets, ys):
    yslist = np.squeeze(ys).tolist()
    
    freqs = {}
    for y, tweet in zip(yslist, tweets):
        for word in process_tweet(tweet):
            pair = (word, y)
            freqs[pair] = freqs.get(pair, 0) + 1
            
    return freqs
    
def sigmoid(z): 
    
    h = 1/(1 + np.exp(-z))
    
    return h
    
def gradientDescent(x, y, theta, alpha, num_iterations):
    
    m = len(x)
    try:
        for i in range(0, num_iterations):
        
            z = np.dot(x,theta)
        
            h = sigmoid(z)
        
            J = (-1/m)*(np.dot(y.T,np.log(h)) + np.dot((1-y).T,np.log(1-h)))
        
            theta = theta - (alpha/m)*np.dot(x.T, h-y)
        
        J = float(J)
        return J, theta
    except ZeroDivisionError:
        print("ZeroDivisionError has occurred.")
    
def extract_features(tweet, freqs):

    word_l = process_tweet(tweet)
    
    x = np.zeros((1, 3)) 
    
    x[0,0] = 1 
        
    for word in word_l:
        
        x[0,1] += freqs.get((word,1),0)
        
        x[0,2] += freqs.get((word,0),0)
        
    assert(x.shape == (1, 3))
    return x
    
test_positive = all_positive_tweets[4000:]
train_positive = all_positive_tweets[:4000]
test_negative = all_negative_tweets[4000:]
train_negative = all_negative_tweets[:4000]
train_x = train_positive + train_negative 
test_x = test_positive + test_negative

train_y = np.append(np.ones((len(train_positive), 1)), np.zeros((len(train_negative), 1)), axis=0)
test_y = np.append(np.ones((len(test_positive), 1)), np.zeros((len(test_negative), 1)), axis=0)

X = np.zeros((len(train_x), 3))

for i in range(len(train_x)):
    X[i, :]= extract_features(train_x[i], freqs)
    
Y = train_y
J, theta = gradientDescent(X, Y, np.zeros((3, 1)), 1e-9, 1500)
print(f"The cost after training is {J:.8f}.")
print(f"The resulting vector of weights is {[round(t, 8) for t in np.squeeze(theta)]}")

def predict_tweet(tweet, freqs, theta):
 
    x = extract_features(tweet, freqs)
    
    z = np.dot(x,theta)
    y_pred = sigmoid(z)
    
    
    return y_pred
    
def logistic_regression(x_v, x_y, frequency, theta):

    y_hat = []
    
    for tweet in x_v:
        y_pred = predict_tweet(tweet, frequency, theta)
        
        if y_pred > 0.5:
            y_hat.append(1)
        else:
            y_hat.append(0)
    y_hat = np.array(y_hat)
    x_y = x_y.reshape(-1)
    accuracy = np.sum((x_y == y_hat).astype(int))/len(x_v)
    
    return accuracy
