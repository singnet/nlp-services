import os
import pickle
from nltk.classify import ClassifierI
from statistics import mode
from nltk.tokenize import word_tokenize
from log import log_config

logger = log_config.getLogger('consensus_mod.py')

#Service paths
current_path = os.path.dirname(os.path.realpath(__file__))
parent_path = os.path.abspath(os.path.join(current_path, os.pardir))
service_root_path = os.path.abspath(os.path.join(parent_path, os.pardir))


class VoteClassifier(ClassifierI):
    """ Vote by classifiers results
    """
    def __init__(self, *classifiers):
        self._classifiers = classifiers

    def classify(self, features):
        """ Vote on all classifiers results
        :param features: incomming feature to be classified
        :return: vote winner
        """

        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        return mode(votes)

    def confidence(self, features):
        """ Calculate the confidence of the result
        :param features:
        :return: confidence
        """

        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)

        total_of_winner_votes = votes.count(mode(votes))
        conf = total_of_winner_votes / len(votes)
        return conf


# Fetching word features
word_features5k_f = open(service_root_path + "/models/word_features5k.pickle", "rb")
word_features = pickle.load(word_features5k_f)
word_features5k_f.close()


def find_features(document):
    """ Tokenize document
    :param document:
    :return:
    """
    words = word_tokenize(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features


# Fetching trained classifieds
open_file = open(service_root_path + "/models/NaiveBayes_classifier5k.pickle", "rb")
NBlassifier = pickle.load(open_file)
open_file.close()

open_file = open(service_root_path + "/models/MNB_classifier5k.pickle", "rb")
MNB_classifier = pickle.load(open_file)
open_file.close()

open_file = open(service_root_path + "/models/BernoulliNB_classifier5k.pickle", "rb")
BernoulliNB_classifier = pickle.load(open_file)
open_file.close()

open_file = open(service_root_path + "/models/LogisticRegression_classifier5k.pickle", "rb")
LogisticRegression_classifier = pickle.load(open_file)
open_file.close()

open_file = open(service_root_path + "/models/LinearSVC_classifier5k.pickle", "rb")
LinearSVC_classifier = pickle.load(open_file)
open_file.close()

open_file = open(service_root_path + "/models/NuSVC_classifier5k.pickle", "rb")
NuSVC_classifier = pickle.load(open_file)
open_file.close()

open_file = open(service_root_path + "/models/SGDC_classifier5k.pickle", "rb")
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


def sentiment(text):
    """ Analyzing the semtniment

    :param text:
    :return: sentimento analysis
    """
    feats = find_features(text)
    return voted_classifier.classify(feats), voted_classifier.confidence(feats)
