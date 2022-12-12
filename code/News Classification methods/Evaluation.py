# ============================= TFIDF CLASSIFIERS =========================================

cats = ['Αθλητισμός', 'Αστυνομικό', 'Δικαιοσύνη', 'Εκπαίδευση','Κοινωνία', 'Κόσμος', 'Οικονομία', 'Περιβάλλον', 'Πολιτική', 'Πολιτισμός', 'Τεχνολογία', 'Υγεία']
sns.heatmap(confusion_matrix(labels_test, model_prediction), annot = True,fmt="d",cmap='Blues',xticklabels=cats, yticklabels=cats)

# ====================================================================

def rename_cats(cat):
    cats = ['Αθλητισμός', 'Αστυνομικό', 'Δικαιοσύνη', 'Εκπαίδευση', 'Κοινωνία', 'Κόσμος', 'Οικονομία', 'Περιβάλλον',
            'Πολιτική', 'Πολιτισμός', 'Τεχνολογία', 'Υγεία']
    return cats.index(cat)
	
yy_test = y_test
yy_test['label'] = yy_test.apply(rename_cats)

pred_prob = model.predict_proba(features_test)
fpr = {}
tpr = {}
thresh = {}
n_class = 12

for i in range(n_class):
    fpr[i], tpr[i], thresh[i] = roc_curve(y_test['label'], pred_prob[:, i], pos_label=i)
	
# plotting    
plt.plot(fpr[0], tpr[0], linestyle='--', color='orange', label='Αθλητισμός')
plt.plot(fpr[1], tpr[1], linestyle='--', color='green', label='Αστυνομικό')
plt.plot(fpr[2], tpr[2], linestyle='--', color='blue', label='Δικαιοσύνη')
plt.plot(fpr[3], tpr[3], linestyle='--', color='r', label='Αστυνομικό')
plt.plot(fpr[4], tpr[4], linestyle='--', color='c', label='Κοινωνία')
plt.plot(fpr[5], tpr[5], linestyle='--', color='m', label='Κόσμος')
plt.plot(fpr[6], tpr[6], linestyle='--', color='y', label='Οικονομία')
plt.plot(fpr[7], tpr[7], linestyle='--', color='k', label='Περιβάλλον')
plt.plot(fpr[8], tpr[8], linestyle='--', color='violet', label='Πολιτική')
plt.plot(fpr[9], tpr[9], linestyle='--', color='lime', label='Πολιτισμός')
plt.plot(fpr[10], tpr[10], linestyle='--', color='pink', label='Τεχνολογία')
plt.plot(fpr[11], tpr[11], linestyle='--', color='sienna', label='Υγεία')
plt.title('ROC Καμπύλη')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive rate')
plt.legend(loc='best')
plt.savefig('Multiclass ROC', dpi=300)

# ========================================= DOC2VEC CLASSIFIERS =========================================

cats = ['Αθλητισμός', 'Αστυνομικό', 'Δικαιοσύνη', 'Εκπαίδευση','Κοινωνία', 'Κόσμος', 'Οικονομία', 'Περιβάλλον', 'Πολιτική', 'Πολιτισμός', 'Τεχνολογία', 'Υγεία']
sns.heatmap(confusion_matrix(y_test, model_prediction), annot = True,fmt="d",cmap='Blues',xticklabels=cats, yticklabels=cats)

# ===========================================================================================

def rename_cats(cat):
    cats = ['Αθλητισμός', 'Αστυνομικό', 'Δικαιοσύνη', 'Εκπαίδευση', 'Κοινωνία', 'Κόσμος', 'Οικονομία', 'Περιβάλλον',
            'Πολιτική', 'Πολιτισμός', 'Τεχνολογία', 'Υγεία']
    return cats.index(cat)
	
yy_test = y_test
yy_test['label'] = yy_test.apply(rename_cats)

pred_prob = model.predict_proba(test_vectors_dbow)
fpr = {}
tpr = {}
thresh = {}
n_class = 12

for i in range(n_class):
    fpr[i], tpr[i], thresh[i] = roc_curve(y_test['label'], pred_prob[:, i], pos_label=i)
	
# plotting    
plt.plot(fpr[0], tpr[0], linestyle='--', color='orange', label='Αθλητισμός')
plt.plot(fpr[1], tpr[1], linestyle='--', color='green', label='Αστυνομικό')
plt.plot(fpr[2], tpr[2], linestyle='--', color='blue', label='Δικαιοσύνη')
plt.plot(fpr[3], tpr[3], linestyle='--', color='r', label='Αστυνομικό')
plt.plot(fpr[4], tpr[4], linestyle='--', color='c', label='Κοινωνία')
plt.plot(fpr[5], tpr[5], linestyle='--', color='m', label='Κόσμος')
plt.plot(fpr[6], tpr[6], linestyle='--', color='y', label='Οικονομία')
plt.plot(fpr[7], tpr[7], linestyle='--', color='k', label='Περιβάλλον')
plt.plot(fpr[8], tpr[8], linestyle='--', color='violet', label='Πολιτική')
plt.plot(fpr[9], tpr[9], linestyle='--', color='lime', label='Πολιτισμός')
plt.plot(fpr[10], tpr[10], linestyle='--', color='pink', label='Τεχνολογία')
plt.plot(fpr[11], tpr[11], linestyle='--', color='sienna', label='Υγεία')
plt.title('ROC Καμπύλη')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive rate')
plt.legend(loc='best')
plt.savefig('Multiclass ROC', dpi=300)
