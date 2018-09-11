import os
import pickle
from nltk.classify import ClassifierI
from statistics import mode
from nltk.tokenize import word_tokenize

#Current script path
current_path = os.path.dirname(__file__)


# Vote by classifiers results
class VoteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers

    # Iterate all classifiers
    def classify(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        return mode(votes)

    # Calculate the confidence of the result
    def confidence(self, features):
        # print(str(features))
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)

        print("")
        print("=========================================================================")
        print("")
        print("TOTAL OF VOTES => " + str(len(votes)) + ", OPENED VOTES => " + str(votes))
        print("")
        print("WINNER VOTE => " + str(mode(votes)) + ", TOTAL OF VOTES => " + str(votes.count(mode(votes))))
        print("")
        print("=========================================================================")
        print("")

        total_of_winner_votes = votes.count(mode(votes))
        conf = total_of_winner_votes / len(votes)
        return conf


# Fetching word features
word_features5k_f = open(os.path.join(current_path, "models/word_features5k.pickle"), "rb")
word_features = pickle.load(word_features5k_f)
word_features5k_f.close()


# Tokenizing document
def find_features(document):
    words = word_tokenize(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features


# Fetching trained classifieds
open_file = open(os.path.join(current_path, "models/NaiveBayes_classifier5k.pickle"), "rb")
NBlassifier = pickle.load(open_file)
open_file.close()

open_file = open(os.path.join(current_path, "models/MNB_classifier5k.pickle"), "rb")
MNB_classifier = pickle.load(open_file)
open_file.close()

open_file = open(os.path.join(current_path, "models/BernoulliNB_classifier5k.pickle"), "rb")
BernoulliNB_classifier = pickle.load(open_file)
open_file.close()

open_file = open(os.path.join(current_path, "models/LogisticRegression_classifier5k.pickle"), "rb")
LogisticRegression_classifier = pickle.load(open_file)
open_file.close()

open_file = open(os.path.join(current_path, "models/LinearSVC_classifier5k.pickle"), "rb")
LinearSVC_classifier = pickle.load(open_file)
open_file.close()

# ATTENTION ###
open_file = open(os.path.join(current_path, "models/NuSVC_classifier5k.pickle"), "rb")
NuSVC_classifier = pickle.load(open_file)
open_file.close()

open_file = open(os.path.join(current_path, "models/SGDC_classifier5k.pickle"), "rb")
SGDC_classifier = pickle.load(open_file)
open_file.close()

voted_classifier = VoteClassifier(
                                  NBlassifier,
                                  MNB_classifier,
                                  BernoulliNB_classifier,
                                  LogisticRegression_classifier,
                                  LinearSVC_classifier,
                                  NuSVC_classifier,
                                  SGDC_classifier
                                  )


# Classify sentiment
def sentiment(text):
    print(text)
    feats = find_features(text)
    return voted_classifier.classify(feats), voted_classifier.confidence(feats)
