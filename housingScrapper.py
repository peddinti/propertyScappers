import requests
import json
import csv
import time
############################################################################################################################################
######################################################## Global Variables ##################################################################
############################################################################################################################################
Cookie = 'traffic=sourcemedium%3Ddirect%20%2F%20none%3B; uuid=id%3D2b90a931aa148541d3fbd1e59a652535%3B; userCity=1cdd81323d5286e9fa47; category=residential; _ga=GA1.2.1251477610.1577342613; _gid=GA1.2.538114294.1577342613; tvc_sm_fc_new=direct%7Cnone; tvc_sm_lc=direct%7Cnone; cuid=45945569-6878-4e0a-aba3-a6073e4b9d4e; experiments=hj%3Dtrue%3Bsrp_gallery%3Dtrue%3Bfilter_card_mobile_serp%3Dtrue%3Bis_phoenix_enabled%3Dbuy_dedicated_10%3Bmf_weightage_sort_experiment%3Dmf_original%3Bshow_crf_drop_off_research_popup%3Dtrue%3Bremove_titanium_mobile%3Dfalse%3Bcrf_v3%3Dtrue%3Bremove_70_30_experiment%3Dfalse%3Brent_card_revamp%3Dtrue%3Bfilter_api_version%3Dv6%3Bavoid_filter_blind_spot%3Dtrue%3BlistedByFilterBoost%3Dtrue%3Bserp_por_cta%3DGet%20Best%20Price%3Bpaid_filter_price_range%3D20%3Bctr_relevance_experiment%3Dfalse%3Bapp_download_hook%3D1%3Btest_experiment%3Dfalse%3Bapp_download_hook_1%3Dtrue%3Bproject_card_type%3Dproject%3Bpaid_feed_srp%3Dtrue%3Bdiversity_listing_experiment%3Dtrue%3Bgallery_img_version%3Dtrue%3B; _uuid=fb1a0c00e3cf0c04552b0249975c617e; origin=5; is_return_user=true; is_return_session=true; service=rent; cookie_consent=not-req; _udata_=time%3D1577342621668%3B; experiments=makaan_propcard_click%253Dfalse%253Bmakaan_mpsticky_pos%253Dtop%253Bmakaan_quick_filters%253Denabled%253Bmakaan_mob_prop_open%253Dsame_tab%253Bmakaan_mpmatching%253Ddisabled%253Bmakaan_mp_onboarding%253Dtext%253Bmakaan_serpVersion%253D1%253Bmakaan_lf_config_position%253Dabove%253Bmakaan_serp_new%253Dfalse%253B'
ApiUrl = 'https://housing.com/zeus/api/gql'
Headers = {
    'authority': 'housing.com',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'accept-language': 'en-US,en;q=0.9,fr-FR;q=0.8,fr;q=0.7',
    'cookie': Cookie,
}
ColumnHeaders = ["id", "name", "avgRate", "overallScore", "Property Distribution/BY BHK TYPE/1 BHK", "Property Distribution/BY BHK TYPE/1 RK", "Property Distribution/BY BHK TYPE/2 BHK", "Property Distribution/BY BHK TYPE/3 BHK", 
"Property Distribution/BY BHK TYPE/3+ BHK", "Property Distribution/BY PROPERTY TYPE/Villa", "Property Distribution/BY LEASE TYPE/Bachelor", "Property Distribution/BY LEASE TYPE/Company", "Property Distribution/BY LEASE TYPE/Family", 
"Property Distribution/BY PROPERTY TYPE/Apartment", "Property Distribution/BY PROPERTY TYPE/Independent Floor", "Property Distribution/BY PROPERTY TYPE/Independent House", 
"Score/Amenity", "Score/Commute", "Score/Lifestyle", "Score/Popularity", "Score/Value For Money", "User Preferences/BY BHK TYPE/1 BHK", "User Preferences/BY BHK TYPE/1 RK", 
"User Preferences/BY BHK TYPE/2 BHK", "User Preferences/BY BHK TYPE/3 BHK", "User Preferences/BY BHK TYPE/3+ BHK", 'Price_1 BHK_Number of Properties', 'Price_3 BHK_Max Price', 'Price_1 RK_Min Price', 'Price_1 RK_Max Price', 'Price_2 BHK_Max Price', 
'Price_1 RK_Number of Properties', 'Price_3 BHK_Min Price', 'Price_1 BHK_Min Price', 'Price_1 BHK_Max Price', 'Price_3 BHK_Number of Properties', 'Price_2 BHK_Min Price', 'Price_2 BHK_Number of Properties', 'Price_3+ BHK_Number of Properties', 'Price_3+ BHK_Min Price', 'Price_3+ BHK_Max Price']

############################################################################################################################################
######################################################## Global Variables ##################################################################
############################################################################################################################################
class AutoSuggest:
    @staticmethod
    def getSearchParams(locationName):
        searchQuery = dict((
            ('name', locationName),
            ('service', 'rent'),
            ('category', 'residential'),
            ('city', dict((
                ('name', 'Hyderabad'),
                ('id', '1cdd81323d5286e9fa47'),
                ('url', 'hyderabad'),
            ))),
            ('excludeEntities', [])
        ))
        paramVariables = dict((
            ('searchQuery', searchQuery),
            ('variant', 'moondragon'),

        ))
        params = (
            ('isBot', 'false'),
            ('query', '\n  query($searchQuery: SearchQueryInput!, $variant:String){\n    typeAhead(searchQuery: $searchQuery, variant:$variant) {\n      results {\n        id\n        name\n        displayType\n        type\n        subType\n        url\n        center\n      }\n      defaultUrl\n      isCrossCitySearch\n    }\n  }\n'),
            ('source', 'web'),
            ('variables', json.dumps(paramVariables)),
        )
        return params

    @staticmethod
    def locationSearch(locationName):
        searchParams = AutoSuggest.getSearchParams(locationName)
        print("Searching for location {0}".format(locationName))
        try:
            response = requests.get(ApiUrl, headers=Headers, params=searchParams)
            if response.status_code == 200:
                result = json.loads(response.content)
                return result['data']['typeAhead']['results']
        except requests.exceptions.RequestException:
            print("Eror Searching for location {0}".format(locationName))
            return None
        return None

class LocationDetails:
    @staticmethod
    def getSearchParams(service, localityInfo):
        locality = dict((
            ('id', localityInfo['id']),
            ('name', localityInfo['name']),
            ('type', localityInfo['type']),
            ('subType', localityInfo['subType']),
            ('displayType', localityInfo['displayType']),
        ))
        paramVariables = dict((
            ('service', service),
            ('locality', locality),
        ))
        params = (
            ('isBot', 'false'),
            ('query', '\n  query($service: String!, $locality: RealEstateEntityInput!) {\n    localityInfo(service: $service, locality: $locality) {\n     entity {\n       id\n       name\n       image\n       }\n     avgRate {\n      value\n      displayValue\n     } \n     overallScore\n     scoreComponents {\n      label\n      description\n      value\n     }\n     distributionData {\n      title\n      subTitle\n      tabs{\n       title\n       data\n      }\n      chart\n     }\n    }\n  }\n'),
            ('source', 'web'),
            ('variables', json.dumps(paramVariables)),
        )
        return params

    @staticmethod
    def formatLocalityInfo(locality, localityInfo):
        if localityInfo['scoreComponents']:
            scoreComponents = dict([("Score/" + x['label'], x['value']) for x in localityInfo['scoreComponents']])
        else:
            scoreComponents = {}
        distributionData = {}
        for dd in localityInfo['distributionData']:
            for tab in dd['tabs']:
                data = tab['data']
                if dd['title'] == 'Pricing By BHK':
                    cols = data[0]
                    distributionData.update(dict([("Price_" + point[0]+"_"+x[0], x[1]) for point in data[1:] for x in (zip(cols, point)[1:])]))
                else:
                    data = filter(lambda x: type(x[0]) == dict, data)
                    distributionData.update(dict([(dd['title'] + "/" + tab['title'] + "/" + x[0]['label'], x[1]) for x in data]))

        result =  {
            'avgRate': localityInfo['avgRate']['value'],
            'overallScore': localityInfo['overallScore'],
            'id': localityInfo['entity']['id'],
            'name': locality['name'],
        }
        result.update(scoreComponents)
        result.update(distributionData)
        return result

    @staticmethod
    def locationRentInfo(locality):
        searchParams = LocationDetails.getSearchParams('rent', locality)
        print("Fetching locationInfo for {0}".format(locality['name']))
        try:
            response = requests.get(ApiUrl, headers=Headers, params=searchParams)
            if response.status_code == 200:
                result = json.loads(response.content)
                return LocationDetails.formatLocalityInfo(locality, result['data']['localityInfo'])
        except requests.exceptions.RequestException:
            print("Got error fetching locationInfo for {0}".format(locality['name']))
            return None

        return None

def fetchLocationData(locations):
    localityInfos = []
    for location in locations:
        time.sleep(1)
        try:
            localities = AutoSuggest.locationSearch(location)
            if localities != None:
                localityInfos += [LocationDetails.locationRentInfo(localities[0])]
        except:
            print("Error fetching data for location: {0}".format(location))
    return localityInfos

if __name__ == '__main__':
    hyderabad_localities = [line.rstrip('\n') for line in open("hyderabad_localities.txt")]
    localityInfos = fetchLocationData(hyderabad_localities)

    try:
        with open("hyderabad_housing_data.csv", 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=ColumnHeaders, delimiter="\t")
            writer.writeheader()
            for row in localityInfos:
                writer.writerow(row)
    except IOError:
        print("I/O error")

