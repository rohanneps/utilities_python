from datetime import datetime
import re

def get_cleaned_name(value):
	# return re.sub('[^A-Za-z0-9_]', '_', value)
	return value.replace('/','__')


def get_current_date_time_stamp():
	now = datetime.now()
	return now.strftime("%d_%m_%Y__%H_%M_%S")


def get_query_clean_name(query):
	return '{}--{}'.format(get_cleaned_name(query), get_current_date_time_stamp())
