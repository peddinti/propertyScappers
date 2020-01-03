import datetime
import sys
import urllib
import urllib2
import xml.dom.minidom
import re
import HTMLParser
from bs4 import BeautifulSoup
import requests
############################################################################################################################################
######################################################## Global Variables ##################################################################
############################################################################################################################################
Location = 'Hyderabad'
Types = ['RESIDENTIAL', 'COMMERCIAL']
OverviewTrendsUrl = 'https://www.magicbricks.com/Property-Rates-Trends/ALL-{0}-rates-in-{1}'
AjaxDataUrl = 'https://www.magicbricks.com/bricks/dwr/call/plaincall/ajaxService.getPropertyRates.dwr'
Headers = {
    'authority': 'www.magicbricks.com',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    'sec-fetch-user': '?1',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'referer': 'https://www.magicbricks.com/Property-Rates-Trends/ALL-COMMERCIAL-rates-in-Hyderabad',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9,fr-FR;q=0.8,fr;q=0.7',
    'cookie': 'AlteonP-MB=BO8eGYCPEme6ikdWF9s8DQ$$; JSESSIONID=5DC4F218F1AFE8A94C4262F5CFEE066B-n1.MBAPP-178; _ga=GA1.2.1821810557.1577115480; _gid=GA1.2.1539445425.1577115480; userNTrackId=3f5053f4-9297-4499-8b2e-a0225eff971f; _fbp=fb.1.1577115481387.644145408',
}

############################################################################################################################################
######################################################## Method Functions ##################################################################
############################################################################################################################################
def getOverviewTends(location, type):
	url = OverviewTrendsUrl.format(type, location)
	try:
		response = webdriver.Firefox().get(url, headers=Headers)
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return response.content
    except urllib2.URLError:
        
    return None

def parseOverviewTendsPage(pageContent, location, type):
	htmlDoc = BeautifulSoup(pageContent)


def getMetricData(typeId):
	headers = Headers
	headers['sec-fetch-mode'] = 'cors'
    data = {
    	"callCount": 1,
    	"httpSessionId": "F6AEABBF9B52334CFB6B882F77E3973C-n1.MBAPP-176",
    	"scriptSessionId": "1F47710CD4AE2F5DB09361C487D16BBD459",
    	"c0-scriptName": "ajaxService",
    	"c0-methodName": "getPropertyRates",
    	"c0-id": "0",
		"c0-param0": "string:2060",
		"c0-param1": "string:{0}".format(typeId),
		"c0-param2": "string:",
		"c0-param3": "string:",
		"c0-param4": "number:1",
		"c0-param5": "number:9000",
		"c0-param6": "boolean:false",
		"c0-param7": "boolean:false",
		"batchId": "2",
    }
	response = requests.post(AjaxDataUrl, headers=headers, data=data)
