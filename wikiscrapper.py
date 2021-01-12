import asyncio
import threading
from bs4 import BeautifulSoup
import pandas as pd
import requests
from typing import Any, Callable


import asyncio

class WikiScrapper:
  is_running = False
  on_finish = None

  def __init__(self, interval, base_endpoint):
    self.interval = interval
    self.base_endpoint = base_endpoint
    self._loop = asyncio.get_event_loop()

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
        elif tag.has_attr('class'):
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

    self.dataframe.loc[self.dataframe['Title'] == title, 'RawWiki'] = raw_header
    
    print('Processed "%s", waiting %d seconds' % (title, self.interval))


  async def _run(self):
    for title in self._titles_iter:
      self._process(title)
      await asyncio.sleep(self.interval)

  def start(self, dataframe):
    self.dataframe = dataframe
    self._titles_iter = iter(dataframe['Title'])
    self.is_running = True
    self._task = self._loop.create_task(self._run())
    try:
      self._loop.run_until_complete(self._task)
      return self.dataframe
    except asyncio.CancelledError:
      pass
