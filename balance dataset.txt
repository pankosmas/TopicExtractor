df = pd.read_csv('C:\\Python\\torchidis\\process_text_imbala.csv')
df.index

df['ftext'] = df['pars_parsed'].apply(lambda x : str(x).replace('  ', ' '))
df['ftext'] = df['ftext'].apply(lambda x : str(x).replace('  ', ' '))
x_train, x_test, y_train, y_test = train_test_split(df['ftext'],
                                                    df['category_target'],
                                                    test_size=0.3,
                                                    random_state=8)
													
label_encoder = preprocessing.LabelEncoder()
df['category_target'] = label_encoder.fit_transform(df['category'])
df.head()

frame = {'ftext': x_train, 'label': y_train}
df = pd.DataFrame(frame)

import math
categories = [0,1,2,3,4,5,6,7,8,9,10,11]
sum = len(df[df['label']==8])
nn = df
for ctg in categories:
  dd = df[df['label']==ctg]
  subsum = len(dd)
  d = math.floor(sum / subsum)
  print(d)
  u = sum % subsum
  for i in range(d-1):
    nn = pd.concat([nn, dd])
  df2 = dd.head(u)
  nn = pd.concat([nn, df2])
len(nn)

x_train = nn['ftext'].squeeze()
y_train = nn['label'].squeeze()

