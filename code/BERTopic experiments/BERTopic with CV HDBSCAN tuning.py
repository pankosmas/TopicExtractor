for i in [15, 25, 50]:
    umap_model = UMAP(n_neighbors=i, n_components=5, min_dist=0.0, metric='cosine', random_state=42)
    umap_emb = umap_model.fit_transform(embeddings)
    hdb = hdbscan.HDBSCAN(gen_min_span_tree=True).fit(umap_emb)

    # specify parameters and distributions to sample from
    param_dist = {
		'min_samples':[10],
        'min_cluster_size': [10],
        'cluster_selection_method': ['eom'],
        'metric': ['euclidean']
    }
 
    # validity_scroer = "hdbscan__hdbscan___HDBSCAN__validity_index"
    validity_scorer = make_scorer(hdbscan.validity.validity_index, greater_is_better=True)

    n_iter_search = 20
    random_search = RandomizedSearchCV(hdb
                                       , param_distributions=param_dist
                                       , n_iter=n_iter_search
                                       , scoring=validity_scorer
                                       , random_state=42)

    random_search.fit(umap_emb)
    print(f"Best Parameters {random_search.best_params_}")
    print(f"DBCV score :{random_search.best_estimator_.relative_validity_}")

    hdbscan_model = HDBSCAN(min_cluster_size=random_search.best_params_['min_cluster_size'], metric=random_search.best_params_['metric'], cluster_selection_method=random_search.best_params_['cluster_selection_method'], prediction_data=True)
    vectorizer_model = CountVectorizer(ngram_range=(1, 3), stop_words=list(stoplist), min_df=5, max_df=0.70)
    topic_model = BERTopic(vectorizer_model=vectorizer_model, umap_model=umap_model, hdbscan_model=hdbscan_model, language="greek", calculate_probabilities=False, diversity=0.75,
                           verbose=True)  # .fit_transform(texts)  
    topics, probs = topic_model.fit_transform(texts, embeddings)
    
    print(topic_model.get_topic_info())
    
    indices = [index for index, topic in enumerate(topics) if topic != -1]
    X = umap_emb[np.array(indices)]
    labels = [topic for index, topic in enumerate(topics) if topic != -1]

    # Calculate silhouette score
    print(silhouette_score(X, labels))

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
    print('c_npmi = ', npmi_s)
    npmi = Coherence(texts=tokens, topk=10, measure='u_mass')
    npmi_s = npmi.score(output)
    print('u_mass = ', npmi_s)
    npmi = Coherence(texts=tokens, topk=10, measure='c_uci')
    npmi_s = npmi.score(output)
    print('c_uci = ', npmi_s)
    print("---------------------------------------------------------------------------------------")

    hierarchical_topics = topic_model.hierarchical_topics(texts)

    fig = topic_model.visualize_barchart(top_n_topics=20)
    fig.write_html("C:\\Users\\Panagiotis\\Desktop\\peiramata\\peirama1\\barchart" + str(i) + ".html")
    fig = topic_model.visualize_heatmap(top_n_topics=50)
    fig.write_html("C:\\Users\\Panagiotis\\Desktop\\peiramata\\peirama1\\heatmap" + str(i) + ".html")
    fig = topic_model.visualize_documents(texts, embeddings=embeddings, hide_annotations=True, hide_document_hover=True)
    fig.write_html("C:\\Users\\Panagiotis\\Desktop\\peiramata\\peirama1\\documents" + str(i) + ".html")
    fig = topic_model.visualize_hierarchical_documents(texts, hierarchical_topics, embeddings=embeddings,
                                                       hide_annotations=True, hide_document_hover=True)
    fig.write_html("C:\\Users\\Panagiotis\\Desktop\\peiramata\\peirama1\\hierarchical_documents" + str(i) + ".html")
    fig = topic_model.visualize_hierarchy(hierarchical_topics=hierarchical_topics, top_n_topics=100,
                                          orientation='bottom')
    fig.write_html("C:\\Users\\Panagiotis\\Desktop\\peiramata\\peirama1\\hierarchy" + str(i) + ".html")
    fig = topic_model.visualize_topics(top_n_topics=100)
    fig.write_html("C:\\Users\\Panagiotis\\Desktop\\peiramata\\peirama1\\topics_chart" + str(i) + ".html")
    fig = topic_model.visualize_topics()
    fig.write_html("C:\\Users\\Panagiotis\\Desktop\\peiramata\\peirama1\\topics_chart2" + str(i) + ".html")        
    
