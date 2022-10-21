class MyModel:
    """
    nel modello ho bisogno di prendere i match della prossima giornata e: 
    - calcolare il rank delle due squadre
    - ottenere le medie
    - calcolare le differenze
    - ottenere il testo delle predizioni
    - tokenizzare il testo e ottenere la predizione del sito
    - combinare tutto e ottenere la predizione
    """
    def __init__(self, matches):
        self.matches = matches

    
