from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from utils.dbconfig.db_variables import *
from urllib.parse import quote_plus as urlquote

class DatabaseHandler():

	def __init__(self):
		self.database_type = database_type
		self.dbname = database
		self.username = username
		self.password = password
		self.host = host

		self.amazonTableName = 'amazon_file_with_cat'
		self.ebayTableName = 'ebay_file_with_cat'
		self.googleTableName = 'google_cat'

	def connect(self):
		create_engine_string = '{}://{}:{}@{}/{}'.format(self.database_type,self.username,urlquote(self.password),self.host,self.dbname)
		self.engine = create_engine(create_engine_string)

	def getSessionObject(self):
		Session = sessionmaker(bind=self.engine)
		self.session = Session()

	def getTableMetaData(self, tableName):
		metadata = MetaData(self.engine, reflect=True)
		tableMetaData = metadata.tables[tableName]
		return tableMetaData

