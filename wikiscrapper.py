import asyncio
import threading
from bs4 import BeautifulSoup
import pandas as pd
import requests
from typing import Any, Callable


import asyncio

class WikiScrapper:


  def __init__(self, base_endpoint):
    self.base_endpoint = base_endpoint

  def _get_header_text(self, soup):
    content = soup.find("div", {"class": 'mw-parser-output'})
    header_texts = ""
    if content is not None:
      for tag in content.findChildren(recursive=False):
        if tag.name != "p":
          if not header_texts:
            continue
          else:
            return header_texts.strip()
        elif tag.has_attr('class') or tag.findChild(attrs={'id': 'coordinates'}, recursive=True):
          continue
        tag_text = tag.get_text()

        tag_text = tag_text.replace('\n', ' ')

        header_texts += tag_text
    return header_texts.strip()

  def _process(self, title):
    endpoint = self.base_endpoint + title.replace(' ', '_')
    response = requests.get(url=endpoint)

    print('Processing "%s"..., got status %d' % (title, response.status_code))

    soup = BeautifulSoup(response.content, 'html.parser')

    raw_header = self._get_header_text(soup)
    
    return raw_header
  
  def _save_to_dataframe(self, title, result):
    self.dataframe.loc[self.dataframe['RowKey'] == title, 'RawWiki'] = result

  async def _run(self):
    for title in self._titles_iter:
      result = self._process(title)
      self._save_to_dataframe(title, result)
      await asyncio.sleep(self.interval)

  def start(self, data, interval = 10):
    self.interval = interval
    if isinstance(data, pd.DataFrame):
      self.dataframe = data
    else:
      self.dataframe = pd.DataFrame(data)
    self._titles_iter = iter(self.dataframe['RowKey'])
    self._loop = asyncio.get_event_loop()
    self._task = self._loop.create_task(self._run())
    try:
      self._loop.run_until_complete(self._task)
      return self.dataframe
    except asyncio.CancelledError:
      return None
  
  def get(self, title):
    return self._process(title)
  