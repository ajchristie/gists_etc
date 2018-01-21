import mechanize
import cookielib
import unicodedata as ucd
from bs4 import BeautifulSoup as BS
import numpy as np
import pandas as pd
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8') ## to avoid unicode decode errors when opening pages

## This version is for mountaintimes.info

signs = ["aries", "taurus", "gemini", "cancer", "leo", "virgo", "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"]

## Ready the mechanize browser (undisguised, response is 403)
br = mechanize.Browser()
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)
br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_robots(False)
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

urls = []
for link in soup.find_all('a',attrs={'class':'businessLink'}):
    urls.append(link.get('href'))

for i in range(2,13):
    url = "http://mountaintimes.info/category/horoscope-archives/page/"+str(i)
    response = br.open(url)
    html = response.read()
    soup = BS(html,'lxml')
    for link in soup.find_all('a',attrs={'class':'businessLink'}):
        urls.append(link.get('href'))

with open('mountaintimessurls.csv','w') as file:
    writer = csv.writer(file)
    writer.writerow(urls)

scopes = pd.DataFrame()

for url in urls:
    try:
        response = br.open(url)
        html = response.read()
        soup = BS(html,'lxml')
        for sign in signs:
            block = soup.find('div',attrs={'id':sign})
            block.p.decompose() ##remove horoscopeName
            dates = block.p.get_text(strip=True) ##remove/capture horoscopeDates
            block.p.decompose() ##remove horoscopeDates 
            scopes = scopes.append([[sign,dates,block.p.get_text(strip=True)]],ignore_index=True)
        #block.em.decompose()
        #text = block.get_text(" ",strip=True)
        #scopes = scopes.append([[text]],ignore_index=True)

    except:
        print "Error accessing "+url+" ! Moving on..."

scopes.columns = ['Sign','Dates','Horoscope']

scopes.to_csv('mountaintimesarchive.csv',encoding='utf-8')
