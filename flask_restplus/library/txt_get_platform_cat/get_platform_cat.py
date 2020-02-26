from utils.db_connector.db_handler import DatabaseHandler


def getPlatformCat(platform):
	databaseHandler = DatabaseHandler()
	databaseHandler.connect()
	databaseHandler.getSessionObject()


	amazonTable = databaseHandler.getTableMetaData(databaseHandler.amazonTableName)
	ebayTable = databaseHandler.getTableMetaData(databaseHandler.ebayTableName)
	platformTable = amazonTable if platform == 'amazon' else ebayTable


	resultSet=databaseHandler.session.query(platformTable.c.RootCategory).distinct()

	categoryList = []
	for row in resultSet:
		categoryList.append(row[0])

	
	return categoryList