import os
from log import log_config
import nltk
from nltk import pos_tag
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
from nltk.chunk import conlltags2tree
from nltk.tree import Tree

logger = log_config.getLogger('classifiers_mod.py')

#Services Path
current_path = os.path.dirname(os.path.realpath(__file__))
parent_path = os.path.abspath(os.path.join(current_path, os.pardir))
service_root_path = os.path.abspath(os.path.join(parent_path, os.pardir))

# Snet Classifier
class SnetClassifier:

    def __init__(self):
        # Snet Classifier.
        logger.debug("SnetClassifier INIT")
        self.english_model = service_root_path + '/models/stanford-ner-2018-02-27/classifiers/english.all.3class.distsim.crf.ser.gz'
        self.stanford_jar = service_root_path + '/models/stanford-ner-2018-02-27/stanford-ner-3.9.1.jar'

    # Process text
    def process_text(self, input_text):
        token_text = word_tokenize(str(input_text))
        return token_text

    # Stanford NER tagger
    def stanford_tagger(self, token_text):
        st = StanfordNERTagger(self.english_model, self.stanford_jar, encoding='utf-8')
        ne_tagged = st.tag(token_text)
        return (ne_tagged)

    # NLTK POS and NER taggers
    def nltk_tagger(self, token_text):
        tagged_words = nltk.pos_tag(token_text)
        ne_tagged = nltk.ne_chunk(tagged_words)
        return (ne_tagged)

    # Tag tokens with standard NLP BIO tags
    def bio_tagger(self, ne_tagged):
        bio_tagged = []
        prev_tag = "O"
        for token, tag in ne_tagged:
            if tag == "O":  # O
                bio_tagged.append((token, tag))
                prev_tag = tag
                continue
            if tag != "O" and prev_tag == "O":  # Begin NE
                bio_tagged.append((token, "B-" + tag))
                prev_tag = tag
            elif prev_tag != "O" and prev_tag == tag:  # Inside NE
                bio_tagged.append((token, "I-" + tag))
                prev_tag = tag
            elif prev_tag != "O" and prev_tag != tag:  # Adjacent NE
                bio_tagged.append((token, "B-" + tag))
                prev_tag = tag
        return bio_tagged

    # Create tree
    def stanford_tree(self, bio_tagged):
        tokens, ne_tags = zip(*bio_tagged)
        pos_tags = [pos for token, pos in pos_tag(tokens)]

        conlltags = [(token, pos, ne) for token, pos, ne in zip(tokens, pos_tags, ne_tags)]
        ne_tree = conlltags2tree(conlltags)
        return ne_tree

    # Parse named entities from tree
    def structure_ne(self, ne_tree):
        ne = []
        for subtree in ne_tree:
            if type(subtree) == Tree:  # If subtree is a noun chunk, i.e. NE != "O"
                ne_label = subtree.label()
                ne_string = " ".join([token for token, pos in subtree.leaves()])
                ne.append((ne_string, ne_label))
        return ne

    # Nltk Named Entity Recognizer
    def nltk_classifier(self, input_text):
        result = self.structure_ne(self.nltk_tagger(self.process_text(input_text)))
        # logger.debug("nltk input text => ", str(result))
        return result

    # Stanford Named Entity Recognizer
    def stanford_classifier(self, input_text):
        result = self.structure_ne(self.stanford_tree(self.bio_tagger(self.stanford_tagger(self.process_text(input_text)))))
        # logger.debug("stanford input text => ", str(result))
        return result
