umap_model= UMAP(n_neighbors=15, n_components=5, min_dist=0.0, metric='cosine')
hdbscan_model = hdbscan.HDBSCAN(min_cluster_size=10, min_samples=10, metric='euclidean', cluster_selection_method='eom', prediction_data=True)

vectorizer_model = CountVectorizer(ngram_range=(1, 3), stop_words=list(stoplist), min_df=5, max_df=0.70)
topic_model = BERTopic(vectorizer_model=vectorizer_model, embedding_model=sentence_model, calculate_probabilities=False, verbose=True, diversity=0.75)
topics, probs = topic_model.fit_transform(texts, embeddings)

umap_emb = umap_model.fit_transform(embeddings)
indices = [index for index, topic in enumerate(topics) if topic != -1]
X = umap_emb[np.array(indices)]
labels = [topic for index, topic in enumerate(topics) if topic != -1]
# Calculate silhouette score
print(silhouette_score(X, labels))
hdb = hdbscan.HDBSCAN(gen_min_span_tree=True).fit(umap_emb)
# specify parameters and distributions to sample from
param_dist = {
                'min_samples': [10],
              'min_cluster_size':[10],  
              'cluster_selection_method' : ['eom'],
              'metric' : ['euclidean'] 
            }
#validity_scroer = "hdbscan__hdbscan___HDBSCAN__validity_index"
validity_scorer = make_scorer(hdbscan.validity.validity_index,greater_is_better=True)
n_iter_search = 20
random_search = RandomizedSearchCV(hdb
                                  ,param_distributions=param_dist
                                  ,n_iter=n_iter_search
                                  ,scoring=validity_scorer 
                                  ,random_state=42)
random_search.fit(umap_emb)
print(f"Best Parameters {random_search.best_params_}")
print(f"DBCV score :{random_search.best_estimator_.relative_validity_}")


# Preprocess Documents
documents = pd.DataFrame({"Document": texts,
                          "ID": range(len(texts)),
                          "Topic": topics})
documents_per_topic = documents.groupby(['Topic'], as_index=False).agg({'Document': ' '.join})
cleaned_docs = topic_model._preprocess_text(documents_per_topic.Document.values)

# Extract vectorizer and analyzer from BERTopic
vectorizer = topic_model.vectorizer_model
analyzer = vectorizer.build_analyzer()

# Extract features for Topic Coherence evaluation
words = vectorizer.get_feature_names()
tokens = [analyzer(doc) for doc in cleaned_docs]
topic_words = topic_model.c_tf_idf_

# top div
output = {'topic-word-matrix': topic_words, 'topics': tokens, 'topic-document-matrix': probs}
t_d = TopicDiversity(topk=10)
t_d_s = t_d.score(output)
print('topic diversity = ', t_d_s)

# coherence
npmi = Coherence(texts=tokens, topk=10, measure='c_npmi')
npmi_s = npmi.score(output)
print('c_npmi = ',npmi_s)

npmi = Coherence(texts=tokens, topk=10, measure='u_mass')
npmi_s = npmi.score(output)
print('u_mass = ', npmi_s)

topic_model.get_topic_info()

for i in range(20):
	x = topic_model.get_topic(i)
	y = ', '.join(elem[0] for elem in x)
	print(f"{i+1}: {y}")          
