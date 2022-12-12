from sentence_transformers import SentenceTransformer
import pandas as pd
from umap import UMAP
from hdbscan import HDBSCAN
from bertopic import BERTopic
from sklearn.feature_extraction.text import CountVectorizer

stoplist = set('αλλα αλλά εγω εγώ εσυ εσύ αυτος αυτός αυτη αυτή αυτο αυτό εμεις εμείς εσεις εσείς αυτοι αυτοί αυτα '
               'αυτά το του τα των τις τους τοις και ναι οχι μη μην δε λίγο λιγο τόσο τοσο γι για δεν ειμαι είμαι '
               'εισαι είσαι ειναι είναι ειμαστε είμαστε ειστε είστε ειναι είναι ουτε ούτε μητε μήτε ουδε ουδέ η ή '
               'ειτε είτε αν και μα παρα πάρα παρά ομως όμως ωστοσο ωστόσο ενω ενώ μολονοτι μολονότι μονο μόνο μονό '
               'που λοιπον λοιπόν ωστε ώστε αρα άρα επομενως επομένως οποτε όποτε οπότε δηλαδη δηλαδή οτι ότι πως που '
               'μην μηπως μήπως να αμα άμα οταν όταν καθως καθώς αφου αφού αφοτου αφότου πριν μολις προτου ωσπου '
               'ωσοτου σαν γιατι διοτι επειδη αφου τι οτι για να ωστε ως παρα αναμεσα κάνω κάνεις κάνει κάνουν '
               'κάνουμε κι δε μέρα μεταξυ εαν ανω κατω πανω πισω μπρος μπροστα εχω κανω λεω βλεπω μπορω μπορει ισως '
               'καλα καλο καλος καλη καλων έχω έχεις έχει έχουμε έχετε έχουν εχω εχεις εχει εχουμε εχετε εχουν'
               'είχα είχες είχε είχαμε είχατε είχαν ειχα ειχες ειχε ειχαμε ειχατε ειχαν καλους καλε εκει εκτος εντος'
               'μεσα εξω ιδιο ηταν ζωη ολα ολο ολος ολοι ομως ποτε σπανια οποιος οποια οποιο οποιους οποιοι οποιες '
               'πολυ πολλα πολλη πολλων πολλους τωρα χθες σημερα αυριο παρον παρων μελλον παρελθον χθες ωρα χωρις με '
               'χρονια πρωτος της κατα στα στο στη στων στις στους οι ο η απο στην στη στον στο τον την μόλις προτού '
               'ώσπου ωσότου σαν γιατί διότι επειδή αφού τι ότι για να ώστε ως πάρα αναμεσά έχετε κάνετε χθες χτες '
               'εχτές εχθές μεταξύ εάν άνω κάτω πάνω πίσω μπρος μπροστά έχω κάνω λέω βλέπω μπορώ μπορεί ίσως καλά '
               'καλό καλός καλή καλών καλούς καλέ εκεί εκτός εντός μέσα έξω ίδιο ήταν ζωή μεγάλη μικρή όλα όλο όλος '
               'όλοι όμως ποτέ σπάνια όποιος όποια όποιο όποιους όποιοι όποιες πολύ πολλά πολλή πολλών πολλούς τώρα '
               'χθες σήμερα αύριο παρόν παρών μέλλον παρελθόν χθες ώρα χωρίς με χρονιά πρώτος της κατά στα στο μετα '
               'μετά όσων οσων στη στων στις στους οι ο η από στην στη στον στο τον την θα όμως σε αυτού τη όλους μας '
               'σας πρέπει ήδη έχει είχε μια μία ένα ένας ενός υπό οποία οποίο οποίος οποίους δικό μετά κοντά έως εώς '
               'άλλους κάτι γύρω πιο όσο έχουν μπορώ μπορεί μπορείτε μπορούν πάνε κάντε δικό θέλετε δώσετε προς όπως '
               'δώστε δει δείτε βλέπω έτσι άλλοι ίδια νέα πολλά κυρίως άλλη ακόμα οποίων επί είπε όχι μέχρι μου σου '
               'του δυο δύο πλέον είπε α β γ δ ε ζ η θ ι κ λ μ ν ξ ο π ρ σ τ υ φ χ ψ ω αυτ όλη όσους όλες αυτούς θέλω '
               'βάζω κάθε κά τότε έχουμε θέλει έκανε βρίσκεται ακόμη όπου φέτος πέρσι μετά πέρυσι πήρε έδωσε ης βγει '
               'νέος νέα νέοι νέους νέας νέων ος γίνει υπάρχει υπάρχω υπάρχουν πάλι θέμα πώς μια μία μιας ανεξαρτήτως '
               'ίδιος μάλιστα έναν έγινε άλλο τρία τρια τρείς τρεις πέντε έξι επτά οκτώ δέκα τέσσερις θεμα ετ κεδ '
               'εναντίον τέσσερα αε ίδιες σ ς εννέα εννιά αο γς τέλος πάντως επίσης ας πχ x εκ περί αυτές '
               'άλλων'.split(' '))

s2 = set([word.upper() for word in stoplist])
s3 = set([word.capitalize() for word in stoplist])

stoplist = stoplist.union(s2)
stoplist = stoplist.union(s3)

df = pd.read_csv('C:\\Python\\torchidis\\omilies_proc.csv')

texts = df['text'].tolist()

sentence_model = SentenceTransformer("lighteternal/stsb-xlm-r-greek-transfer")  # paraphrase-multilingual-mpnet-base-v2
embeddings = sentence_model.encode(texts, show_progress_bar=True)

umap_model = UMAP(n_neighbors=15, n_components=5, min_dist=0.0, metric='cosine')
hdbscan_model = HDBSCAN(min_cluster_size=10, min_samples=10, metric='euclidean', cluster_selection_method='eom',
                         prediction_data=True)

vectorizer_model = CountVectorizer(ngram_range=(1, 3), stop_words=list(stoplist), min_df=5, max_df=0.70)
topic_model = BERTopic(vectorizer_model=vectorizer_model, umap_model=umap_model, hdbscan_model=hdbscan_model,
                       language="greek", calculate_probabilities=False, verbose=True, diversity=0.80)
# .fit_transform(texts)
topics, probs = topic_model.fit_transform(texts, embeddings)
topic_model.save("C:\\Python\\torchidis\\omilies_model2")















'''
my_loaded_topic_model = BERTopic.load("C:\\Python\\myNewsScraper\\omilies_model", embedding_model=sentence_model)


for i in range(1131):
    t = my_loaded_topic_model.get_topic(i)
    for j in range(len(t)):
        print(t[j][0], end=' ')
    print('\n')
'''

