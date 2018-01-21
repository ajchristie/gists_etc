import mechanize
import cookielib
import unicodedata as ucd
from bs4 import BeautifulSoup as BS
import numpy as np
import pandas as pd
import time

## This version is for palmspringslife.com

months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]

scopes = pd.DataFrame()

## Ready the mechanize browser (undisguised, response is 403)
br = mechanize.Browser()
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)
br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_robots(False)
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

#br.set_debug_http(True)
#br.set_debug_redirects(True)
#br.set_debug_responses(True)

urls = []
## following will grab reverse chronological list of archive page urls
for i in range(1,13):
    url = "https://www.palmspringslife.com/page/"+str(i)+"/?s=horoscope"
    response = br.open(url)
    html = response.read()
    soup = BS(html,'lxml')
    for link in soup.find_all('h2',attrs={'class':'entry-title'}):
        urls.append(link.a.get('href'))

with open('palmspringsurls.csv','w') as file:
    writer = csv.writer(file)
    writer.writerow(urls)

## harvest horoscopes as text blocks from archive pages
for url in urls:
    try:
        response = br.open(url)
        html = response.read()
        soup = BS(html,'lxml')
        block = soup.find('div',attrs={'class':'entry-wrap'})
        #block.em.decompose()
        text = block.get_text(" ",strip=True)
        scopes = scopes.append([[text]],ignore_index=True)

    except:
        print "Error accessing "+url+" ! Moving on..."


scopes.columns = ["year","month","entry, yo"]

scopes.to_csv('palmsprings_archives_utf.csv',encoding='utf-8')
##scopes.to_csv('palmsprings_archives.csv')
