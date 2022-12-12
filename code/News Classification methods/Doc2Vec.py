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
from gensim.models import Doc2Vec
from gensim.models.doc2vec import TaggedDocument
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

from sklearn.model_selection import train_test_split
def label_sentences(corpus, label_type):
    labeled = []
    for i,v in enumerate(corpus):
        label = label_type + '_' + str(i)
        labeled.append(TaggedDocument(v.split(), [label]))
    return labeled

x_train, x_test, y_train, y_test = train_test_split(data.text, data.category, random_state=0, test_size=0.3)
													
x_train = label_sentences(x_train, 'Train')
x_test = label_sentences(x_test, 'Test')
all_data = x_train + x_test

# ========================================================================================================================================================================================================================================================

from sklearn import utils

model_dbow = Doc2Vec(dm=0, vector_size=300, negative=5, min_count=1, alpha=0.065, min_alpha=0.0065)
model_dbow.build_vocab([x for x in all_data])

for epoch in range(30):
    model_dbow.train(utils.shuffle([x for x in all_data]), total_examples=len(all_data), epochs=1)
    model_dbow.alpha -= 0.002
    model_dbow.min_alpha = model_dbow.alpha
	
# ========================================================================================================================================================================================================================================================
	
model_dbow.save('C:\\Python\\myNewsScraper\\dbow_model')
model_dbow = Doc2Vec.load('C:\\Python\\myNewsScraper\\dbow_model')

# ========================================================================================================================================================================================================================================================

import numpy as np

def get_vectors(model, corpus_size, vectors_size, vectors_type):
    vectors = np.zeros((corpus_size, vectors_size))
    for i in range(0, corpus_size):
        prefix = vectors_type + '_' + str(i)
        vectors[i] = model.dv[prefix]
        
    return vectors
	
# ========================================================================================================================================================================================================================================================

train_vectors_dbow = get_vectors(model_dbow, len(x_train), 300, 'Train')
test_vectors_dbow = get_vectors(model_dbow, len(x_test), 300, 'Test')

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

model = RandomForestClassifier()
model.fit(train_vectors_dbow, y_train)
model_prediction = model.predict(test_vectors_dbow)
print('Accuracy', accuracy_score(model_prediction, y_test))
print(classification_report(y_test, model_prediction))

# =========================================================================================================================================================================================================== LOGISTIC REGRESSION =============================

param_grid = {'C':[0.1, 0.001, 1], 'penalty': ['l1','l2']}
model = LogisticRegression()
clf = GridSearchCV(model, param_grid, cv=3, verbose=10)
bestF = clf.fit(features_train, labels_train)
bestF.best_params_

# ========================================================================================================================================================================================================================================================

from sklearn.linear_model import LogisticRegression

model = LogisticRegression(C=1e5)
model = model.fit(train_vectors_dbow, y_train)
model_prediction = model.predict(test_vectors_dbow)
print('accuracy %s' % accuracy_score(model_prediction, y_test))
print(classification_report(y_test, model_prediction))

# =========================================================================================================================================================================================================== K - NN =============================

params_kNN = {'n_neighbors': [1,2,3,4,5,6,7], 'p': [1,2,5]}
model = KNeighborsClassifier()
gridF = GridSearchCV(model, params_kNN, cv=3, verbose=1, n_jobs=-1)
bestF = gridF.fit(features_train, labels_train)
bestF.best_params_

# ========================================================================================================================================================================================================================================================

model = KNeighborsClassifier()
model.fit(train_vectors_dbow, y_train)
model_prediction = model.predict(test_vectors_dbow)
print('Accuracy', accuracy_score(model_prediction, y_test))
print(classification_report(y_test, model_prediction))

#  ========================================================================================================================================================================================================== svm =============================

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

clf = make_pipeline(StandardScaler(), SVC(gamma='auto', probability=True))
clf.fit(train_vectors_dbow, y_train)

from sklearn.metrics import accuracy_score, classification_report
model_prediction = clf.predict(test_vectors_dbow)
print('accuracy %s' % accuracy_score(model_prediction, y_test))
print(classification_report(y_test, model_prediction))

# ========================================================================================================================================================================================================================================================

import pickle

pkl_filename = "C:\\Python\\myNewsScraper\\svm_model_93.pkl"

with open(pkl_filename, 'wb') as file:
    pickle.dump(clf, file)
	
from joblib import dump, load
dump(clf, "C:\\Python\\myNewsScraper\\svm_model_93b.pkl")

clf = load("C:\\Python\\myNewsScraper\\svm_model_93b.pkl") 

# ========================================================================================================================================================================================================================================================

import pickle
import pandas as pd
import re
nts = pd.read_csv("C:\\Users\\Panagiotis\\Desktop\\topics.csv")

len(nts.index)

vectors = [model_dbow.infer_vector(1000000*test_df['topic_processed'][i].split()) for i in range(794)]

y = clf.predict(vectors)
ctg = ['Αθλητισμός', 'Αυτοκίνητο', 'Αστρολογία', 'Θρησκεία', 'Καιρός', 'Κοινωνία', 'Διεθνή', 'Μόδα', 'Οικονομία', 'Περιβάλλον', 'Πολιτική', 'Πολιτισμός', 'Τεχνολογία', 'Υγεία']
ctgs = []
for elem in y:
    ctgs.append(ctg[elem])
test_df['auto_category_svm'] = ctgs
test_df.to_csv("C:\\Users\Panagiotis\\Desktop\\topics.csv", encoding='utf-8')

from difflib import SequenceMatcher
import unidecode

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def process_topic(topic):
    topic = re.sub(r'[0-9] ', '', topic)
    topic = topic.replace(' ', '-')
    topic = re.sub(r'[0-9]', '', topic)
    topic = topic.replace('_', ' ')
    words = [word for word in topic.split(' ') if word not in stoplist]
    words = list(dict.fromkeys(words))
    
    trash_words = []
    for i in range(len(words)-1):
        similarities = []
        for j in range(i+1, len(words)):
            similarity = similar(unidecode.unidecode(words[i]), unidecode.unidecode(words[j]))
            if similarity >= 0.75:
                if len(words[i]) <= len(words[j]):
                    trash_words.append(words[j])
                else:
                    trash_words.append(words[i])
                    
    words = [x for x in words if not x in trash_words or trash_words.remove(x)]
    topic = ' '.join(words)
    
    return topic

import pandas as pd
import re
test_df = pd.read_csv('C:\\Users\\Panagiotis\\Desktop\\topics.csv')
ctg = test_df['auto_category_svm']
test_df = test_df.drop(columns=['topic_processed'], axis=1)
test_df['topic_processed'] = test_df['topic'].apply(process_topic)
test_df.to_csv('C:\\Users\\Panagiotis\\Desktop\\topics2.csv')


vectors = [model_dbow.infer_vector(1000000*test_df['topic_processed'][i].split()) for i in range(686)]
y = clf.predict(vectors)
y

ctg = ['Αθλητισμός', 'Αυτοκίνητο', 'Αστρολογία', 'Θρησκεία', 'Καιρός', 'Κοινωνία', 'Διεθνή', 'Μόδα', 'Οικονομία', 'Περιβάλλον', 'Πολιτική', 'Πολιτισμός', 'Τεχνολογία', 'Υγεία']
ctgs = []
for elem in y:
    ctgs.append(ctg[elem])
test_df['auto_category_svm'] = ctgs
test_df.to_csv("C:\\Users\Panagiotis\\Desktop\\file3.csv", encoding='utf-8')

				
