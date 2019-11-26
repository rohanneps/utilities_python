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
BUCKET_NAME = 'gbd-daf-dump'
S3_PROJECT_ROOT_KEY = 'rnd_region_google_scrape_details/{}'.format(CURRENT_REGION)
S3_HTML_PREFIX = 'page_source'
S3_RELATED_SEARCH_PREFIX = 'related_search'
S3_SERP_RESULT_PREFIX = 'serp_result'
S3_SPONSORED_RESULT_PREFIX = 'sponsored_result'

BASE_URL = 'https://www.google.com/search?q={}'


def write_page_source_to_s3(page_source_s3_key, page_source):
	s3_resource = boto3.resource("s3")
	s3_resource.Object(BUCKET_NAME, page_source_s3_key).put(Body=page_source)


def upload_file_to_s3(output_file_path, local_file):
	s3_resource = boto3.resource("s3")
	s3_resource.Object(BUCKET_NAME, output_file_path).upload_file(Filename=local_file)
	os.remove(local_file)


def get_related_search_details(soup, query_clean_name, related_search_s3_key):
	related_search_element = soup.find('div',{'id':'extrares'})
	if related_search_element:
		related_search_query_file = '{}_related_search.tsv'.format(query_clean_name)
		related_search_query_file_path = os.path.join(TEMP_FOLDER, related_search_query_file)
		with open(related_search_query_file_path,'w') as req_file:
			req_file.write('url'+'\t'+'related_search')
			req_file.write('\n')
			related_search_elems = related_search_element.findAll('p')
			for related_search_elem in related_search_elems:
				try:
					related_search_text = related_search_elem.text.strip()
				except:
					related_search_text = ''
				try:
					related_search_url = related_search_elem.find('a')['href']
				except:
					related_search_url = ''

				req_file.write(related_search_url+'\t'+related_search_text)
				req_file.write('\n')

		upload_file_to_s3(related_search_s3_key, related_search_query_file_path)


def get_serp_result_details(soup, query_clean_name, serp_result_s3_key):

	serp_result = soup.find('div',{'id':'rso'})
	if serp_result:
		serp_result_query_file = '{}_serp_result.tsv'.format(query_clean_name)
		serp_result_query_file_path = os.path.join(TEMP_FOLDER, serp_result_query_file)

		with open(serp_result_query_file_path,'w') as req_file:
			req_file.write('serp_url'+'\t'+'serp_text'+'\t'+'serp_breadcrumb'+'\t'+'serp_description')
			req_file.write('\n')
			serp_elem_list = serp_result.findAll('div',{'class':'rc'})

			for serp_elem in serp_elem_list:
				try:
					serp_url = serp_elem.find('a')['href']
				except:
					serp_url = ''
				try:
					serp_text = serp_elem.find('h3').text.strip()
				except:
					serp_text = ''
				try:
					serp_description = serp_elem.find('span',{'class':'st'}).text.strip()
				except:
					serp_description = ''
				try:
					serp_breadcrumb = serp_elem.find('cite').text.strip()
				except:
					serp_breadcrumb = ''
				req_file.write(serp_url+'\t'+serp_text+'\t'+serp_breadcrumb+'\t'+serp_description)
				req_file.write('\n')

		upload_file_to_s3(serp_result_s3_key, serp_result_query_file_path)

def get_sponsored_result_details(soup, query_clean_name, sponsored_result_s3_key):
	sponsored_section_tag = soup.find('div',{'class':'top-pla-group-inner'})

	if sponsored_section_tag:
		sponsored_result_query_file = '{}_sponsored_result.tsv'.format(query_clean_name)
		sponsored_result_query_file_path = os.path.join(TEMP_FOLDER, sponsored_result_query_file)
		with open(sponsored_result_query_file_path,'w') as req_file:
			req_file.write('url'+'\t'+'name'+'\t'+'price'+'\t'+'price_drop'+'\t'+'image'+'\t'+'brand'+'\t'+'rating'+'\t'+'review'+'\t'+'return_policy')
			req_file.write('\n')
			sponsored_elem_list = sponsored_section_tag.findChildren('div', recursive=False)

			for sponsored_elem in sponsored_elem_list:
				# image section:
				try:
					sponspored_elem_image = sponsored_elem.find('div',{'class':'Ter3Ue Nwl2ud'}).find('div',{'class':'Gor6zc'}).find('img')['src']
				except:
					sponspored_elem_image = ''

				# name price section

				name_price_tag = sponsored_elem.find('div',{'class':'orXoSd'})
				try:
					# sponspored_elem_name = name_price_tag.find('a',{'id':re.compile(r'vplaurlt')}).text.strip()
					sponsored_name_tag = sponsored_elem.find('span',{'class': 'pymv4e'})
					sponspored_elem_name = sponsored_name_tag.text.strip()
				except:
					sponspored_elem_name = ''
				try:
					sponspored_elem_url = sponsored_elem.find('div',{'class':'Ter3Ue Nwl2ud'}).find('a').findNext('a')['href']
				except:
					sponspored_elem_url = ''

				try:
					sponspored_elem_price = name_price_tag.find('div',{'class': 'e10twf T4OwTb'}).text.strip()
				except:
					sponspored_elem_price = ''

				try:
					sponspored_elem_price_drop = name_price_tag.find('div',{'class': 'wEE4ud'}).text.strip()
				except:
					sponspored_elem_price_drop = ''

				try:
					sponspored_elem_brand = name_price_tag.find('div',{'class': 'LbUacb'}).text.strip()
				except:
					sponspored_elem_brand = ''

				# for rating and reviews
				try:
					sponspored_elem_rating = name_price_tag.find('g-review-stars').find('span')['aria-label'].strip()
				except:
					sponspored_elem_rating = ''

				try:
					sponspored_elem_total_reviews = name_price_tag.find('a',{'class':'fl pbAs0b'})['aria-label'].strip()
				except:
					sponspored_elem_total_reviews = ''

				try:
					sponspored_elem_return_policy = sponsored_elem.find('div',{'class':'nbd1Bd'}).text.strip()
				except:
					sponspored_elem_return_policy = ''

				req_file.write(sponspored_elem_url+'\t'+sponspored_elem_name+'\t'+sponspored_elem_price+'\t'+sponspored_elem_price_drop+'\t'+sponspored_elem_image+'\t'+sponspored_elem_brand+'\t'+sponspored_elem_rating+'\t'+sponspored_elem_total_reviews+'\t'+sponspored_elem_return_policy)
				req_file.write('\n')
		upload_file_to_s3(sponsored_result_s3_key, sponsored_result_query_file_path)


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
	chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
	chrome_options.binary_location = os.getcwd() + "/bin/headless-chromium"

	query_list = ['red sweater']

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
		
		# For Related Search
		related_search_s3_key = '{}/{}/{}_related_search.tsv'.format(S3_PROJECT_ROOT_KEY, S3_RELATED_SEARCH_PREFIX, query_clean_name)
		get_related_search_details(soup, query_clean_name, related_search_s3_key)

		# For Related Search
		serp_result_s3_key = '{}/{}/{}_serp_result.tsv'.format(S3_PROJECT_ROOT_KEY, S3_SERP_RESULT_PREFIX, query_clean_name)
		get_serp_result_details(soup, query_clean_name, serp_result_s3_key)

		# For Sponsored Products
		sponsored_result_s3_key = '{}/{}/{}_sponsored_result.tsv'.format(S3_PROJECT_ROOT_KEY, S3_SPONSORED_RESULT_PREFIX, query_clean_name)
		get_sponsored_result_details(soup, query_clean_name, sponsored_result_s3_key)

	driver.close()
