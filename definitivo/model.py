import sklearn.metrics as mtr
import pandas as pd

class Model:
    def __init__(self, name, model):
        self.name = name
        self.model = model

    def fit(self, X_train, y_train):
        self.y_train = y_train
        self.model.fit(X_train, self.y_train)
    
    def predict(self, X_test, y_test):
        self.y_test = y_test
        self.y_pred = self.model.predict(X_test)

    def generate_report(self):
        self.analysis = pd.DataFrame()
        
        report = mtr.classification_report(self.y_test, self.y_pred, output_dict=True, zero_division=0)
        self.analysis = {
            'Model': self.name, 'Accuracy': report['accuracy'],
            'Avg Precision (macro)': report['macro avg']['precision'],
            'Avg Recall (macro)': report['macro avg']['recall'],
            'Avg F1-score (macro)': report['macro avg']['f1-score'],
            'Avg Precision (weighted)': report['weighted avg']['precision'],
            'Avg Recall (weighted)': report['weighted avg']['recall'],
            'Avg F1-score (weighted)': report['weighted avg']['f1-score']
        }


    def get_report(self):
        return self.analysis