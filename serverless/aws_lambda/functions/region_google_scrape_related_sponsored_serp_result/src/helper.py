from datetime import datetime
import re

def get_cleaned_name(value):
	return re.sub('[^A-Za-z0-9_]', '_', value)


def get_current_date_time_stamp():
	now = datetime.now()
	return now.strftime("%d_%m_%Y__%H_%M_%S")


def get_query_clean_name(query):
	return get_cleaned_name('{}__{}'.format(query, get_current_date_time_stamp()))
