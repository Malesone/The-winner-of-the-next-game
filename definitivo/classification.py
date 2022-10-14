import pandas as pd
from sklearn.model_selection import train_test_split
import sklearn.metrics as mtr

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from IPython.display import display
from model import Model

class Classification:
    def prepare(self, dataset):
        features = [x for x in dataset.columns if x != 'result' and x != 'date']
        X, y = dataset[features], dataset.result.values

        #shuffle viene settato a False perché non voglio che vengano randomizzate le partite, verrebbe un risultato sballato
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2, shuffle=False) 

    def create_models(self):
        self.models = []
        self.models.extend([
            Model('Logistic Regression', LogisticRegression(max_iter=10000)),
            Model('Support Vector Machine', SVC()),
            Model('Decision Tree', DecisionTreeClassifier()),
            Model('Random Forest', RandomForestClassifier()),
            Model('K-Nearest Neighbors', KNeighborsClassifier())
        ])

        for model in self.models:
            model.fit(self.X_train, self.y_train)
            model.predict(self.X_test, self.y_test)
        
    def gen_report(self):
        #genero un report su tutti i modelli utilizzati con le varie accuratezza 
        E = []
        for model in self.models:
            model.generate_report()
            E.append(model.get_report())

        self.E = pd.DataFrame(E).set_index('Model', inplace=False)

    def get_higher_accuracies(self, distance): 
        #prendo le accuratezze migliori: prima prendo l'accuratezza più alta, poi confronto questa accuratezza con le altre e se c'è uno scarto di 0.2 allora è tollerabile
        max_accuracy = self.models[0]

        #get max accuracy
        for model in self.models[1:]:
            if model.analysis['Accuracy'] > max_accuracy.analysis['Accuracy']:
                max_accuracy = model
        
        best_accuracies = []
        for model in self.models:
            if (max_accuracy.analysis['Accuracy'] - model.analysis['Accuracy']) < distance:
                best_accuracies.append(model.analysis)

        self.best_accuracies = pd.DataFrame(best_accuracies).set_index('Model', inplace=False)
        display(self.best_accuracies)
        
        

