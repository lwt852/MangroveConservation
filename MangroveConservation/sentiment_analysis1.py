# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 14:08:10 2020

@author: Mimi Gong
adpted from Meng Cai
"""
"""A few functions for exploratory analysis of text data."""


from sklearn.feature_extraction.text import CountVectorizer
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
import nltk
from spacy.lang.en import English
from nltk.corpus import wordnet as wn
import gensim
from gensim import corpora
import pyLDAvis.gensim
from textblob import TextBlob
nltk.download("stopwords")
nltk.download("wordnet")


def PlotTopWords(text, n, ngram_min=1, ngram_max=1, remove_stop_words=True):
    """
    Plot distribution of top words in text.

    Input: 
    text -- list of text data;
    n -- number of top words/n-grams to display;
    ngram_min -- the minimum value of n-grams (default: 1);
    ngram_max -- the maximum value of n-grams (default: 1);
    remove_stop_words -- whether or not to remove stop words (default: True). 
    Output:
    A plot displaying top n-grams in text.

    Reference:
    https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html
    """
    if remove_stop_words == True:
        vec = CountVectorizer(ngram_range=(
            ngram_min, ngram_max), stop_words="english").fit(text)
        bag_of_words = vec.transform(text)
        sum_words = bag_of_words.sum(axis=0)
        words_freq = [(word, sum_words[0, idx])
                      for word, idx in vec.vocabulary_.items()]
        words_freq = sorted(words_freq, key=lambda x: x[1], reverse=True)
        df = pd.DataFrame(words_freq[:n], columns=["Topwords", "Count"])
        fig, ax = plt.subplots()
        ax.barh(df["Topwords"], df["Count"], color="teal")
        ax.invert_yaxis()
        ax.set_xlabel("Count")
        ax.set_title(
            "Top {} words/ phrases after removing stop words".format(n))
    if remove_stop_words == False:
        vec = CountVectorizer(ngram_range=(
            ngram_min, ngram_max), stop_words=None).fit(text)
        bag_of_words = vec.transform(text)
        sum_words = bag_of_words.sum(axis=0)
        words_freq = [(word, sum_words[0, idx])
                      for word, idx in vec.vocabulary_.items()]
        words_freq = sorted(words_freq, key=lambda x: x[1], reverse=True)
        df = pd.DataFrame(words_freq[:n], columns=["Topwords", "Count"])
        fig, ax = plt.subplots()
        ax.barh(df["Topwords"], df["Count"], color="teal")
        ax.invert_yaxis()
        ax.set_xlabel("Count")
        ax.set_title("Top {} words/ phrases".format(n))
    return ax


def PlotWordCloud(text):
    """
    Generate a wordcloud of text.

    Input:
    text -- list of text data.
    Output:
    A plot displaying wordcloud.

    Reference:
    https://github.com/amueller/word_cloud
    """
    alltext = ','.join(list(text.values))
    wordcloud = WordCloud(background_color='white',
                          max_words=500, contour_color='steelblue')
    wordcloud.generate(alltext)
    return wordcloud.to_image()


def Tokenize(text):
    """
    Break text into tokens.

    Input: 
    text -- list of text data.
    Output: 
    tokens.
    """
    parser = English()
    tokens = parser(text)
    thetokens = []
    for token in tokens:
        if token.orth_.isspace():
            continue
        elif token.like_url:
            thetokens.append('URL')
        elif token.orth_.startswith('@'):
            thetokens.append('SCREEN_NAME')
        else:
            thetokens.append(token.lower_)
    return thetokens


def GetLemma(word):
    """
    Get the semantic root of a given word.

    Input:
    word -- a string.
    Output:
    the root of the word.
    """
    lemma = WordNetLemmatizer().lemmatize(word)
    return lemma


def ProcessToken(sentence):
    """
    Tokenize, remove stopwords, and get lemma of a given sentence.

    Input: 
    sentence -- a string.
    Output: 
    cleaned tokens.
    """
    en_stop = set(nltk.corpus.stopwords.words("english"))
    tokens = Tokenize(sentence)
    clean_tokens = []
    for token in tokens:
        if token not in en_stop:
            clean_tokens.append(GetLemma(token))
    return clean_tokens


def Prepare(text):
    """
    Prepare text for topic modelling.

    Input:
    text -- a list of text data.
    Output: 
    a list of text data ready for topic modelling.
    """
    processedtext = []
    for entry in text:
        processedtext.append(ProcessToken(entry))
    return processedtext


def LDAtopic(text, n_topics=2, n_words=3):
    """
    Find topics in text by Latent Dirichlet Allocation.

    Input:
    text -- list of text data; 
    n_topics -- number of topics to generate;
    n_words -- number of words to display in each topic.
    Output:
    topics found in text, fitted model, corpus, and dictionary.

    Reference:
    https://radimrehurek.com/gensim/models/ldamodel.html
    """
    dictionary = corpora.Dictionary(text)
    corpus = [dictionary.doc2bow(t) for t in text]
    ldamodel = gensim.models.ldamodel.LdaModel(
        corpus, num_topics=n_topics, id2word=dictionary, passes=15)
    topics = ldamodel.print_topics(num_words=n_words)
    return topics, ldamodel, corpus, dictionary


def PlotLDA(model, corpus, dictionary):
    """
    Visualize LDA topic model.

    Input:
    model -- a LDA topic model;
    corpus -- the corpus for modelling;
    dictionary -- the dictionary for modelling.
    Output:
    an interactive LDA model visualization.

    Reference:
    https://pypi.org/project/pyLDAvis/
    """
    lda_display = pyLDAvis.gensim.prepare(
        model, corpus, dictionary, sort_topics=False)
    return pyLDAvis.display(lda_display)


def WhichTopic(text, ldamodel, corpus):
    """
    Find the most likely topic of text.

    Input:
    text -- list of text data;
    ldamodel -- a LDA model built by LDATopic;
    corpus -- a corpus built by LDATopic.
    Output:
    the most likely topic of each piece of text.
    """
    topic = []
    for i in range(len(text)):
        topic_index, topic_value = max(
            ldamodel[corpus[i]], key=lambda item: item[1])
        topic.append(topic_index)
    return topic


def Sentiment(text):
    """
    Detect the sentiment of text.

    Input:
    text -- list of text data;
    Output:
    sentiments decided by TextBlob.

    Reference:
    https://textblob.readthedocs.io/en/dev/
    """
    sentiment = []
    for i in range(len(text)):
        analysis = TextBlob(text.iloc[i])
        if analysis.sentiment.polarity > 0:
            sentiment.append("Positive")
        elif analysis.sentiment.polarity == 0:
            sentiment.append("Neutral")
        else:
            sentiment.append("Negative")
    return sentiment


def PlotSentiment(sentiment):
    """
    Visualize percentages of sentiments.

    Input:
    sentiment -- a column with sentiments.
    Output:
    a pie plot of sentiments.
    """
    plt.figure(figsize=[6, 6])
    senticount = [list(sentiment).count("Positive"),
                  list(sentiment).count("Neutral"),
                  list(sentiment).count("Negative")]
    sentilabel = ["Positive", "Neutural", "Negative"]
    colors = ["#5A8A91", "#FBC800", "#EF2648"]
    plt.pie(senticount, colors=colors, labels=sentilabel, autopct='%1.1f%%')
    return
