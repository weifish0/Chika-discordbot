import urllib.request as req
import bs4

def get_covid_data():

    url = 'https://covid-19.nchc.org.tw/'
  
    # 建立一個 Requst 物件, 附加 Request Headers 的資訊
    request = req.Request(url,headers = {
        'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
    })
    
    # 讀取資料
    with req.urlopen(request) as response:
        data = response.read().decode('utf-8')

    # 查找標籤
    root = bs4.BeautifulSoup(data,'html.parser')
    today_covid_cases=str(root.find('h1',class_='country_recovered mb-1 text-info'))
        
    return today_covid_cases[today_covid_cases.find('</small>')+8: today_covid_cases.find('</h1>')]
