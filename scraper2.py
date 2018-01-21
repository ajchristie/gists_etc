import mechanize
import cookielib
import unicodedata as ucd
from bs4 import BeautifulSoup as BS
import numpy as np
import pandas as pd
import time
import re

## This version is for free-horoscope.com

signs = ["aries", "taurus", "gemini", "cancer", "leo", "virgo", "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"]

months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]

scopes = pd.DataFrame()

## Horoscopes are stored on individual pages per sign/month/year. They are divided into different sections and are long as-is, but we'll just grab everything for now and apply processing later if appropriate.

## Ready the mechanize browser (undisguised, response is 403)
br = mechanize.Browser()
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)
br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_robots(False)
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

## To avoid repeatedly compiling the comment-removal regex
pattern = re.compile("<!--(.+?)-->",re.S)

for year in xrange(2013,2017):
    for month in months:
        for sign in signs:
            url = "http://www.free-horoscope.com/horoscopes/monthly/"+month+"-"+str(year)+"/"+sign+".htm"
            response = br.open(url)
            html = response.read()
            soup = BS(html,'lxml')
            scope = soup.find('td',attrs={'class':'txt'})
            ## Remove extraneous elements
            divs = scope.find_all("div")
            for match in divs:
                match.decompose()
            anchors = scope.find_all("a")
            for match in anchors:
                scope.a.decompose()
            heads = scope.find_all("h3")
            for match in heads:
                scope.h3.decompose()
            pars = scope.find_all("p")
            for match in pars:
                scope.p.decompose()
            record = scope.get_text(" ", strip=True)
            record = ucd.normalize("NFKD",record)
            ## Remove comments
            record = re.sub(pattern,"",record)
            scopes = scopes.append([[sign,month,year,record]],ignore_index=True)
            time.sleep(1)

scopes.columns = ["Sign", "Month", "Year", "Horoscope"]

##for safety, export in utf-8 and ascii, both
scopes.to_csv('free-horoscope_archives_utf.csv', encoding='utf-8')
scopes.to_csv('free-horoscope_archives.csv')
