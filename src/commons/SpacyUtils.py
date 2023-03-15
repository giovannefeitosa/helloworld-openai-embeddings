import spacy
from commons.Configs import configs


class SpacyUtils:
    def __init__(self, debug=False):
        self.debug = debug

    # Receives a raw text and returns an array of sentences
    def splitSentences(self, text):
        """Split text into sentences"""
        nlp = self.spacyLoad()
        doc = nlp(text)
        return [str(sent.text).replace('"', '') for sent in doc.sents]

    # Returns a spacy.load() model
    def spacyLoad(self):
        """Load spacy model"""
        if not hasattr(self, 'spacyInstance'):
            self.spacyInstance = spacy.load(configs.spacyModel)
        return self.spacyInstance


spacyUtils = SpacyUtils()
