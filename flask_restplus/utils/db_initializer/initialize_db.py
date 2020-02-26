from utils.db_connector.db_handler import DatabaseHandler
import pandas as pd

from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
stemmer=PorterStemmer()



databaseHandler = DatabaseHandler()
databaseHandler.connect()
databaseHandler.getSessionObject()

platformresultJson = {}


# For Amazon
amazonTable = databaseHandler.amazonTableName
amazonTableMeta = databaseHandler.getTableMetaData(amazonTable)
amazonPlatformTableStmt = databaseHandler.session.query(amazonTableMeta.c.RootCategory,amazonTableMeta.c.AttributeName,amazonTableMeta.c.AttributeValue).distinct().statement
amazonPlatformDF = pd.read_sql(amazonPlatformTableStmt,databaseHandler.session.bind)
# extracting root of each attribute value
amazonPlatformDF['RootAttributeValue'] = amazonPlatformDF['AttributeValue'].apply(lambda attrval:stemmer.stem(attrval))


# For Ebay
ebayTable = databaseHandler.ebayTableName
ebayTableMeta = databaseHandler.getTableMetaData(ebayTable)
ebayPlatformTableStmt = databaseHandler.session.query(ebayTableMeta.c.RootCategory,ebayTableMeta.c.AttributeName,ebayTableMeta.c.AttributeValue).distinct().statement
ebayPlatformDF = pd.read_sql(ebayPlatformTableStmt,databaseHandler.session.bind)
# extracting root of each attribute value
ebayPlatformDF['RootAttributeValue'] = ebayPlatformDF['AttributeValue'].apply(lambda attrval:stemmer.stem(attrval))



