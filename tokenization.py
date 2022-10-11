from nltk.tokenize import sent_tokenize, word_tokenize

text = "Verona and Sassuolo take on each other in a highly-anticipated Serie A game at Stadio Marc’Antonio Bentegodi on Saturday evening. The Mastini have established themselves as a top-table side in the Italian top flight, but the game against Sassuolo will be anything but a walk in the park for the hosts. The club chiefs did well to keep hold of key players in the summer transfer window, but keep in mind that both Lasagna and Faraoni are likely to miss the season opener. The Neroverdi, on the other hand, were producing fine displays in pre-season, with the team beating both Parma and Vicenza, while sharing the spoils with Lazio. Considering that Sassuolo are likely to stick to their attacking style of play, both teams to score betting option should be considered. Centre-back Marlon is no longer part of the team, while Kyriakopoulos is banned for the match. Obiang is yet another absentee in the away team"

#stampa qualsiasi cosa
tokenization1 = word_tokenize(text)

tokenizations = {
    'nltk.tokenize.word_tokenize': word_tokenize
}


from nltk.tokenize import RegexpTokenizer
token = RegexpTokenizer(r'[a-zA-Z0-9]+')
#non abbiamo lo punteggiatura
print(token.tokenize(text))

import nltk
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))