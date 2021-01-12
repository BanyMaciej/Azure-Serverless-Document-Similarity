import logging
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from sklearn import utils
from tqdm import tqdm

class ModelProcessor:
  tags_ids = {}
  dataframe = None

  def __init__(self):
    print("Initialized ModelProcessor")
  
  def _record_to_tagged_document(self, record):
    return TaggedDocument(record['CleanWiki'].split(), [self.tags_ids.get(record['Category'])])
  
  def train(self, dataframe, vector_size=100):
    self.tags_ids = {tag: idx for idx, tag in enumerate(dataframe['Category'].unique())}
    records = dataframe.to_records(index=False)
    documents = [self._record_to_tagged_document(record) for record in records]
    self.model = Doc2Vec(documents, vector_size=vector_size, min_count=2, workers=4)
    self.model.delete_temporary_training_data(keep_doctags_vectors=True, keep_inference=True)
    return self.model
  
  def train2(self, dataframe, epochs = 30, vector_size=100):
    self.tags_ids = {tag: idx for idx, tag in enumerate(dataframe['Category'].unique())}
    records = dataframe.to_records(index=False)
    documents = [self._record_to_tagged_document(record) for record in records]

    self.model = Doc2Vec(dm=0, vector_size=vector_size, negative=5, hs=0, min_count=2, sample = 0, workers=4)
    self.model.build_vocab([x for x in tqdm(documents)])

    for _ in tqdm(range(epochs)):
      self.model.train(utils.shuffle(documents), total_examples=len(documents), epochs=1)
      self.model.alpha -= 0.002
      self.model.min_alpha = self.model.alpha

  
  def get_vector(self, words):
    return self.model.infer_vector(words)