#	Used to extract phishing sites from onlie-valid.xml 

import sys
import os
import xml.etree.cElementTree as ET

tree = ET.ElementTree(file='online-valid.xml')
root = tree.getroot()
elements = root[1]
for element in elements:
	url = element[0].text
	ip = element[3][0][0].text
	cidr = element[3][0][1].text
	auto_sys = element[3][0][2].text
	try:
		print url,' ',ip,' ',cidr,' ',auto_sys
	except Exception as e:
		print e
