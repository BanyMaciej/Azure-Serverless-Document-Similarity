from azure.data.tables import TableClient

class AzureStorageClient:
    
  def __init__(self, connection_string, table_name):
    self.table_client = TableClient.from_connection_string(conn_str=connection_string, table_name=table_name)
  
  def get_by_title(self, title):
    result = self.table_client.query_entities(
      filter=("RowKey eq '%s'" % title),
      select='PartitionKey, RowKey, RawWiki, CleanWiki'
    )
    result_list = list(result)
    return result_list[0] if len(result_list) > 0 else None
  
  def get_by_category(self, category):
    result = self.table_client.query_entities(
      filter=("PartitionKey eq '%s'" % category),
      select='PartitionKey, RowKey, RawWiki, CleanWiki'
    )
    return list(result)
  
  def get_table(self, as_generator=True):
    result = self.table_client.query_entities(
      filter=None,
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
      
      self.table_client.update_entity(entity)
      return True
    else:
      return False
  
  def update_by_dataframe(self, dataframe):
    inbatch = 0
    batch = self.table_client.create_batch()
    results = []
    for pk, indexes in dataframe.groupby('PartitionKey').groups.items():
      for idx in indexes:
        entity = dataframe.iloc[idx, :].to_dict()
        entity.pop('etag', None)
        batch.upsert_entity(entity)
        inbatch += 1
        if inbatch > 99:
          print("commit - exceeded")
          results.append(self.table_client.send_batch(batch))
          inbatch = 0
          batch = self.table_client.create_batch()
      if inbatch > 0:
        print("commit - pk")
        results.append(self.table_client.send_batch(batch))
        inbatch = 0
        batch = self.table_client.create_batch()
    return results


