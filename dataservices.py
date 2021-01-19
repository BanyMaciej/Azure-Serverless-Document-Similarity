import pandas as pd

class DataLoader:
  _fields_types = {'PartitionKey': str, 
                   'RowKey': str, 
                   'RawWiki': str, 
                   'CleanWiki': str}
  
  def __init__(self, input_file):
    self.input_file = input_file
  
  
  def get_dataframe(self):
    return pd.read_csv(self.input_file, delimiter='\t', dtype=self._fields_types)


class DataWriter:
  _fields_types = {'PartitionKey': str, 
                   'RowKey': str, 
                   'RawWiki': str, 
                   'CleanWiki': str}
  
  def __init__(self, output_file):
    self.output_file = output_file
  
  
  def save_result(self, result):
    result.to_csv(self.output_file, sep='\t', columns=self._fields_types.keys(), index=False)
    return True
    