import csv
import progressbar
import re
import requests
import time
import pickle
from bs4 import BeautifulSoup
from get_url import *
from get_text import *
from get_metadata import *
from main import *

url_list = ptt_url_implement("MakeUp", "2")
print(len(url_list))

url_meta_text_list = ptt_text_implement("MakeUp")
print(len(url_meta_text_list))
