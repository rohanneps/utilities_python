from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import urllib.parse
from bs4 import BeautifulSoup
import boto3
import helper
import os
import re

SESSION = boto3.session.Session()
CURRENT_REGION = SESSION.region_name


TEMP_FOLDER = '/tmp'

BUCKET_NAME = 'us-east-1-google-serp'

S3_PROJECT_ROOT_KEY = 'rnd_region_amazon_scrape_details/{}'.format(CURRENT_REGION)
S3_HTML_PREFIX = 'page_source'
S3_SPONSORED_RESULT_PREFIX = 'sponsored_result'

S3_AMAZON_CHOICE_PREFIX = 'amazon_choice'
S3_EDITORAL_RECOMMENDATION_PREFIX = 'editoral_recommendations'
S3_MORE_BUYING_CHOICES_PREFIX = 'more_buying_choices'
S3_SERP_RESULT_PREFIX = 'serp_results'
S3_TODAY_DEALS_PREFIX = 'today_deals'
S3_BRANDS_RELATED_PREFIX = 'brands_related'

BASE_URL = 'https://www.amazon.com/s?k={}&ref=nb_sb_noss_2'

def write_page_source_to_s3(page_source_s3_key, page_source):
	s3_resource = boto3.resource("s3")
	s3_resource.Object(BUCKET_NAME, page_source_s3_key).put(Body=page_source)


def upload_file_to_s3(output_file_path, local_file):
	s3_resource = boto3.resource("s3")
	s3_resource.Object(BUCKET_NAME, output_file_path).upload_file(Filename=local_file)
	os.remove(local_file)



def get_sponsored_result_details(soup, query_clean_name, sponsored_result_s3_key):
	sponsored_section_tag = soup.find('div',{'class':'sb_2vdjSJEF'})
	if sponsored_section_tag:
		sponsored_result_query_file = '{}_sponsored_result.tsv'.format(query_clean_name)
		sponsored_result_query_file_path = os.path.join(TEMP_FOLDER, sponsored_result_query_file)
		with open(sponsored_result_query_file_path,'w') as req_file:
			req_file.write('url'+'\t'+'name'+'\t'+'image'+'\t'+'rating'+'\t'+'total_ratings'+'\t'+'prime_info')
			req_file.write('\n')
			sponsored_elem_list = sponsored_section_tag.findAll('div', recursive=False)
			for sponsored_elem in sponsored_elem_list[:-1]:
				# url section
				try:
					sponspored_elem_url = sponsored_elem.find('a')['href']
				except:
					sponspored_elem_url = ''
				# image section:
				try:
					sponspored_elem_image = sponsored_elem.find('img')['src']
				except:
					sponspored_elem_image = ''
				# name section
				try:
					sponspored_elem_name = sponsored_elem.find('div',{'class': 'sb_3pR2krbd'}).find('span').text.strip().replace('\n','')
				except:
					sponspored_elem_name = ''
				# For total ratings
				try:
					sponspored_elem_rating = sponsored_elem.find('div',{'class':'sb_3XOrDvex'})['aria-label']
				except:
					sponspored_elem_rating = ''
				# For total ratings
				try:
					sponspored_elem_total_ratings = sponsored_elem.find('div',{'class':'sb_3dDFIaal'}).text.strip()
				except:
					sponspored_elem_total_ratings = ''
				# For sponsored info
				try:
					sponspored_elem_prime_tag_val = sponsored_elem.find('img',{'class':'sb_cjpk3nRm sb_M0s9neQ0'})['alt']
					if sponspored_elem_prime_tag_val == 'Prime' :
						sponspored_elem_prime = 'Yes'
					else:
						sponspored_elem_prime = 'No'
				except:
					sponspored_elem_prime = 'No'
				
				req_file.write(sponspored_elem_url+'\t'+sponspored_elem_name+'\t'+sponspored_elem_image+'\t'+\
								sponspored_elem_rating + '\t'+ sponspored_elem_total_ratings+'\t'+sponspored_elem_prime)
				req_file.write('\n')

		upload_file_to_s3(sponsored_result_s3_key, sponsored_result_query_file_path)

def get_amazon_choice_result_details(soup, query_clean_name, amazon_choice_s3_key):
	amazon_choice_tag = soup.find('ol',{'class':'a-carousel'})
	if amazon_choice_tag:
		amazon_choice_query_file = '{}_amazon_choice.tsv'.format(query_clean_name)
		amazon_choice_query_file_path = os.path.join(TEMP_FOLDER, amazon_choice_query_file)
		with open(amazon_choice_query_file_path,'w') as req_file:
			req_file.write('url'+'\t'+'name'+'\t'+'image'+'\t'+'rating'+'\t'+'total_ratings'+'\t'+'sale_price'+'\t'+'marked_price'+'\t'+'query'+'\t'+'prime_info')
			req_file.write('\n')

			amazon_choice_list = amazon_choice_tag.findAll('li', {'class':'a-carousel-card'})

			for amazon_choice_elem in amazon_choice_list:
				# url section
				try:
					amazon_choice_elem_url = amazon_choice_elem.find('a')['href']
				except:
					amazon_choice_elem_url = ''

				# image section:
				try:
					amazon_choice_elem_image = amazon_choice_elem.find('img')['src']
				except:
					amazon_choice_elem_image = ''
				# name section
				try:
					amazon_choice_elem_name = amazon_choice_elem.find('h2').text.strip().replace('\n','')
				except:
					amazon_choice_elem_name = ''

				# rating
				try:
					amazon_choice_elem_rating = amazon_choice_elem.find('span',{'class':'a-icon-alt'}).text.strip()
				except:
					amazon_choice_elem_rating = ''

				# For total ratings
				try:
					amazon_choice_elem_total_rating = amazon_choice_elem.find('span',{'class':'a-size-base'}).text.strip()
				except:
					amazon_choice_elem_total_rating = ''
				
				# For special price
				try:
					amazon_choice_elem_sale_price = amazon_choice_elem.find('span',{'class':'a-price'}).find('span').text.strip()
				except:
					amazon_choice_elem_sale_price = ''

				# For marked price
				try:
					amazon_choice_elem_marked_price = amazon_choice_elem.find('span',{'class':'a-price a-text-price'}).find('span').text.strip()
				except:
					amazon_choice_elem_marked_price = ''
				# For Prime info
				try:
					amazon_choice_elem_prime_info_tag_val = amazon_choice_elem.find('i',{'role':'img'})['aria-label']
					if amazon_choice_elem_prime_info_tag_val == 'Amazon Prime':
						amazon_choice_elem_prime_info = 'Yes'
					else:
						amazon_choice_elem_prime_info = 'No'
				except:
					amazon_choice_elem_prime_info = 'No'
				try:
					amazon_choice_elem_query = amazon_choice_elem.find('span',{'class':'a-size-base-plus a-text-bold'}).text.strip()
				except:
					amazon_choice_elem_query = ''

				req_file.write(amazon_choice_elem_url+'\t'+amazon_choice_elem_name+'\t'+amazon_choice_elem_image+'\t'\
							   +amazon_choice_elem_rating+'\t'+amazon_choice_elem_total_rating+'\t'+amazon_choice_elem_sale_price+'\t'\
							   +amazon_choice_elem_marked_price+'\t'+amazon_choice_elem_query+'\t'+amazon_choice_elem_prime_info)
				req_file.write('\n')
				
		upload_file_to_s3(amazon_choice_s3_key, amazon_choice_query_file_path)


def get_editorial_recommendation_details(soup, query_clean_name, editorial_recommendations_s3_key):
	# editorial_recommendation_tag = soup.find('span',{'cel_widget_id':'SEARCH_RESULTS-SHOPPING_ADVISER'})
	editorial_recommendation_tag = soup.find('div',{'id':'anonCarousel2'})
	if not editorial_recommendation_tag:
		editorial_recommendation_tag = soup.findAll('span',{'cel_widget_id':'SEARCH_RESULTS-SHOPPING_ADVISER'})
		if len(editorial_recommendation_tag)>=2:
			editorial_recommendation_tag = editorial_recommendation_tag[1]
		else:
			try:
				editorial_recommendation_tag = editorial_recommendation_tag[0]
			except:
				editorial_recommendation_tag = None
		
	if editorial_recommendation_tag:
		editorial_recommendation_query_file = '{}_editorial_recommendations.tsv'.format(query_clean_name)
		editorial_recommendation_query_file_path = os.path.join(TEMP_FOLDER, editorial_recommendation_query_file)
		with open(editorial_recommendation_query_file_path,'w') as req_file:
			req_file.write('url'+'\t'+'name'+'\t'+'image'+'\t'+'rating'+'\t'+'total_ratings'+'\t'+'sale_price'+'\t'+'marked_price'+'\t'+'description'+'\t'+'best_category'+'\t'+'series'+'\t'+'prime_info')
			req_file.write('\n')

			editorial_recommendation_list = editorial_recommendation_tag.findAll('li', {'class':'a-carousel-card'})

			# skip first element
			for editorial_recommendation_elem in editorial_recommendation_list[1:]:
				# url section
				try:
					editorial_recommendation_elem_url = editorial_recommendation_elem.find('a')['href']
				except:
					editorial_recommendation_elem_url = ''

				# image section:
				try:
					editorial_recommendation_elem_image = editorial_recommendation_elem.find('img')['src']
				except:
					editorial_recommendation_elem_image = ''
				# name section
				try:
					editorial_recommendation_elem_name = editorial_recommendation_elem.find('h2').text.strip().replace('\n','')
				except:
					editorial_recommendation_elem_name = ''
				# description section
				try:
					editorial_recommendation_elem_desc = editorial_recommendation_elem.find('div',{'class':'a-section a-spacing-top-medium'}).find('span',{'class':'a-truncate-full a-offscreen'}).text.strip().replace('\n','')
				except:
					editorial_recommendation_elem_desc = ''

				# rating
				try:
					editorial_recommendation_elem_rating = editorial_recommendation_elem.find('span',{'class':'a-icon-alt'}).text.strip()
				except:
					editorial_recommendation_elem_rating = ''

				# For total ratings
				try:
					editorial_recommendation_elem_total_rating = editorial_recommendation_elem.find('span',{'class':'a-size-base'}).text.strip()
				except:
					editorial_recommendation_elem_total_rating = ''
				
				# For special price
				try:
					editorial_recommendation_elem_sale_price = editorial_recommendation_elem.find('span',{'class':'a-price'}).find('span').text.strip()
				except:
					editorial_recommendation_elem_sale_price = ''

				# For marked price
				try:
					editorial_recommendation_elem_marked_price = editorial_recommendation_elem.find('span',{'class':'a-price a-text-price'}).find('span').text.strip()
				except:
					editorial_recommendation_elem_marked_price = ''
				# For Prime info
				try:
					editorial_recommendation_elem_prime_info_tag_val = editorial_recommendation_elem.find('i',{'role':'img'})['aria-label']
					if editorial_recommendation_elem_prime_info_tag_val == 'Amazon Prime':
						editorial_recommendation_elem_prime_info = 'Yes'
					else:
						editorial_recommendation_elem_prime_info = 'No'
				except:
					editorial_recommendation_elem_prime_info = 'No'
				# For best category
				try:
					editorial_recommendation_elem_best_cat = editorial_recommendation_elem.find('div',{'class':'a-row'}).text.strip().replace('\n','')
				except:
					editorial_recommendation_elem_best_cat = ''

				# For series
				try:
					editorial_recommendation_elem_series = editorial_recommendation_elem.find('span',{'class':'a-truncate'}).find('span').text.strip().replace('\n','')
				except:
					editorial_recommendation_elem_series = ''

				req_file.write(editorial_recommendation_elem_url+'\t'+editorial_recommendation_elem_name+'\t'+\
							   editorial_recommendation_elem_image+'\t'+editorial_recommendation_elem_rating+'\t'+\
							   editorial_recommendation_elem_total_rating+'\t'+editorial_recommendation_elem_sale_price\
							   +'\t'+editorial_recommendation_elem_marked_price+'\t'+editorial_recommendation_elem_desc+'\t'\
							   +editorial_recommendation_elem_best_cat\
							   +'\t'+editorial_recommendation_elem_series+'\t'+editorial_recommendation_elem_prime_info)
				req_file.write('\n')
		upload_file_to_s3(editorial_recommendations_s3_key, editorial_recommendation_query_file_path)


def get_today_deal_details(soup, query_clean_name, today_deals_s3_key):
	today_deals_tag = soup.find('span',{'cel_widget_id':'BOTTOM-FEATURED_ASINS_LIST'})
	if today_deals_tag:
		today_deals_query_file = '{}_today\'s_deals.tsv'.format(query_clean_name)
		today_deals_query_file_path = os.path.join(TEMP_FOLDER, today_deals_query_file)
		with open(today_deals_query_file_path,'w') as req_file:
			req_file.write('url'+'\t'+'name'+'\t'+'image'+'\t'+'rating'+'\t'+'total_ratings'+'\t'+'sale_price'+'\t'+'marked_price'+'\t'+'prime_info')
			req_file.write('\n')

			today_deals_list = today_deals_tag.findAll('li', {'class':'a-carousel-card'})

			for today_deals_elem in today_deals_list:
				# url section
				try:
					# today_deals_elem_url = today_deals_elem.find('a')['href']
					today_deals_elem_url = today_deals_elem.find('img').findParent('div').findParent('a')['href']
				except:
					today_deals_elem_url = ''

				# image section:
				try:
					today_deals_elem_image = today_deals_elem.find('img')['src']
				except:
					today_deals_elem_image = ''
				# name section
				try:
					today_deals_elem_name = today_deals_elem.find('h2').text.strip().replace('\n','')
				except:
					today_deals_elem_name = ''
				# description section

				# rating
				try:
					today_deals_elem_rating = today_deals_elem.find('span',{'class':'a-icon-alt'}).text.strip()
				except:
					today_deals_elem_rating = ''

				# For total ratings
				try:
					today_deals_elem_total_rating = today_deals_elem.find('span',{'class':'a-size-base'}).text.strip()
				except:
					today_deals_elem_total_rating = ''
				
				# For special price
				try:
					today_deals_elem_sale_price = today_deals_elem.find('span',{'class':'a-price'}).find('span').text.strip()
				except:
					today_deals_elem_sale_price = ''

				# For marked price
				try:
					today_deals_elem_marked_price = today_deals_elem.find('span',{'class':'a-price a-text-price'}).find('span').text.strip()
				except:
					today_deals_elem_marked_price = ''

				# For Prime info
				try:
					today_deals_elem_prime_info_tag_val = today_deals_elem.find('i',{'class':'a-icon a-icon-prime a-icon-medium'})['aria-label']
					if today_deals_elem_prime_info_tag_val == 'Amazon Prime':
						today_deals_elem_prime_info = 'Yes'
					else:
						today_deals_elem_prime_info = 'No'
				except:
					today_deals_elem_prime_info = 'No'

				req_file.write(today_deals_elem_url+'\t'+today_deals_elem_name+'\t'+\
							   today_deals_elem_image+'\t'+today_deals_elem_rating+'\t'+\
							   today_deals_elem_total_rating+'\t'+today_deals_elem_sale_price\
							   +'\t'+today_deals_elem_marked_price+'\t'+today_deals_elem_prime_info)
				req_file.write('\n')
		upload_file_to_s3(today_deals_s3_key, today_deals_query_file_path)


def get_brands_related_details(soup, query_clean_name, brands_related_s3_key):
	brands_related_tag = soup.find('div',{'class':'threepsl-creatives'})
	if brands_related_tag:
		brands_related_query_file = '{}_brands_related.tsv'.format(query_clean_name)
		brands_related_query_file_path = os.path.join(TEMP_FOLDER, brands_related_query_file)
		with open(brands_related_query_file_path,'w') as req_file:
			req_file.write('url'+'\t'+'name'+'\t'+'image'+'\t'+'text')
			req_file.write('\n')
			brands_related_list = brands_related_tag.findAll('div', recursive=False)
			for brands_related_elem in brands_related_list:
				# url section
				try:
					brands_related_elem_url = brands_related_elem.find('a')['href']
				except:
					brands_related_elem_url = ''
				# image section:
				try:
					brands_related_elem_image = brands_related_elem.find('img')['src']
				except:
					brands_related_elem_image = ''
				# name section
				try:
					brands_related_elem_desc = brands_related_elem.find('span',{'class':'sb_34-gYLw1'}).text.strip().replace('\n','')
				except:
					brands_related_elem_desc = ''
				# description section
				try:
					brands_related_elem_name = brands_related_elem.find('span',{'class':'sb_3GxDSLVn'}).find('span').text.replace('\xa0','').split('Shop')[-1].strip()
				except:
					brands_related_elem_name = ''
				req_file.write(brands_related_elem_url+'\t'+brands_related_elem_name+'\t'+\
							   brands_related_elem_image+'\t'+brands_related_elem_desc)
				req_file.write('\n')

		upload_file_to_s3(brands_related_s3_key, brands_related_query_file_path)

def get_serp_result_details(soup, query_clean_name, serp_result_s3_key):
	serp_results_list = soup.findAll('span',{'cel_widget_id':'SEARCH_RESULTS-SEARCH_RESULTS'})
	if serp_results_list:
		serp_results_query_file = '{}_serp_results.tsv'.format(query_clean_name)
		serp_results_query_file_path = os.path.join(TEMP_FOLDER, serp_results_query_file)
		with open(serp_results_query_file_path,'w') as req_file:
			req_file.write('url'+'\t'+'name'+'\t'+'image'+'\t'+'rating'+'\t'+'total_ratings'+'\t'+'sale_price'+'\t'+'marked_price'\
							+'\t'+'stock_info'+'\t'+'coupon_info'+'\t'+'shipping_info'+'\t'+'prime_info'+'\t'+'more_buy_info'+'\t'+'sponsored')
			req_file.write('\n')

			for serp_results_elem in serp_results_list:
				# url section
				try:
					serp_results_elem_url = serp_results_elem.find('img').findParent('div').findParent('a')['href']
				except:
					serp_results_elem_url = ''

				# image section:
				try:
					serp_results_elem_image = serp_results_elem.find('img')['src']
				except:
					serp_results_elem_image = ''
				# name section
				try:
					serp_results_elem_name = serp_results_elem.find('h2').text.strip().replace('\n','')
				except:
					serp_results_elem_name = ''
				# rating
				try:
					serp_results_elem_rating = serp_results_elem.find('span',{'class':'a-icon-alt'}).text.strip()
				except:
					serp_results_elem_rating = ''

				
				# For special price
				try:
					serp_results_elem_sale_price = serp_results_elem.find('span',{'class':'a-price'}).find('span').text.strip()
				except:
					serp_results_elem_sale_price = ''

				# For marked price
				try:
					serp_results_elem_marked_price = serp_results_elem.find('span',{'class':'a-price a-text-price'}).find('span').text.strip()
				except:
					serp_results_elem_marked_price = ''

				# For stock details
				try:
					serp_results_elem_stock = serp_results_elem.find('span',{'class':'a-color-price'}).text.strip()
				except:
					serp_results_elem_stock = ''

				# For coupon info
				try:
					serp_results_elem_coupon_info = serp_results_elem.find('span',{'class':'s-coupon-unclipped'}).text.strip().replace('\n','')
				except:
					serp_results_elem_coupon_info = ''
				# For shipping info
				try:
					serp_results_elem_shipping_info = serp_results_elem.findAll('div',{'class':'sg-row'})[3].find('div',{'class':'a-section a-spacing-none a-spacing-top-micro'}).text.replace('\n',' ')
					pattern = ' ' + '{2,}'
					serp_results_elem_shipping_info = re.sub(pattern, ' ', serp_results_elem_shipping_info).strip()
				except:
					serp_results_elem_shipping_info = ''
				# For Prime info
				try:
					serp_results_elem_prime_info_tag_val = serp_results_elem.findAll('div',{'class':'sg-row'})[3].find('div',{'class':'a-section a-spacing-none a-spacing-top-micro'}).find('i')['aria-label']
					if serp_results_elem_prime_info_tag_val == 'Amazon Prime':
						serp_results_elem_prime_info = 'Yes'
					else:
						serp_results_elem_prime_info = 'No'
				except:
					serp_results_elem_prime_info = 'No'
				# For buying info
				try:
					serp_results_elem_more_buy_info = serp_results_elem.find('div',{'class':'a-section a-spacing-none a-spacing-top-mini'}).text.strip().replace('\n','')
					serp_results_elem_more_buy_info = re.sub('\s+', ' ', serp_results_elem_more_buy_info).strip().replace('$',' $')
				except:
					serp_results_elem_more_buy_info = ''

				# For sponsored info
				try:
					serp_results_elem_sponsored_tag_val = serp_results_elem.find('span',{'class':'a-size-base a-color-secondary'}).text.strip().lower()
					if serp_results_elem_sponsored_tag_val == 'sponsored' :
						serp_results_elem_sponsored = 'Yes'
					else:
						serp_results_elem_sponsored = 'No'
				except:
					serp_results_elem_sponsored = 'No'


				# For total ratings
				try:
					if serp_results_elem_sponsored != 'Yes':
						serp_results_elem_total_rating = serp_results_elem.find('span',{'class':'a-size-base'}).text.strip()
					else:
						serp_results_elem_total_rating = serp_results_elem.findAll('span',{'class':'a-size-base'})[1].text.strip()
				except:
					serp_results_elem_total_rating = ''

				req_file.write(serp_results_elem_url+'\t'+serp_results_elem_name+'\t'+\
							   serp_results_elem_image+'\t'+serp_results_elem_rating+'\t'+\
							   serp_results_elem_total_rating+'\t'+serp_results_elem_sale_price\
							   +'\t'+serp_results_elem_marked_price+'\t'+serp_results_elem_stock\
							   +'\t'+serp_results_elem_coupon_info+'\t'+serp_results_elem_shipping_info+'\t'\
							   +serp_results_elem_prime_info+'\t'
							   +serp_results_elem_more_buy_info+'\t'+serp_results_elem_sponsored)
				req_file.write('\n')
		upload_file_to_s3(serp_result_s3_key, serp_results_query_file_path)


def amazon_scrape_handler(event, context):
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

	query_list = event.get('query_list')
	client_name = event.get('client')

	driver = webdriver.Chrome(chrome_options=chrome_options)
	driver.get('https://www.amazon.com/')
	page_data = ""

	for query in query_list:
		q = urllib.parse.quote(query)
		search_url = BASE_URL.format(q)
		print(search_url)

		driver.get(search_url)
		page_data = driver.page_source
		soup = BeautifulSoup(page_data,'html.parser')
		query_clean_name = helper.get_query_clean_name(q)

		# For html page source
		page_source_s3_key = '{}/{}/{}/{}.html'.format(S3_PROJECT_ROOT_KEY, client_name, S3_HTML_PREFIX, query_clean_name)
		write_page_source_to_s3(page_source_s3_key, page_data)

		# For Sponsored Products
		sponsored_result_s3_key = '{}/{}/{}/{}_sponsored_result.tsv'.format(S3_PROJECT_ROOT_KEY, client_name, S3_SPONSORED_RESULT_PREFIX, query_clean_name)
		get_sponsored_result_details(soup, query_clean_name, sponsored_result_s3_key)

		# For Amazon's Choice
		amazon_choice_s3_key = '{}/{}/{}/{}_amazon_choice.tsv'.format(S3_PROJECT_ROOT_KEY, client_name, S3_AMAZON_CHOICE_PREFIX, query_clean_name)
		get_amazon_choice_result_details(soup, query_clean_name, amazon_choice_s3_key)

		# For Editorial Recommendations
		editorial_recommendations_s3_key = '{}/{}/{}/{}_editorial_recommendations.tsv'.format(S3_PROJECT_ROOT_KEY, client_name, S3_EDITORAL_RECOMMENDATION_PREFIX, query_clean_name)
		get_editorial_recommendation_details(soup, query_clean_name, editorial_recommendations_s3_key)

		# For Today's deals
		today_deals_s3_key = '{}/{}/{}/{}_today_deals.tsv'.format(S3_PROJECT_ROOT_KEY, client_name, S3_TODAY_DEALS_PREFIX, query_clean_name)
		get_today_deal_details(soup, query_clean_name, today_deals_s3_key)

		# For brands related
		brands_related_s3_key = '{}/{}/{}/{}_brands_related.tsv'.format(S3_PROJECT_ROOT_KEY, client_name, S3_BRANDS_RELATED_PREFIX, query_clean_name)
		get_brands_related_details(soup, query_clean_name, brands_related_s3_key)

		# For serp results
		serp_result_s3_key = '{}/{}/{}/{}_serp_result.tsv'.format(S3_PROJECT_ROOT_KEY, client_name, S3_SERP_RESULT_PREFIX, query_clean_name)
		get_serp_result_details(soup, query_clean_name, serp_result_s3_key)

	driver.close()