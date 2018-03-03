import sqlite3
import requests
import xmltodict

from property import Property
from anytree import Node, RenderTree


API_KEY = ''

address = '9239 N 63RD Dr, Glendale, AZ'
zipcode = '85302'
zpid = '7703659'

PROPERTY_URL = "https://www.zillow.com/webservice/GetSearchResults.htm?zws-id=X1-ZWz1g9kczky39n_2qbsp&address='9239 N 63RD Dr, Glendale, AZ'&citystatezip=85302"
def searchProperty():
	# Return odict_keys(['zpid', 'links', 'address', 'zestimate', 'localRealEstate'])
    response = requests.get(PROPERTY_URL)
    contentDict = xmltodict.parse(response.content)
    return contentDict['SearchResults:searchresults']['response']['results']['result']

'''
def searchComps(zpid, count):
	COMP_URL = "http://www.zillow.com/webservice/GetComps.htm?zws-id=X1-ZWz1g9kczky39n_2qbsp&zpid={}&count={}".format(zpid, count)
	response = requests.get(COMP_URL)
	contentDict = xmltodict.parse(response.content)
	parentNode = contentDict['Comps:comps']['response']['properties']['principal']
	# Comparables are a list of dictionaries
	comparables = contentDict['Comps:comps']['response']['properties']['comparables']['comp']
	for comp in comparables:
		print(comp['@score'], comp['localRealEstate'])
	return contentDict
'''
initialNode = searchProperty()
initialProperty = Property(initialNode['zpid'], initialNode['links'], initialNode['address'], initialNode['zestimate'], initialNode['localRealEstate'])

first = Node(initialProperty.zpid)

principal, comparables = initialProperty.searchComparables()

# Creating Property objects from list of comparables
levelCount = 0
# {"Tree-Height": parentNode}
NodeDict = {str(levelCount): first}
def recurseSearch(parentNode, principal, comparables, limit):
	''' Recursively creates a network of comparable real estate.
		Height of the tree = limit. Number of leaf nodes = 5 ** (limit - 1)'''
	print("Height Level: {}".format(limit))
	if limit == 1:
		return True
	for comp in comparables:
		compObj = Property(comp['zpid'], comp['links'], comp['address'], comp['zestimate'], comp['localRealEstate'], 
						principal=principal)
		tempParent = Node(compObj.zpid, parent=parentNode)
		tempPrinciple, tempComparables = compObj.searchComparables()
		recurseSearch(tempParent, tempPrinciple, tempComparables, limit-1)


recurseSearch(first, principal, comparables, 4)

print(RenderTree(first))

