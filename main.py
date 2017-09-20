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

def ptt_url_implement(board_name, index_num):
    domain = "https://www.ptt.cc/"
    url = "https://www.ptt.cc/bbs/{}/index{}.html".format(board_name, index_num)

    ##########get url
    url_list = []
    count = 1
    page_count = 0
    bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength) 

    while True:
        serp_url = requests.get(url).text
        soup = BeautifulSoup(serp_url, "html.parser")
        serp_title_link(soup, domain, url_list)
        page_count += 1 #bar
        bar.update(page_count)  #bar

        #break when the last page is finished
        last_page = "https://www.ptt.cc//bbs/{}/index1.html".format(board_name)
        if url == last_page:
            break
        previous_page_link(soup, domain)
        url = previous_page_link(soup, domain)


        #write csv automatically after crawling every 500 pages
        if count < 500:
            count += 1
        elif count == 500:
            count = 1
            pickle.dump(url_list,open("ptt_{}_url_pickle.txt".format(board_name), "wb"))
            for_csv_url_list = []
            for i in url_list:
                list_list = []
                list_list.append(i)
                for_csv_url_list.append(list_list)

            f = open('ptt_{}_url.csv'.format(board_name), 'w')
            w = csv.writer(f)
            w.writerows(for_csv_url_list)

            f.close()


    #save again after the loop being finished 
    pickle.dump(url_list,open("ptt_{}_url_pickle.txt".format(board_name), "wb"))
    for_csv_url_list = []
    for i in url_list:
        list_list = []
        list_list.append(i)
        for_csv_url_list.append(list_list)

    f = open('ptt_{}_url.csv'.format(board_name), 'w')
    w1 = csv.writer(f)
    w1.writerows(for_csv_url_list)
    f.close()
    return(url_list)


def ptt_text_implement(board_name, url_list):
    url_meta_text_list = []
    save_count = 0
    url_count = 0
    bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)

    for url in url_list:
        try:
            page_text(url)
            text_whole = [url]
            meta = get_meta_text_common(url)
            for meta_content in meta:
                text_whole.append(meta_content)
            text_whole.append(text_without_garbage(url))
            #print(text_whole)

            url_meta_text_list.append(text_whole)

            url_count += 1 #bar
            bar.update(url_count)  #bar


            if save_count < 500:
                save_count += 1

            elif save_count == 500:
                save_count = 1
                pickle.dump(url_meta_text_list,open("ptt_{}_text_pickle.txt".format(board_name), "wb"))

                f = open('ptt_{}_text.csv'.format(board_name), 'w')
                w2 = csv.writer(f)
                w2.writerows(url_meta_text_list)
                f.close()

            if url_count % 2000 == 0:
                time.sleep(60*15)

        except:
            continue


    #save again after the loop being finished 
    pickle.dump(url_meta_text_list,open("ptt_{}_textpickle.txt".format(board_name), "wb"))
    f = open('ptt_{}_text.csv'.format(board_name), 'w')
    w3 = csv.writer(f)
    w3.writerows(url_meta_text_list)

    f.close()
    return(url_meta_text_list)
