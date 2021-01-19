from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.tablebatch import TableBatch
from azure.cosmosdb.table.models import Entity

class AzureStorageClient:

  def __init__(self, account_name, account_key, table_name):
    self.table_service = TableService(account_name=account_name, account_key=account_key)
    self.table_name = table_name
  
  def get_by_title(self, title):
    result = self.table_service.query_entities(
      self.table_name, 
      filter=("RowKey eq '%s'" % title),
      select='PartitionKey, RowKey, RawWiki, CleanWiki'
    )
    result_list = list(result)
    return result_list[0] if len(result_list) > 0 else None
  
  def get_by_category(self, category):
    result = self.table_service.query_entities(
      self.table_name, 
      filter=("PartitionKey eq '%s'" % category),
      select='PartitionKey, RowKey, RawWiki, CleanWiki'
    )
    return list(result)
  
  def get_table(self, as_generator=True):
    result = self.table_service.query_entities(
      self.table_name,
      select='PartitionKey, RowKey, RawWiki, CleanWiki'
    )
    if as_generator:
      return result
    else:
      return list(result)
  
  def set_wiki(self, title, *, raw_wiki=None, clean_wiki=None):
    entity = self.get_by_title(title)
    if entity is not None:
      if raw_wiki is None and clean_wiki is None:
        print('No update necessary')
        return False
      
      if raw_wiki is not None:
        entity['RawWiki'] = raw_wiki
      if clean_wiki is not None:
        entity['CleanWiki'] = clean_wiki
      
      self.table_service.update_entity(self.table_name, entity)
      return True
    else:
      return False
  
  def update_by_dataframe(self, dataframe):
    inbatch = 0
    batch = TableBatch()
    result = []
    for pk, indexes in dataframe.groupby('PartitionKey').groups.items():
      for idx in indexes:
        entity = dataframe.iloc[idx, :].to_dict()
        entity.pop('etag', None)
        batch.insert_or_merge_entity(entity)
        inbatch += 1
        if inbatch > 99:
          print("commit - exceeded")
          result += self.table_service.commit_batch(self.table_name, batch)
          inbatch = 0
          batch = TableBatch()
      if inbatch > 0:
        print("commit - pk")
        result += self.table_service.commit_batch(self.table_name, batch)
        inbatch = 0
        batch = TableBatch()
    return result


