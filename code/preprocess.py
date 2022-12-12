# -------------------------------------------------------------------------- AFAIRESH EIDIKWN XARAKTHRWN KAI ARI8MWN KAI KENWN

def process_text(text):
  text = text.replace('\n', ' ')
  text = text.replace('\xa0', '')
  text = ''.join([i for i in text if not i.isdigit()])
  while '  ' in text:
    text = text.replace('  ', ' ')
  return text
  
  
# --------------------------------------------------------------------------- DATASET PRIMEMINISTER XWRISMOS SE PARAGRAFOYS

df = pd.read_csv("/content/drive/MyDrive/datasets/primeminister.csv", encoding="utf-8")
df = df.dropna(subset=['text'])
# df = df[df.text != '\n']

df['ptext'] = df['text'].apply(process_text)

texts = df['ptext'].tolist()

new_texts = []
for text in texts:
    paragraphs = str(text).split('\n')
    for par in paragraphs:
        if par != ' ':
            new_texts.append(par)

df.head()
