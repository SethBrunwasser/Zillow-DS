import requests
import xmltodict

class Property(object):
	"""docstring for Property"""
	def __init__(self, zpid, links, address, zestimate, localRealEstate, principal=None, comparables=None):
		super(Property, self).__init__()
		self.zpid = zpid
		self.links = links
		self.address = address
		self.zestimate = zestimate
		self.localRealEstate = localRealEstate
		self.principal = principal
		self.comparables = comparables


	def getComparables(self):
		# Return List[Property]
		return self.comparables

	def setComparables(self, comparables):
		self.comparables = comparables

	def searchComparables(self, count=5):
		# Return (Dict, List[Dict])
		COMP_URL = "http://www.zillow.com/webservice/GetComps.htm?zws-id=X1-ZWz1g9kczky39n_2qbsp&zpid={}&count={}".format(self.zpid, count)
		response = requests.get(COMP_URL)
		contentDict = xmltodict.parse(response.content)
		principal = contentDict['Comps:comps']['response']['properties']['principal']
		comparables = contentDict['Comps:comps']['response']['properties']['comparables']['comp']
		self.setComparables(comparables)
		return principal, comparables

	
		