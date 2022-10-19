import sklearn.metrics as mtr
import pandas as pd
import warnings
import matplotlib.pyplot as plt

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

    def gen_confusion_matrix(self):
        warnings.filterwarnings('ignore')
        cm = mtr.confusion_matrix(self.y_test, self.y_pred)
        d = mtr.ConfusionMatrixDisplay(cm, [0,1,2])
        fig, ax = plt.subplots(figsize=(4,4))
        d.plot(ax=ax, cmap='Greens')
        plt.tight_layout()
        plt.show()

    def get_formatted_df(self):
        E = pd.DataFrame.from_dict(list(self.analysis.items()))
        E = E.T

        new_header = E.iloc[0] #grab the first row for the header
        df = E[1:] #take the data less the header row
        df.columns = new_header #set the header row as the df header
        df.set_index('Model', inplace=True)
        return df
    