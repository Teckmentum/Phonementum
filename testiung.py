




import re
newLicence = r'11|ZGRUMSERVER2016\\Phrases:license'
delimiter = r'<QLLicenseDatabase>.*</SQLLicenseDatabase>'
result = r"""<QLLicenseDatabase>11|ZGRUMSERVER2016\Phrases:license</SQLLicenseDatabase>
"""

p = re.compile(delimiter)
result = p.sub('<QLLicenseDatabase>' + newLicence + '</SQLLicenseDatabase>', result)
print(result)




"""
import urllib.request
import xml.etree.ElementTree as Et
import xmltodict
result = urllib.request.urlopen("http://api.geonames.org/findNearbyPostalCodes?postalcode=00988&radius=10&username=teckmentum&maxRows=20").read()

tree = Et.fromstring(result)

xmldic = xmltodict.parse(result)

for child in xmldic['geonames']['code']:
    print(child['postalcode'])

"""
