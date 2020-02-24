from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import urllib.parse
from bs4 import BeautifulSoup
import boto3
import helper
import os

SESSION = boto3.session.Session()
CURRENT_REGION = SESSION.region_name


TEMP_FOLDER = '/tmp'

BUCKET_NAME = 'us-west-2-google-serp'

S3_PROJECT_ROOT_KEY = 'rnd_region_google_scrape_details_mobile/{}'.format(CURRENT_REGION)
S3_HTML_PREFIX = 'page_source'
S3_RELATED_SEARCH_PREFIX = 'related_search'
S3_SERP_RESULT_PREFIX = 'serp_result'
S3_SPONSORED_RESULT_PREFIX = 'sponsored_result'

BASE_URL = 'https://www.google.com/search?q={}'


def write_page_source_to_s3(page_source_s3_key, page_source):
	s3_resource = boto3.resource("s3")
	s3_resource.Object(BUCKET_NAME, page_source_s3_key).put(Body=page_source)




def scrape_handler(event, context):
	chrome_options = Options()
	chrome_options.add_argument('--headless')
	chrome_options.add_argument('--no-sandbox')
	chrome_options.add_argument('--disable-gpu')
	chrome_options.add_argument('--window-size=1280x1696')
	chrome_options.add_argument('--user-data-dir=/tmp/user-data')
	chrome_options.add_argument('--hide-scrollbars')
	chrome_options.add_argument('--enable-logging')
	chrome_options.add_argument('--log-level=0')
	chrome_options.add_argument('--v=99')
	chrome_options.add_argument('--single-process')
	chrome_options.add_argument('--data-path=/tmp/data-path')
	chrome_options.add_argument('--ignore-certificate-errors')
	chrome_options.add_argument('--disable-dev-shm-usage')
	chrome_options.add_argument('--homedir=/tmp')
	chrome_options.add_argument('--disk-cache-dir=/tmp/cache-dir')
	chrome_options.add_argument('--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1')
	chrome_options.binary_location = os.getcwd() + "/bin/headless-chromium"

	query_list = event.get('query_list')

	driver = webdriver.Chrome(chrome_options=chrome_options)
	page_data = ""


	for query in query_list:
		q = urllib.parse.quote(query)
		search_url = BASE_URL.format(q)
		print(search_url)

		driver.get(search_url)
		page_data = driver.page_source
		soup = BeautifulSoup(page_data,'html.parser')
		query_clean_name = helper.get_query_clean_name(query)

		# For html page source
		page_source_s3_key = '{}/{}/{}.html'.format(S3_PROJECT_ROOT_KEY, S3_HTML_PREFIX, query_clean_name)
		write_page_source_to_s3(page_source_s3_key, page_data)
		
		

	driver.close()
