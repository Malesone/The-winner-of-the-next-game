import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import pathlib

headers = {'User-Agent': 
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

page = "https://fbref.com/it/comp/11/2021-2022/Statistiche-di-Serie-A-2021-2022"
pageTree = requests.get(page)
self.soup = BeautifulSoup(pageTree.text, features="lxml")