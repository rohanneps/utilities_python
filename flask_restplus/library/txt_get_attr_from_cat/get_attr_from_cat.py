from utils.db_connector.db_handler import DatabaseHandler
from utils.helpers.get_unique_key_val_pair import getUniqueListOfKeyValue


def getAttrFromRootCat(category):
	databaseHandler = DatabaseHandler()
	databaseHandler.connect()
	databaseHandler.getSessionObject()

	amazonresultJson = {}
	amazonTable = databaseHandler.getTableMetaData(databaseHandler.amazonTableName)
	amazonResultSet=databaseHandler.session.query(amazonTable).filter(amazonTable.c.RootCategory.ilike('%{}%'.format(category)))
	for row in amazonResultSet:
		amazonresultJson[row.RootCategory] = '{}||{}'.format(amazonresultJson.get(row.RootCategory,' '),row.AttributeName)
	amazonresultJson = getUniqueListOfKeyValue(amazonresultJson)

	ebayresultJson = {}
	ebayTable = databaseHandler.getTableMetaData(databaseHandler.ebayTableName)
	ebayResultSet=databaseHandler.session.query(ebayTable).filter(ebayTable.c.RootCategory.ilike('%{}%'.format(category)))
	for row in ebayResultSet:
		ebayresultJson[row.RootCategory] = '{}||{}'.format(ebayresultJson.get(row.RootCategory,' '),row.AttributeName)
	ebayresultJson = getUniqueListOfKeyValue(ebayresultJson)

	attributeValueJson = {
	'Amazon': amazonresultJson,
	'Ebay': ebayresultJson
	}
	return attributeValueJson
