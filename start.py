from configparser import ConfigParser
from dataprocessor import DataProcessor
from dataservices import DataLoader, DataWriter
from wikiscrapper import WikiScrapper


def main():
  config = ConfigParser()
  config.read("config.ini")

  interval = config.getint("main", "interval")
  base_endpoint = config.get("main", "base_endpoint")

  dataframe = DataLoader(input_file="test.csv").get_dataframe()
  scrapper = WikiScrapper(interval, base_endpoint)
  scrapper.start(dataframe)
  dataProcessor = DataProcessor()
  dataProcessor.preprocess_dataframe(dataframe)
  DataWriter(output_file="result.csv").save_result(dataframe)


if __name__ == '__main__':
  main()