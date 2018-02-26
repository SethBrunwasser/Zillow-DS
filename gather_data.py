from pyzillow.pyzillow import ZillowWrapper, GetDeepSearchResults, GetUpdatedPropertyDetails
import sqlite3
import urllib
import requests
import xmltodict
import json


API_KEY = 'X1-ZWz1g9kczky39n_2qbsp'

address = '9239 N 63RD Dr, Glendale, AZ'
zipcode = '85302'
'''zillow_data = ZillowWrapper('X1-ZWz1g9kczky39n_2qbsp')
deep_search_response = zillow_data.get_deep_search_results(address, zipcode)
zillow_id = GetDeepSearchResults(deep_search_response)
print(zillow_id)
updated_property_details_response = zillow_data.get_updated_property_details(zillow_id)
result = GetUpdatedPropertyDetails(updated_property_details_response) 

print(result)
'''
PROPERTY_URL = "https://www.zillow.com/webservice/GetSearchResults.htm?zws-id=X1-ZWz1g9kczky39n_2qbsp&address='9239 N 63RD Dr, Glendale, AZ'&citystatezip=85302"
def searchProperty():
    response = requests.get(PROPERTY_URL)
    contentDict = xmltodict.parse(response.content)
    print(contentDict['SearchResults:searchresults']['response']['results']['result'].keys())
    return contentDict['SearchResults:searchresults']['response']['results']['result']

def searchComps(zpid, count):
	COMP_URL = "http://www.zillow.com/webservice/GetComps.htm?zws-id=X1-ZWz1g9kczky39n_2qbsp&zpid={}&count={}".format(zpid, count)
	response = requests.get(COMP_URL)
	contentDict = xmltodict.parse(response.content)
	print(json.dumps(contentDict['Comps:comps']['response']['properties'], indent=4, sort_keys=True))
	return contentDict

initialProperty = searchProperty()
initial_zpid = initialProperty['zpid']
print(initial_zpid)
searchComps(initial_zpid, 5)


