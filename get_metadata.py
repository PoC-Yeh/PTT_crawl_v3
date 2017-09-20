from bs4 import BeautifulSoup
import requests
from datetime import datetime


def get_meta_text_common(url):    
    get_page_url = requests.get(url).text
    soup = BeautifulSoup(get_page_url, "html.parser")
    
    #get meta data
    text = soup.find("div", class_="bbs-screen bbs-content").text
    meta = soup.find_all("span", class_="article-meta-value")
    
    meta_text = []  #author, category, title, time
    for item in meta:
        meta_text.append(item.text)
    #print(meta_text)
    
    if len(meta_text) == 4:
        #deal with datetime format
        datetime_object = datetime.strptime( meta_text[3], '%a %b %d %H:%M:%S %Y')
        extract_date = "".join(("".join(list(str(datetime_object))[:10])).split("-"))

        #list of meta data in order
        final_text = [extract_date]  #date
        final_text.append("PTT")  #PTT
        final_text.append(meta_text[1]) #board
        final_text.append(meta_text[2]) #title
        final_text.append(meta_text[0]) #author
        #text_join = "; ".join(final_text)
        return(final_text)
