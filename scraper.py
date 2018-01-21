import mechanize
import cookielib
import unicodedata as ucd
from bs4 import BeautifulSoup as BS
import numpy as np
import pandas as pd
import time

## This version is for astrostyle.com

signs = ["aries", "taurus", "gemini", "cancer", "leo", "virgo", "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"]

scopes = pd.DataFrame()

## Horoscopes are stored on individual pages per sign/month/year. They contain separate (long) horoscopes around different themes as well as an overview horoscope. These are all scraped and stored separately.

## Ready the mechanize browser (undisguised, response is 403)
br = mechanize.Browser()
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)
br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_robots(False)
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

for year in xrange(2013,2017):
    for month in xrange(1,12):
        if year == 2017 and month > 4:
            break
        for sign in signs:
            url = "http://astrostyle.com/?pagename=single-archive&hyear="+str(year)+"&hmonth="+str(month)+"&sign="+sign
            response = br.open(url)
            html = response.read()
            soup = BS(html,'lxml')
            overview = soup.find('div',attrs={'id':'standard'}).get_text(strip=True)
            overview = ucd.normalize("NFKD",overview) #reg encoding
            overview = overview.replace(u"\u2019","'") #reg single-quotes
            overview = overview.replace(u"\u2014","--") #reg m-dashes
            love = soup.find('div',attrs={'id':'love'}).get_text(strip=True)
            love = ucd.normalize("NFKD",love)
            love = love.replace(u"\u2019","'")
            love = love.replace(u"\u2014","--")
            money = soup.find('div',attrs={'id':'money'}).get_text(strip=True)
            money = ucd.normalize("NFKD",money)
            money = money.replace(u"\u2019","'")
            money = money.replace(u"\u2014","--")
            health = soup.find('div',attrs={'id':'health'}).get_text(strip=True)
            health = ucd.normalize("NFKD",health)
            health = health.replace(u"\u2019","'")
            health = health.replace(u"\u2014","--")
            scopes = scopes.append([[sign,month,year,overview,love,money,health]],ignore_index=True)
            time.sleep(1)

## Honest Q: Is there a more efficient way to do this? Like build rows or even arrays inside loops and then append outside? Are the appendings heavy, resource-wise?
scopes.columns = ["Sign", "Month", "Year", "Overview", "Love&Rel", "Money&Career", "Health&Happy"]

## For safety, export in both utf-8 and ascii
scopes.to_csv('astrostyle_archives_utf.csv',encoding='utf-8')
scopes.to_csv('astrostyle_archives.csv')
