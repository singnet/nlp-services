import os

import nltk
import random
from nltk.classify.scikitlearn import SklearnClassifier
import pickle
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from nltk.classify import ClassifierI
from statistics import mode
from nltk.tokenize import word_tokenize

#Current script path
current_path = os.path.dirname(__file__)


# Vote Classifier class
class VoteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers

    def classify(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        return mode(votes)

    def confidence(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)

        choice_votes = votes.count(mode(votes))
        conf = choice_votes / len(votes)
        return conf


# Fetching trained dataset
short_pos = open("../corpus/imdb/pos/corpus.txt", "r", encoding="utf-8").read()
short_neg = open("../corpus/imdb/neg/corpus.txt", "r", encoding="utf-8").read()
print("files loaded")

# Documents and words variables
all_words = []
documents = []

# j is adject, r is adverb, and v is verb
# allowed_word_types = ["J","R","V"]
allowed_word_types = ["J"]

# Setting allowed words by type
for p in short_pos.split('\n'):
    # Adding all positive document words
    documents.append((p, "pos"))
    # Tokenizing positive sentence
    words = word_tokenize(p)
    # Tagging words
    pos = nltk.pos_tag(words)
    # Appending positive allowed word types
    for w in pos:
        if w[1][0] in allowed_word_types:
            all_words.append(w[0].lower())

# Setting allowed words by type
for p in short_neg.split('\n'):
    # Adding all negative document words
    documents.append((p, "neg"))
    # Tokenizing negative sentence
    words = word_tokenize(p)
    # Tagging words
    neg = nltk.pos_tag(words)
    # Appending positive allowed word types
    for w in neg:
        if w[1][0] in allowed_word_types:
            all_words.append(w[0].lower())

# The FreqDist class is used to encode “frequency distributions”,
# which count the number of times that each outcome of an experiment occurs.
# Setting the word frequency
all_words = nltk.FreqDist(all_words)

# Fetching the first 5000 word features
word_features = list(all_words.keys())[:5000]

# Saving document reference
save_documents = open("models/documents.pickle", "wb")
pickle.dump(documents, save_documents)
save_documents.close()
print("SAVED WITH SUCCESS:  documents.pickle")

# Saving word features references
save_word_features = open("models/word_features5k.pickle", "wb")
pickle.dump(word_features, save_word_features)
save_word_features.close()
print("SAVED WITH SUCCESS:  word_features5k.pickle")


# Find features function
def find_features(document):
    words = word_tokenize(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features


# Setting featuresets
featuresets = [(find_features(rev), category) for (rev, category) in documents]

# Shuffling the features
random.shuffle(featuresets)
print(len(featuresets))

# Fetching data for testing
testing_set = featuresets[10000:]
# Fetching data for trainning
training_set = featuresets[:10000]

# Trainning the classifier
classifier = nltk.NaiveBayesClassifier.train(training_set)
print("Original Naive Bayes Algo accuracy percent:", (nltk.classify.accuracy(classifier, testing_set)) * 100)
classifier.show_most_informative_features(15)

# Saving the trained classifier
save_classifier = open("models/NaiveBayes_classifier5k.pickle", "wb")
pickle.dump(classifier, save_classifier)
save_classifier.close()
print("SAVED WITH SUCCESS:  NaiveBayes_classifier5k.pickle")

# Trainning the classifier
MNB_classifier = SklearnClassifier(MultinomialNB())
MNB_classifier.train(training_set)
print("MNB_classifier accuracy percent:", (nltk.classify.accuracy(MNB_classifier, testing_set)) * 100)

# Saving the trained classifier
save_classifier = open("models/MNB_classifier5k.pickle", "wb")
pickle.dump(MNB_classifier, save_classifier)
save_classifier.close()
print("SAVED WITH SUCCESS:  MNB_classifier5k.pickle")

# Trainning the classifier
BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
BernoulliNB_classifier.train(training_set)
print("BernoulliNB_classifier accuracy percent:", (nltk.classify.accuracy(BernoulliNB_classifier, testing_set)) * 100)

# Saving the trained classifier
save_classifier = open("models/BernoulliNB_classifier5k.pickle", "wb")
pickle.dump(BernoulliNB_classifier, save_classifier)
save_classifier.close()
print("SAVED WITH SUCCESS:  BernoulliNB_classifier5k.pickle")

# Trainning the classifier
LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
LogisticRegression_classifier.train(training_set)
print("LogisticRegression_classifier accuracy percent:",
      (nltk.classify.accuracy(LogisticRegression_classifier, testing_set)) * 100)

# Saving the trained classifier
save_classifier = open("models/LogisticRegression_classifier5k.pickle", "wb")
pickle.dump(LogisticRegression_classifier, save_classifier)
save_classifier.close()
print("SAVED WITH SUCCESS:  LogisticRegression_classifier5k.pickle")

# Trainning the classifier
LinearSVC_classifier = SklearnClassifier(LinearSVC())
LinearSVC_classifier.train(training_set)
print("LinearSVC_classifier accuracy percent:", (nltk.classify.accuracy(LinearSVC_classifier, testing_set)) * 100)

# Saving the trained classifier
save_classifier = open("models/LinearSVC_classifier5k.pickle", "wb")
pickle.dump(LinearSVC_classifier, save_classifier)
save_classifier.close()
print("SAVED WITH SUCCESS:  LinearSVC_classifier5k.pickle")

# Trainning the classifier ####
NuSVC_classifier = SklearnClassifier(NuSVC())
NuSVC_classifier.train(training_set)
print("NuSVC_classifier accuracy percent:", (nltk.classify.accuracy(NuSVC_classifier, testing_set))*100)

# Saving the trained classifier ####
save_classifier = open("models/NuSVC_classifier5k.pickle", "wb")
pickle.dump(NuSVC_classifier, save_classifier)
save_classifier.close()
print("SAVED WITH SUCCESS:  NuSVC_classifier5k.pickle")

# Trainning the classifier
SGDC_classifier = SklearnClassifier(SGDClassifier())
SGDC_classifier.train(training_set)
print("SGDClassifier accuracy percent:", nltk.classify.accuracy(SGDC_classifier, testing_set) * 100)

# Saving the trained classifier
save_classifier = open("models/SGDC_classifier5k.pickle", "wb")
pickle.dump(SGDC_classifier, save_classifier)
save_classifier.close()
print("SAVED WITH SUCCESS:  SGDC_classifier5k.pickle")

print("ALL CLASSIFIERS SAVED WITH SUCCESS")
