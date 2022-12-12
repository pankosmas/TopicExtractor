!python -m spacy download el_core_news_lg
!pip install Unidecode
!pip install sklearn
import pandas as pd
import seaborn as sns
import spacy
from difflib import SequenceMatcher
import matplotlib.pyplot as plt
import string
import math
import re
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn import preprocessing
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

import pandas as pd
nlp = spacy.load("el_core_news_lg")

# ========================================================================================================================================================================================================================================================

data = pd.read_csv("C:\\Python\\Torchidis\\XXXXXXXXXXXXXXXXXXXXX.csv")

data['category'].unique()
data.isnull().sum()

# ========================================================================================================================================================================================================================================================

chart = sns.countplot(data.category)
chart.set_xticklabels(chart.get_xticklabels(), rotation=45)

# ========================================================================================================================================================================================================================================================

stoplist = set('αλλα αλλά εγω εγώ εσυ εσύ αυτος αυτός αυτη αυτή αυτο αυτό εμεις εμείς εσεις εσείς αυτοι αυτοί αυτα '
               'αυτά το του τα των τις τους τοις ναι οχι και μη μην δε λίγο λιγο τόσο τοσο γι για δεν ειμαι είμαι '
               'εισαι είσαι ειναι είναι ειμαστε είμαστε ειστε είστε ειναι είναι ουτε ούτε μητε μήτε ουδε ουδέ η ή '
               'ειτε είτε αν και μα παρα πάρα παρά ομως όμως ωστοσο ωστόσο ενω ενώ μολονοτι μολονότι μονο μόνο μονό '
               'που λοιπον λοιπόν ωστε ώστε αρα άρα επομενως επομένως οποτε όποτε οπότε δηλαδη δηλαδή οτι ότι πως που '
               'μην μηπως μήπως να αμα άμα οταν όταν καθως καθώς αφου αφού αφοτου αφότου πριν μολις προτου ωσπου '
               'ωσοτου σαν όσον γιατι διοτι επειδη αφου τι οτι για να ωστε ως παρα αναμεσα κάνω κάνεις κάνει κάνουν '
               'κάνουμε κι δε μέρα μεταξυ εαν ανω κατω πανω πισω μπρος μπροστα εχω κανω λεω βλεπω μπορω μπορει ισως '
               'καλα καλο καλος καλη καλων έχω έχεις έχει έχουμε έχετε έχουν εχω εχεις εχει εχουμε εχετε εχουν'
               'είχα είχες είχε είχαμε είχατε είχαν ειχα ειχες ειχε ειχαμε ειχατε ειχαν καλους καλε εκει εκτος εντος'
               'μεσα εξω ιδιο ηταν ζωη ολα ολο ολος ολοι ομως ποτε σπανια οποιος οποια οποιο οποιους οποιοι οποιες πολυ πολλα πολλη πολλων πολλους τωρα χθες σημερα '
               'αυριο παρον παρων μελλον παρελθον χθες ωρα χωρις με χρονια πρωτος της κατα στα στο στη στων στις στους '
               'οι ο η απο στην νέο στη στον στο τον την μόλις προτού το ώσπου ωσότου σαν γιατί διότι επειδή αφού τι ότι για '
               'να ώστε ως πάρα αναμεσά έχετε κάνετε χθες χτες εχτές εχθές μεταξύ εάν άνω κάτω πάνω πίσω μπρος μπροστά '
               'έχω κάνω λέω βλέπω μπορώ μπορεί ίσως καλά καλό καλός καλή καλών καλούς καλέ εκεί εκτός εντός μέσα έξω '
               'ίδιο ήταν ζωή μεγάλη μικρή όλα όλο όλος όλοι όμως ποτέ εδώ σπάνια όποιος όποια όποιο όποιους όποιοι όποιες '
               'πολύ πολλά πολλή πολλών πολλούς τώρα χθες σήμερα αύριο παρόν παρών μέλλον παρελθόν χθες ώρα χωρίς με '
               'χρονιά πρώτος της κατά στα στο μετα μετά όσων οσων στη στων στις στους οι ο η από στην στη στον στο τον την θα όμως σε '
               'αυτού τη όλους μας σας πρέπει ήδη έχει είχε μια μία ένα ένας ενός υπό οποία οποίο οποίος οποίους δικό '
               'μετά κοντά έως εώς άλλους κάτι γύρω πιο όσο έχουν μπορώ μπορεί μπορείτε μπορούν πάνε κάντε δικό θέλετε '
               'δώσετε προς όπως δώστε δει δείτε βλέπω έτσι άλλοι ίδια νέα πολλά κυρίως άλλη ακόμα οποίων επί είπε όχι '
               'μέχρι μου σου του δυο δύο πλέον είπε α β γ δ ε ζ η θ ι κ λ μ ν ξ ο π ρ σ τ υ φ χ ψ ω αυτ όλη όσους '
               'όλες αυτούς θέλω βάζω κάθε κά τότε έχουμε θέλει έκανε βρίσκεται ακόμη όπου φέτος πέρσι μετά πέρυσι '
               'πήρε έδωσε ης βγει νέος νέα νέοι νέους νέας νέων ος γίνει υπάρχει υπάρχω υπάρχουν πάλι θέμα πώς μια μία μιας'
               'ανεξαρτήτως ίδιος μάλιστα έναν έγινε άλλο τρία τρια τρείς τρεις πέντε έξι επτά οκτώ δέκα τέσσερις θεμα'
               'ετ κεδ εναντίον τέσσερα αε ίδιες σ ς εννέα εννιά αο γς τέλος πάντως επίσης ας πχ x εκ περί αυτές άλλων'.split(' '))

s2 = set([word.upper() for word in stoplist])
s3 = set([word.capitalize() for word in stoplist])
stoplist = stoplist.union(s2)
stoplist = stoplist.union(s3)

# ========================================================================================================================================================================================================================================================

def process_text(text):
    text = text.replace('\n', ' ')
    text = text.translate(str.maketrans('', '', string.punctuation))
    words = [word for word in text.split(" ") if word not in stoplist]
    text = ' '.join(words)

    doc = nlp(text)
    clean_text = [token.text for token in doc if token.pos_ in ["NOUN"]]

    text = ' '.join(clean_text)
    return text
	
# ========================================================================================================================================================================================================================================================

label_encoder = preprocessing.LabelEncoder()
data['category_target'] = label_encoder.fit_transform(data['category'])
data.head()

# ========================================================================================================================================================================================================================================================

x_train, x_test, y_train, y_test = train_test_split(data['XXXXXXXXX'], 
                                                    data['category_target'], 
                                                    test_size = 0.3, 
                                                    random_state=8)
													
													
# ========================================================================================================================================================================================================================================================

ngram_range = (1,3)
min_df = 10
max_df = 1.
max_features = 300
tfidf = TfidfVectorizer(encoding='utf-8',
                       ngram_range=ngram_range,
                       stop_words=None,
                       lowercase=False,
                       max_df=max_df,
                       min_df=min_df,
                       max_features=max_features,
                       norm='l2',
                       sublinear_tf = True)

features_train = tfidf.fit_transform(x_train).toarray()
labels_train = y_train

features_test = tfidf.transform(x_test).toarray()
labels_test = y_test

# =========================================================================================================================================================================================================== RANDOM FOREST =============================

n_estimators = [100, 300, 500, 800, 1200]
max_depth = [5, 8, 15, 25, 30]
min_samples_split = [2, 5, 10, 15, 100]
min_samples_leaf = [1, 2, 5, 10]
hyperF = dict(n_estimators=n_estimators, max_depth=max_depth, min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf)
model = RandomForestClassifier()
gridF = GridSearchCV(model, hyperF, cv=3, verbose=1, n_jobs=-1)
bestF = gridF.fit(features_train, labels_train)
bestF.best_params_

# ========================================================================================================================================================================================================================================================

n_estimators=500

model = RandomForestClassifier(random_state=1, max_depth=30, min_samples_leaf=1, min_samples_split=2, n_estimators=1200)
model.fit(features_train, labels_train)
model_predictions = model.predict(features_test)
print('Accuracy', accuracy_score(labels_test, model_predictions))
print(classification_report(labels_test, model_predictions))

# =========================================================================================================================================================================================================== LOGISTIC REGRESSION =============================

param_grid = {'C':[0.1, 0.001, 1], 'penalty': ['l1','l2']}
model = LogisticRegression()
clf = GridSearchCV(model, param_grid, cv=3, verbose=10)
bestF = clf.fit(features_train, labels_train)
bestF.best_params_

# ========================================================================================================================================================================================================================================================

model = LogisticRegression(C=1, penalty='l2')
model.fit(features_train, labels_train)
model_predictions = model.predict(features_test)
print('Accuracy', accuracy_score(labels_test, model_predictions))
print(classification_report(labels_test, model_predictions))

# =========================================================================================================================================================================================================== K - NN =============================

params_kNN = {'n_neighbors': [1,2,3,4,5,6,7], 'p': [1,2,5]}
model = KNeighborsClassifier()
gridF = GridSearchCV(model, params_kNN, cv=3, verbose=1, n_jobs=-1)
bestF = gridF.fit(features_train, labels_train)
bestF.best_params_

# ========================================================================================================================================================================================================================================================

model = KNeighborsClassifier(n_neighbors= 1, p= 2)
model.fit(features_train, labels_train)
model_predictions = model.predict(features_test)
print('Accuracy', accuracy_score(labels_test, model_predictions))
print(classification_report(labels_test, model_predictions))

# =========================================================================================================================================================================================================== DECISION TREES =============================

params_kNN = {'n_neighbors': [1,2,3,4,5,6,7], 'p': [1,2,5]}
model = KNeighborsClassifier()
gridF = GridSearchCV(model, params_kNN, cv=3, verbose=1, n_jobs=-1)
bestF = gridF.fit(features_train, labels_train)
bestF.best_params_

# ========================================================================================================================================================================================================================================================

model = DecisionTreeClassifier()
model.fit(features_train, labels_train)
model_predictions = model.predict(features_test)
print('Accuracy', accuracy_score(labels_test, model_predictions))
print(classification_report(labels_test, model_predictions))


