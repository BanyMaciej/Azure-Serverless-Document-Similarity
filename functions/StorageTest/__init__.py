import logging
import pickle
from gensim.models import Doc2Vec
import json

import azure.functions as func


def preprocess_text(text):
  text = text.lower()

  tokens = text.split()

  tokens = [word.lower() for word in tokens]

  tokens = [word for word in tokens if word.isalpha()]

  # stopwords_set = set(stopwords.words('english'))
  # tokens = [word for word in tokens if not word in stopwords_set]

  return ' '.join(tokens)

def getVector(doc2vec, text):
  words = text.split()
  vector = doc2vec.infer_vector(words)
  return vector

def predict(logreg, vector):
  return logreg.predict(vector.reshape(1, -1))[0]


def main(req: func.HttpRequest, doc2vecblob, logregblob) -> func.HttpResponse:
  logging.info('Python HTTP trigger function processed a request.')

  doc2vec = pickle.load(doc2vecblob)
  logreg = pickle.load(logregblob)

  data = None
  try:
    req_body = req.get_json()
  except ValueError:
    pass
  else:
    data = req_body.get('text')

  if data:
    clean_text = preprocess_text(data)
    vector = getVector(doc2vec, clean_text)
    prediction = predict(logreg, vector)
    logging.info(f'Result: {prediction}')
    return func.HttpResponse(json.dumps({'result': int(prediction)}))
  else:
    return func.HttpResponse(
       json.dumps({'error': 'Bad request - not found "text" in json'}),
       status_code=400
    )
