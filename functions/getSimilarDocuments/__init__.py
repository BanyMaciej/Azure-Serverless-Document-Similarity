import logging
import pickle
from gensim.models import Doc2Vec
import json
import os

from helpers.wikiscrapper import WikiScrapper
from helpers.dataprocessor import DataProcessor
from helpers.azurestorageclient import AzureStorageClient

import azure.functions as func


def get_category_name(category_id):
  d = {0: 'Animals', 1: 'Sports', 2: 'Instruments'}
  return d.get(category_id)

def getVector(doc2vec, text):
  words = text.split()
  vector = doc2vec.infer_vector(words)
  return vector

def predict(logreg, vector):
  return logreg.predict(vector.reshape(1, -1))[0]

def get_storage_client():
  azure_storage_conn = os.environ['AzureWebJobsStorage']
  azure_storage_table = os.environ['AzureStorageTable']
  return AzureStorageClient(azure_storage_conn, azure_storage_table)

def get_similar_documents(doc, doc2vec, logreg):
  base_wikipedia_endpoint = os.environ['WikipediaBaseEndpoint']
  
  clean_text = DataProcessor().preprocess_text(doc)
  vector = getVector(doc2vec, clean_text)
  prediction = predict(logreg, vector)
  category = get_category_name(prediction)

  azure_storage = get_storage_client()
  similar_documents = azure_storage.get_by_category(category)
  
  result = [{
      'url': base_wikipedia_endpoint+d['RowKey'],
      'title': d['RowKey'],
      'summary': d['RawWiki'][:100]+'...' if len(d['RawWiki']) > 100 else d['RawWiki']
    } for d in similar_documents]
  return result

def main(req: func.HttpRequest, doc2vecblob, logregblob) -> func.HttpResponse:
  logging.info('Python HTTP trigger function processed a request.')

  base_wikipedia_endpoint = os.environ['WikipediaBaseEndpoint']

  doc2vec = pickle.load(doc2vecblob)
  logreg = pickle.load(logregblob)

  text = req.params.get('text')
  url = req.params.get('url')
  title = req.params.get('title')
  try:
    req_body = req.get_json()
  except ValueError:
    pass
  else:
    text = req_body.get('text')
    url = req_body.get('url')
    title = req_body.get('title')
  
  data = None
  if text:
    data = text
  elif url:
    scrapper = WikiScrapper(base_wikipedia_endpoint)
    url_title = url.split('/')[0]
    data = scrapper.get(url_title)
  elif title:
    scrapper = WikiScrapper(base_wikipedia_endpoint)
    data = scrapper.get(title)

  if data:
    similar_results = get_similar_documents(data, doc2vec, logreg)
    return func.HttpResponse(
      json.dumps({'result': similar_results}),
      mimetype="application/json"
    )
  else:
    return func.HttpResponse(
       json.dumps({'error': 'Bad request - not found "text" in json'}),
       status_code=400
    )
