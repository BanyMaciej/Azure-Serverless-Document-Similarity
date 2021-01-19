from configparser import ConfigParser
from dataprocessor import DataProcessor
from azurestorageclient import AzureStorageClient
from wikiscrapper import WikiScrapper

def main():
  config = ConfigParser()
  config.read("config.ini")

  interval = config.getint("main", "interval")
  base_endpoint = config.get("main", "base_endpoint")

  account_name = config.get("azure", "storage_account")
  account_key = config.get("azure", "storage_account_key")

  azure_client = AzureStorageClient(account_name, account_key, 'asdsWiki')
  data = azure_client.get_table()
  scrapper = WikiScrapper(base_endpoint)
  dataframe = scrapper.start(data, interval)
  dataProcessor = DataProcessor()
  dataProcessor.preprocess_dataframe(dataframe)
  azure_client.update_by_dataframe(dataframe)

if __name__ == '__main__':
  main()