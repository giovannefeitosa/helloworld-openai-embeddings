import spacy


def readFile(file):
    with open(file, 'r') as f:
        return f.read()


def removeStopWords(nlp, text):
    # nlp.Defaults.stop_words.add('(')
    # nlp.Defaults.stop_words.add(')')
    # nlp.Defaults.stop_words.add('O')
    # nlp.Defaults.stop_words.add('-')
    doc = nlp(text)
    return " ".join([token.text for token in doc if not token.is_stop])


def splitSentences(text):
    # https://stackoverflow.com/a/61254146/1791115
    nlp = spacy.load('en_core_web_sm')
    # parsedText = removeStopWords(nlp, text)
    # print(parsedText)
    # doc.sents is an iterable, but we want it as a list
    # return doc.sents
    doc = nlp(text)
    return [sent.text for sent in doc.sents]
    # return [token.sent.lemma_ for token in nlp(text) if not token.is_stop]
