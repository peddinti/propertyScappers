import datetime
import sys
import urllib
import urllib2
import xml.dom.minidom
import re
import HTMLParser
from bs4 import BeautifulSoup
import requests
import itertools
import csv
############################################################################################################################################
######################################################## Global Variables ##################################################################
############################################################################################################################################
Location = 'hyderabad'
OverviewTrendsUrl = 'https://www.99acres.com/property-rates-and-price-trends-in-{0}'
OverviewAjaxUrl = 'https://www.99acres.com/do/pricetrendsResearch/viewTrendsTable/{0}/locality/{1}/0/0'

Headers = {
    'authority': 'www.99acres.com',
    'content-length': '0',
    'accept': '*/*',
    'origin': 'https://www.99acres.com',
    'x-requested-with': 'XMLHttpRequest',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'referer': 'https://www.99acres.com/property-rates-and-price-trends-in-hyderabad',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9,fr-FR;q=0.8,fr;q=0.7',
    'cookie': '99_ab=67; 99_FP_VISITOR_OFFSET=25; GOOGLE_SEARCH_ID=763711530790051206; PROP_SOURCE=IP; 99_suggestor=1; 99_trackIP=IN; 99NRI=1; __utmc=267917265; RES_COM=RES; src_city=0; 99_citypage=0; 99_city=; kwp_last_action_id_type=0%2CHP_R%2C763711530790051206; _ga=GA1.2.1645051437.1577115309; _gid=GA1.2.1992918508.1577115316; _ss_v=LxRrBSd3LjIITw/m; _fbp=fb.1.1577115318082.1129814149; _sess_id=EF0DHnhsOriggx27yFYPjOGTjkMSpsy95isLEvdrsl51DwcNzFy%2BwtSFTK9ibOis7PpGEGpjZC0RUQuyhJqCCQ%3D%3D; __utma=267917265.1645051437.1577115309.1577115309.1577161458.2; __utmz=267917265.1577161458.2.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmt=1; __utid=5; ak_bmsc=77FE51D880BFF6BAEB2C42E9B3B7A5CCB81A369F5F460000F192015EB02B9E20~plMjFkjPnpqo+RCkek8zj0foPMPzszRe40pG3PDFDrNN3aLXhdbiwpy0RJh6nx7nv4n6eaarP6Ud11iMaL+wLtb+v3e4+4q42c7s5tblcPmhixilDEjpsvEpd/tCdMMlPVjzGbeNaJxdFjNF4LsIVy1udPAMxydjmiG3TEcZtN5fTQqg70TH4wp6lzZVVVtVMxRbaYWFFRmL0koRbBNfnIj0jA9M5aUyxuZj2X2FYGs1a8gyh20RabhlOmFhJMKVP6; session_source=https://www.99acres.com/property-rates-and-price-trends-in-hyderabad; __utmb=267917265.4.10.1577161458; bm_sv=A1B1D96F8C3523D4FD14D0C1FCFAFD89~q+6whNFswtbWqyKH9FzoanDZVD+Q3tTumtm2gEzN7Px+zui5q63j4O7PqRA5VeuZENlIJEfgGbGGDZgXP6fphSmkQnbsgQu7RaeA6QwyxUd6J8NlQR1FPyLp8cyGDmT3XyLlgPQgGn23+mVLOW0RZRW+AR6CkrQQOcuMBLgDz7c=',
}

TypeMapping = {
    1: 'Residential Apartment',
    3: 'Residential Land',
    4: 'Independent/Builder Floor'
}

LocationMapping = {
    269: 'hyderabad',
}

ColNames = ['location', 'sqft price range', 'QoQ', 'trendsUrl', '1B', '2B', '3B']

############################################################################################################################################
######################################################## Method Functions ##################################################################
############################################################################################################################################
def getOverviewTends(location, type):
    url = OverviewAjaxUrl.format(location, type)
    try:
        response = requests.post(url, headers=Headers)
        if response.status_code == 200:
            return response.content
    except urllib2.URLError:
        return None

def parseOverviewTendsPage(pageContent, location, type):
    htmlDoc = BeautifulSoup(pageContent)
    rows = htmlDoc.find('tbody').find_all('tr')
    results = []
    for row in rows:
        cols = row.find_all('td')
        if len(cols) == 0:
            next
        result = dict(zip(ColNames, [x.text.strip() for x in cols]))
        result['region'] = LocationMapping[location]
        result['type'] = TypeMapping[type]
        results.append(result)
    return results

def getAllLocationTrends(location):
    results = []
    for type in TypeMapping.keys():
        results.append(parseOverviewTendsPage(getOverviewTends(location, type), location, type))
    return list(itertools.chain(*results))

try:
    with open("99Acres.csv", 'w') as csvfile:
        colHeades = ColNames.extend(["region", "type"])
        data = getAllLocationTrends(269)
        writer = csv.DictWriter(csvfile, fieldnames=ColNames, delimiter="\t")
        writer.writeheader()
        for row in data:
            writer.writerow(row)
except IOError:
    print("I/O error")