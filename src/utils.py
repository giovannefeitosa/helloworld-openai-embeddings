import spacy


def loadFile(file):
    with open(file, 'r') as f:
        return f.read()


def splitSentences(text):
    # https://stackoverflow.com/a/61254146/1791115
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    # doc.sents is an iterable, but we want it as a list
    # return doc.sents
    return [sent.text for sent in doc.sents]
