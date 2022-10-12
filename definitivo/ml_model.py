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


class MlModel:
    models = {
        'Logistic Regression': LogisticRegression(max_iter=10000), #max_iter di default vale 100, ho dovuto alzarlo se no non converge
        'Support Vector Machine': SVC(),
        #'Multinomial Naive Bayes': MultinomialNB(),
        'Decision Tree': DecisionTreeClassifier(),
        'Random Forest': RandomForestClassifier(),
        'K-Nearest Neighbors': KNeighborsClassifier()
    }

    def prepare(self, dataset):
        features = [x for x in dataset.columns if x != 'result' and x != 'date']
        X, y = dataset[features], dataset.result.values

        #shuffle viene settato a False perché non voglio che vengano randomizzate le partite, verrebbe un risultato sballato
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2, shuffle=False) 

    def fit(self):
        for model_name, model in self.models.items():
            self.models[model_name].fit(self.X_train, self.y_train)

    def predict(self):
        self.predictions = {}
        for model_name, model in self.models.items():
            self.predictions[model_name] = model.predict(self.X_test)

    def gen_report(self):
        #genero un report su tutti i modelli utilizzati con le varie accuratezza 
        E = []
        for estimator, y_pred in self.predictions.items():
            report = mtr.classification_report(self.y_test, y_pred, output_dict=True, zero_division=0)
            E.append({
                'Model': estimator, 'Accuracy': report['accuracy'],
                'Avg Precision (macro)': report['macro avg']['precision'],
                'Avg Recall (macro)': report['macro avg']['recall'],
                'Avg F1-score (macro)': report['macro avg']['f1-score'],
                'Avg Precision (weighted)': report['weighted avg']['precision'],
                'Avg Recall (weighted)': report['weighted avg']['recall'],
                'Avg F1-score (weighted)': report['weighted avg']['f1-score']
            })
        self.E = pd.DataFrame(E).set_index('Model', inplace=False)
        #display(self.E)

    def get_higher_accuracies(self): 
        #prendo le accuratezze migliori: prima prendo l'accuratezza più alta, poi confronto questa accuratezza con le altre e se c'è uno scarto di 0.2 allora è tollerabile
        self.E.reset_index(level='Model', inplace=True)
        
        max_accuracy = self.E.loc[0]
        for row, model in self.E[1:].iterrows():
            if model.Accuracy > max_accuracy.Accuracy:
                max_accuracy = model

        best_accuracies = []
        for row, model in self.E.iterrows():
            if (max_accuracy.Accuracy - model.Accuracy) < 0.2:
                best_accuracies.append(model)

        self.E = pd.DataFrame(best_accuracies)
        self.E.set_index('Model', inplace=True)
        display(self.E)