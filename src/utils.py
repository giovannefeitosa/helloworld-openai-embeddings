import spacy


def loadFile(file):
    with open(file, 'r') as f:
        return f.read()


def splitSentences(text):
    # https://stackoverflow.com/a/61254146/1791115
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    # return [sent for sent in doc.sents]
    return doc.sents
