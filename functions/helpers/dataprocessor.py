
class DataProcessor:

  def preprocess_text(self, text):
    text = text.lower()

    tokens = text.split()

    tokens = [word.lower() for word in tokens]

    tokens = [word for word in tokens if word.isalpha()]

    # stopwords_set = set(stopwords.words('english'))
    # tokens = [word for word in tokens if not word in stopwords_set]

    return ' '.join(tokens)
  
  def preprocess_dataframe(self, dataframe, in_column = 'RawWiki', out_column = 'CleanWiki'):
    dataframe.loc[:, out_column] = dataframe.loc[:, in_column].apply(self.preprocess_text)