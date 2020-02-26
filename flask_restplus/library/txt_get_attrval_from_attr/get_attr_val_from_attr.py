from utils.db_connector.db_handler import DatabaseHandler
from utils.helpers.get_unique_key_val_pair import getUniqueListOfKeyValue


def getAttrValueFromAttr(attribute):
	databaseHandler = DatabaseHandler()
	databaseHandler.connect()
	databaseHandler.getSessionObject()
	
	attributeValueJson = {}
	# querying Amazon Table
	
	amazonresultJson = {}

	amazonTable = databaseHandler.getTableMetaData(databaseHandler.amazonTableName)
	amazonResultSet=databaseHandler.session.query(amazonTable).filter(amazonTable.c.AttributeName.ilike('%{}%'.format(attribute)))
	for row in amazonResultSet:
		amazonresultJson[row.AttributeName] = '{}||{}'.format(amazonresultJson.get(row.AttributeName,' '),row.AttributeValue)
	amazonresultJson = getUniqueListOfKeyValue(amazonresultJson)

	# querying Ebay Table
	
	ebayresultJson = {}

	ebayTable = databaseHandler.getTableMetaData(databaseHandler.ebayTableName)
	ebayResultSet=databaseHandler.session.query(ebayTable).filter(ebayTable.c.AttributeName.ilike('%{}%'.format(attribute)))
	for row in ebayResultSet:
		ebayresultJson[row.AttributeName] = '{}||{}'.format(ebayresultJson.get(row.AttributeName,' '),row.AttributeValue)
	ebayresultJson = getUniqueListOfKeyValue(ebayresultJson)

	attributeValueJson = {
	'Amazon': amazonresultJson,
	'Ebay': ebayresultJson
	}
	return attributeValueJson