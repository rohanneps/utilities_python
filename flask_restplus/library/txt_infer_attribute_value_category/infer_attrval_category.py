# from utils.db_connector.db_handler import DatabaseHandler
from utils.helpers.get_unique_key_val_pair import getUniqueListOfKeyValue,getCatAttrFreq
import pandas as pd
import re,os
import datetime
from utils.global_variables import PATTERNINFEREDCATATTRVAL,DOWNLOADFOLDER,PATTERNFOLDER
from utils.db_initializer.initialize_db import amazonPlatformDF, ebayPlatformDF

from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

stemmer = PorterStemmer()

def inferPlatformAttrValCategoryFromText(distinctCatAttrAttrVal,searchText):
	platformCatInfered = {}
	for catAttrAttrValTrio in distinctCatAttrAttrVal:
		cat = catAttrAttrValTrio.split('|||')[0].strip()
		attr = catAttrAttrValTrio.split('|||')[1].strip()

		# tokenized attribute value here
		attrVal = catAttrAttrValTrio.split('|||')[2].strip()

		spaceCount = searchText.count(' ')

		# # not using stem
		# if (spaceCount<2) :
		# 	if (attrVal.lower() in searchText) and (len(attrVal)>2) and ((attr.lower() in searchText) or  (attr.lower().replace(' ','') in searchText)):
		# 	# if subCat.lower() in searchText:
		# 		attrValPair = attr+'|'+attrVal
		# 		platformCatInfered[cat] = '{}||{}'.format(platformCatInfered.get(cat,' '),attrValPair)
		# else:
		# 	if (' '+attrVal.lower()+' ' in searchText) and ((attr.lower() in searchText) or  (attr.lower().replace(' ','') in searchText)):
		# 	# if subCat.lower() in searchText:
		# 		attrValPair = attr+'|'+attrVal
		# 		platformCatInfered[cat] = '{}||{}'.format(platformCatInfered.get(cat,' '),attrValPair)

		# using stem
		
		tokenizedSearchText = word_tokenize(searchText)  # list of words in the text

		stemmedTokenizedSearchTextList = [stemmer.stem(word) for word in tokenizedSearchText]

		for stemTokenWord in stemmedTokenizedSearchTextList:
			if (stemTokenWord == attrVal.lower()) and ((attr.lower() in searchText) or (attr.lower() in stemmedTokenizedSearchTextList)):
				attrValPair = attr+'|'+attrVal
				platformCatInfered[cat] = '{}||{}'.format(platformCatInfered.get(cat,' '),attrValPair)



	return getUniqueListOfKeyValue(platformCatInfered)


# def getPlatformDBFile(platform):
# 	#Initializing database
# 	databaseHandler = DatabaseHandler()
# 	databaseHandler.connect()
# 	databaseHandler.getSessionObject()

# 	platformresultJson = {}

# 	tableName = databaseHandler.amazonTableName if platform=='amazon' else databaseHandler.ebayTableName

# 	platformTable = databaseHandler.getTableMetaData(tableName)
# 	platformCatTableStmt = databaseHandler.session.query(platformTable.c.RootCategory,platformTable.c.AttributeName,platformTable.c.AttributeValue).distinct().statement

# 	platformDF = pd.read_sql(platformCatTableStmt,databaseHandler.session.bind)
# 	return platformDF

def getPlatformDBFile(platform):
	if platform=='amazon':
		return amazonPlatformDF
	else:
		return ebayPlatformDF

def inferAttrValCategoryFromText(text,platform):
	text = text.lower()
	platformDF = getPlatformDBFile(platform)
	# platformDF = platformDF[['RootCategory', 'StemCategory', 'LeafCategory','AttributeName','AttributeValue']]
	platformDF = platformDF[['RootCategory', 'AttributeName','AttributeValue','RootAttributeValue']]
	
	# dropping duplicate rows because of leaf cat
	platformDF = platformDF.drop_duplicates(subset=['RootCategory', 'AttributeName','AttributeValue','RootAttributeValue'], keep='last')

	platformDF['RootCat-Attr-AttrVal'] = platformDF['RootCategory'].str.strip()+'|||'+platformDF['AttributeName'].str.strip()+'|||'+platformDF['RootAttributeValue'].str.strip()
	distinctCatAttrAttrVal = platformDF['RootCat-Attr-AttrVal'].unique().tolist()
	distinctCatAttrAttrVal = list(filter(lambda x:type(x)!=float,distinctCatAttrAttrVal))

	inferedJson = inferPlatformAttrValCategoryFromText(distinctCatAttrAttrVal,text)
	return inferedJson



def getPattern(item):
	Numbers = re.sub(r'[0-9]', r'9', item)
	Lowercase = re.sub(r'[a-z]', r'x', Numbers)
	UpperCase = re.sub(r'[A-Z]', r'x', Lowercase)
	# UpperCase = re.sub(r'[A-Z]', r'X', Lowercase)
	Symbols=re.sub('[^9xX ]', '#', UpperCase)
	#Spaces = re.sub('[9xX ]'+' '+'[9xX ]', '[9xX ]'+'_'+'[9xX ]', Symbols)
	Spaces = re.sub(' ',  '_' , Symbols)
	return Spaces


def inferAttrValCatPattern(platform,filename,key,val,category):
	try:
		sourceDF = pd.read_csv(filename, encoding='UTF-8')
	except Exception as e:
		return {'error_msg': 'File not found.'}
		
	sourceDF = sourceDF[[key,val]]
	sourceDF = sourceDF[sourceDF[val].notnull()]
	sourceDF['ValPattern'] = sourceDF[val].apply(getPattern)

	sourceDF = sourceDF.iloc[0:2]
	platformDF = getPlatformDBFile(platform)
	platformDF = platformDF[['RootCategory','AttributeName','AttributeValue']]
	platformDF = platformDF.drop_duplicates(subset=['RootCategory', 'AttributeName','AttributeValue'], keep='last')
	platformDF = platformDF[platformDF['RootCategory'].str.contains(category,flags=re.IGNORECASE)]
	platformDF['ValPattern'] = platformDF['AttributeValue'].apply(getPattern)

	inferedDF = pd.DataFrame(columns=[key,'Category','Attribute','AttributeValue','Pattern'])
	
	def searchPattern(row):
		nonlocal inferedDF,key,platformDF
		keyID = row[key]
		valPattern = row['ValPattern']
		for index, row in platformDF.iterrows():
			if row['ValPattern'] in valPattern:
				inferedDF = inferedDF.append(pd.Series([keyID,row['RootCategory'],row['AttributeName'],row['AttributeValue'],row['ValPattern']],index=inferedDF.columns.tolist()),ignore_index=True)


	# sourceDF.apply(searchPattern,axis=1,args=[key,platformDF])
	sourceDF.apply(searchPattern,axis=1)


	inferedDF['PattLen'] = inferedDF['Pattern'].apply(len)
	inferedDF = inferedDF.sort_values([key,'Attribute','PattLen'],ascending = [True,True,False])
	del inferedDF['PattLen']

	# getting current date, time
	now = datetime.datetime.now()
	currentDateTime = '{}{}{}{}{}{}'.format(now.year,now.month,now.day,now.hour,now.minute,now.second)

	outputFileName = '{}_{}.csv'.format(PATTERNINFEREDCATATTRVAL,currentDateTime)
	
	outputFullPath = os.path.join(DOWNLOADFOLDER,PATTERNFOLDER,outputFileName)
	inferedDF = inferedDF.drop_duplicates(keep='last')
	inferedDF.to_csv(outputFullPath,index=False)
	return {'OutputFileName':outputFullPath}