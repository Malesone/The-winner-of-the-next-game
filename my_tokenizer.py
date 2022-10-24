import json
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import sent_tokenize, word_tokenize
import nltk
from nltk.corpus import stopwords
import spacy
from nltk.stem import PorterStemmer, WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
import util_strings as utils

class MyTokenizer:
    def __init__(self, dataset):
        self.dataset = dataset[dataset.prediction != 'NAN'] #non considero i valori NAN, altrimenti non posso tokenizzare
        self.dataset.reset_index(drop=True, inplace=True)
        self.prediction_labels = {
                'N': 0,
                'V': 1,
                'P': 2
            }
        self.nlp = spacy.load("en_core_web_sm")
        self.stop_words = set(stopwords.words('english'))
        self.stemmer = PorterStemmer()

    def feature_normalization(self):
        with open(utils.synonyms) as jsonFile:
            jsonObject = json.load(jsonFile)
            jsonFile.close()

        for i, row in self.dataset.iterrows():
            h_team, a_team, description, prediction = row.home, row.away, row.description, row.prediction

            syn = {}
            #cerco nel dizionario di sinonimi, tutti i sinonimi delle squadre del match
            for key in jsonObject.keys():
                if (h_team in key) or (key in h_team):
                    syn['home team'] = jsonObject[key] 
                    
                if (a_team in key) or (key in a_team):
                    syn['away team'] = jsonObject[key] 

            #successivamente prendo il testo e sostituisco i sinonimi con home o away team
            description = description.lower()
            for key in syn.keys():
                for val in syn[key]:
                    description = description.replace(val.lower(), key)

            self.dataset.at[i, 'description'] = description
            
            self.dataset = self.dataset[['description', 'prediction', 'home', 'away']]
          

        for i, prediction in enumerate(self.dataset.prediction):
            self.dataset.at[i, 'pred'] = self.prediction_labels[prediction]
            
        self.dataset.drop(columns=['prediction'], inplace=True)
        self.dataset.rename(columns={'pred': 'prediction'}, inplace=True)
        
    def word_tokenization(self, text):
        #tokenizzazione utilizzata con NLTK
        tokens = word_tokenize(text)
        tokens = [word for word in tokens if word not in self.stop_words]
        return tokens

    def regex(self, text):
        #tokenizzazione utilizzato con regex
        tokens = RegexpTokenizer(r'[a-zA-Z0-9]+').tokenize(text)
        tokens = [word for word in tokens if word not in self.stop_words]
        return tokens

    def spacy_tokenization(self, text):
        #tokenizzazione utilizzato con spacy
        tokens_text = []
        tokens_lemma = []
        for token in self.nlp(text):
            if not token.is_stop:
                tokens_text.append(token.text)
                tokens_lemma.append(token.lemma_)
        return tokens_text, tokens_lemma

    def clean_text(self):
        self.cleaned_corpus = []
        for i, doc in self.dataset.iterrows():
            doc_text = self.word_tokenization(doc.description)
            doc_text = [self.stemmer.stem(word) for word in doc_text]
            self.dataset.at[i, 'description'] = list(nltk.bigrams(doc_text))
            doc_text = ' '.join(doc_text)
            self.cleaned_corpus.append(doc_text)
        
    def set_bigram_and_get_sets(self): 
        self.vectorizer = TfidfVectorizer(ngram_range=(2,2)) #vectorizer sarà il nostro modello da allenare
        tokenized_text = self.vectorizer.fit_transform(self.cleaned_corpus)

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
        tokenized_text, self.dataset.prediction, test_size=0.2, shuffle=False)
        return self.X_train, self.X_test, self.y_train, self.y_test

    def set_label_prediction(self, y_pred):
        for i in range(len(self.y_train)):
            self.dataset.at[i, 'pred'] = self.y_train[i]
        for i in range(len(y_pred)):
            val = i+len(self.y_train)
            self.dataset.at[val, 'pred'] = y_pred[i]
            