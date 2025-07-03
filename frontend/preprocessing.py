import spacy
import re

nlp = spacy.load("en_core_web_sm")

def preprocess_text(text: str):
    # lower text
    text = text.lower()
    doc = nlp(text)
    # lemmatisation,stopwords,ponctuation
    token = [token.lemma_ for token in doc if not token.is_stop and  not token.is_punct]
    text = ' '.join(token)
    # remove spaces
    text = re.sub(r'\s+',' ',text)
    return text
