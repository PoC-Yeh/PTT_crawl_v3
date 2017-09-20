from bs4 import BeautifulSoup
import requests


def serp_title_link(soup, domain, url_list):
    title = soup.find_all("div", class_ = "title")
    for i in title:
        if i.find("a") != None:
            a = i.find("a").get("href")
            if domain in a:
                url_list.append(a)
            else:
                whole_a = domain + a
                url_list.append(whole_a)
        
#previous page url
def previous_page_link(soup, domain):
    previous = soup.find_all("a", class_ = "btn wide")[1]
    previous_url = domain + previous.get("href")
    return(previous_url)
