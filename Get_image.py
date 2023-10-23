from urllib import response
import requests
from bs4 import BeautifulSoup as bs
import random

def get_img_url():
    response=requests.get("https://www.pixiv.net/ranking.php")
    soup=bs(response.text,'html.parser')
    imgs=soup.find_all('section',class_='ranking-item')
    img_urls=list()
    for img in imgs:
        img_url='https://pixiv.cat/'+img.get('data-id')
        img_urls.append(img_url)
    response=requests.get("https://www.pixiv.net/ranking.php?mode=weekly")
    soup=bs(response.text,'html.parser')
    imgs=soup.find_all('section',class_='ranking-item')
    for img in imgs:
        img_url='https://pixiv.cat/'+img.get('data-id')
        img_urls.append(img_url)
    response=requests.get("https://www.pixiv.net/ranking.php?mode=monthly")
    soup=bs(response.text,'html.parser')
    imgs=soup.find_all('section',class_='ranking-item')
    for img in imgs:
        img_url='https://pixiv.cat/'+img.get('data-id')
        img_urls.append(img_url)
    response=requests.get("https://www.pixiv.net/ranking.php?mode=daily")
    soup=bs(response.text,'html.parser')
    imgs=soup.find_all('section',class_='ranking-item')
    for img in imgs:
        img_url='https://pixiv.cat/'+img.get('data-id')
        img_urls.append(img_url)
    return img_urls
def get_want_url(msg):
    params = {
    'word'   : 'かぐや様は告らせたい',
    'order'  : 'date_d',
    'mode'   : 'all',
    'p'      : '1',
    's_mode' : 's_tag_full',
    'type'   : 'illust_and_ugoira',
    'lang'   : 'zh_tw'
}
    params["word"]=msg


    response = requests.get('https://www.pixiv.net/ajax/search/illustrations/' + params['word'] + '?', params = params)
    soup=bs(response.text,'html.parser')
    soup=str(soup)
    soup_word=[]
    code_list=[]
    soup=soup.replace("{"," ")
    soup=soup.replace("}"," ")
    soup=soup.replace("["," ")
    soup=soup.replace("]"," ")
    soup=soup.replace(","," ")
    soup=soup.replace(":"," ")
    soup=soup.replace('"'," ")
    soup_word=soup.split()
    for i in range(len(soup_word)):
        if soup_word[i]=="id":
            img_url='https://pixiv.cat/'+soup_word[i+1]
            code_list.append(img_url)
            i+=1
    return code_list