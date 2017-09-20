from bs4 import BeautifulSoup
import requests
import re

#text crawling 
#replace ip, date in the comment with ""

def page_text(forum_url):
    page_url = forum_url
    get_page = requests.get(page_url).text
    content = BeautifulSoup(get_page, "html.parser")

    #text and meta data
    text = content.find("div", class_="bbs-screen bbs-content").text
    """
    meta = content.find_all("span", class_="article-meta-value")
    meta_text = []  #author, category, title, time
    for item in meta:
        meta_text.append(item.text)
    """
    #replacement
    ip = re.findall(r"\d+.\d+.\d+.\d+", text)  #ex 101.15.49.192
    date = re.findall(r"\d{2}.\d{2}", text)  #ex 03/15
    for ip_inside in ip:
        text = text.replace(ip_inside, "")
    for date_inside in date:
        text = text.replace(date_inside, "")
    
    #split text with \n    
    split_text = text.split("\n")
    new_split_text= []
    for text in split_text[1:]:
        a = text.split(" ")
        for word in a:
            if len(word) > 2 and "http" not in word and word != '發信站:' and word != '批踢踢實業坊(ptt.cc),' and word != '來自:' and word != '文章網址:':
                new_split_text.append(word)

    return(new_split_text)
    
    
#clean puctuations and comment ids 
def text_without_garbage(url):
    text_list = page_text(url)
    without_name = []
    
    garbage = []
    for x in text_list:
        name = re.findall(r"[-a-zA-Z\d]+.{1}", x)  #ex OrangeLee123:
        if len(name) != 0:
            for name_inside in name:
                garbage.append(name_inside)

    new_text = list(filter(lambda x: x not in garbage, text_list))
    without_name.append(new_text)
    
    others = ["(", "（", ")", "）", ",", "「", "」", "。", "!", "！", ".", "～", ":", "~", "^" ,"?", "？", "＋", "+", "，", "＝", "*", "|", "_", "-", "[", "]", ">", "<", "//", "\\", "*", "%", "@@", "XD", "="]
    final = []
    for wn in without_name:
        for wn_inside in wn:
            without_others = list(filter(lambda x: x not in others, wn_inside))
            if len(without_others) > 0:
                join_without_other = "".join(without_others).strip()
                final.append(join_without_other)
    return(" ".join(final))   
