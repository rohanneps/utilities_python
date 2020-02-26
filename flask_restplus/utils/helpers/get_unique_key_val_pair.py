
def getUniqueListOfKeyValue(resultJson):
	updateResultDict = {}
	for key,value in resultJson.items():
		valueList = list(set(list(filter(lambda val: val!=' ', value.split('||')))))
		valueList.sort()
		updateResultDict[key] = valueList
	return updateResultDict


def getCatAttrFreq(catAttrJson):
	catAttrFreqJson = {}
	for catKey in catAttrJson:
		#attrValPair is list
		attrList=[]
		tempList = list(map(lambda x:x.split('|')[0],catAttrJson[catKey]))
		from collections import Counter
		cnt = Counter(tempList)
		# getting attribute having more than 1 occrance
		attrList = [item for item, itemCount in cnt.items() if itemCount > 1]
		if len(attrList)==0:
			catAttrFreqJson[catKey] = tempList
		else:
			catAttrFreqJson[catKey] = attrList
	return catAttrFreqJson
