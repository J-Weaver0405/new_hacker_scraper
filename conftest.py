import os
import pytest
import sys
import requests
from bs4 import BeautifulSoup
sys.path.append('..')
from dotenv import load_dotenv
load_dotenv()

@pytest.fixture
def page_source():
	html = requests.get(os.getenv('URL'))
	print(html)
	bs = BeautifulSoup(html.text, 'html.parser')
	return bs
