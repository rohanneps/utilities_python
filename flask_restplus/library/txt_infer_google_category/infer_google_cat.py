from library.txt_striphtml.html_stripper import getStrippedHtml,getSourceCode
from utils.db_connector.db_handler import DatabaseHandler
from utils.helpers.get_unique_key_val_pair import getUniqueListOfKeyValue
import pandas as pd


def inferGoogleCategoryFromHtml(distinctCatSubCatList,strippedHtmlContent):
	googeCatSubCatInfered = {}
	for catSubCatPair in distinctCatSubCatList:
		cat = catSubCatPair.split('|')[0].strip()
		subCat = catSubCatPair.split('|')[1].strip()
		if ' '+subCat.lower()+' ' in strippedHtmlContent:
		# if subCat.lower() in strippedHtmlContent:
			googeCatSubCatInfered[cat] = '{}||{}'.format(googeCatSubCatInfered.get(cat,' '),subCat)

	return getUniqueListOfKeyValue(googeCatSubCatInfered)

def inferGoogleCategoryFromUrl(url):
	response = getSourceCode(url)
	strippedHtmlContent = getStrippedHtml(response.content)

	#Initializing database
	databaseHandler = DatabaseHandler()
	databaseHandler.connect()
	databaseHandler.getSessionObject()

	googleresultJson = {}
	googleTable = databaseHandler.getTableMetaData(databaseHandler.googleTableName)
	googleCatTableStmt = databaseHandler.session.query(googleTable).statement

	googleDF = pd.read_sql(googleCatTableStmt,databaseHandler.session.bind)
	googleDF.columns = ['id','Category','SubCategory']
	googleDF = googleDF[(googleDF.SubCategory.notnull()) & (googleDF.SubCategory!='')]
	googleDF['Cat-SubCat'] = googleDF['Category'].str.strip()+'|'+googleDF['SubCategory'].str.strip()
	distinctCatSubCatList = googleDF['Cat-SubCat'].unique().tolist()
	distinctCatSubCatList = list(filter(lambda x:type(x)!=float,distinctCatSubCatList))
	inferedJson = inferGoogleCategoryFromHtml(distinctCatSubCatList,strippedHtmlContent)
	inferedJson ['status_code'] =response.status_code
	return inferedJson


