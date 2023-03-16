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
        sentences = [str(sent.text).replace('"', '') for sent in doc.sents]
        # group sentences in pairs
        # ? does this improves or decreases the quality of the dataset?
        sentences = [
            f"{sentences[i]}. {sentences[i+1]}" for i in range(0, len(sentences) - 1, 2)]
        return sentences

    # Receives a raw text and returns an array of paragraphs
    def splitParagraphs(self, text):
        """Split text into paragraphs"""
        paragraphs = [t for t in text.split('\n') if t.replace(' ', '') != '']
        return paragraphs

    # Returns a spacy.load() model
    def spacyLoad(self):
        """Load spacy model"""
        if not hasattr(self, 'spacyInstance'):
            self.spacyInstance = spacy.load(configs.spacyModel)
        return self.spacyInstance


spacyUtils = SpacyUtils()
