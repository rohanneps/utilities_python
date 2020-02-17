from io import StringIO
import boto3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from product_details_extractor import getProductSellerDetails, VERTICAL_COLUMNS,getRowStringFromList

TEMP_FOLDER = '/tmp'
TEMP_TRACKER_FILE = os.path.join(TEMP_FOLDER,'temp_output.tsv')

def intialiaze_request():
	if os.path.exists(TEMP_TRACKER_FILE):
		os.remove(TEMP_TRACKER_FILE)

def upload_file_to_s3(bucket_name, output_file_path, local_lambda_tmp_file):
	s3_resource = boto3.resource("s3")
	s3_resource.Object(bucket_name, output_file_path).upload_file(Filename=local_lambda_tmp_file)


def scrape_handler(event, context):
	intialiaze_request()

	bucket_name = event.get('bucket')
	project_root_key = event.get('project_root_folder')
	request_tracker_file_path = event.get('request_tracker_file')
	link_aclk_ids = event.get('link_aclk_ids')


	# intializing headless binary chromium
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
	

	if len(link_aclk_ids)>0:
		driver = webdriver.Chrome(chrome_options=chrome_options)
		# file header
		with open(TEMP_TRACKER_FILE,'w') as req_file:
			output_file_header = getRowStringFromList(VERTICAL_COLUMNS)
			req_file.write(output_file_header)

			# iterate over link_aclk_ids
			for link_aclk_id in link_aclk_ids:
				offers_url = 'https://www.google.com/shopping/product/1/online?prds=pid:{}'.format(link_aclk_id)
				driver.get(offers_url)
				aclk_url_row_string = getProductSellerDetails(driver, offers_url)
				req_file.write(aclk_url_row_string)

		driver.close()
		request_tracker_file_path_s3_key = '{}/{}'.format(project_root_key,request_tracker_file_path)
		upload_file_to_s3(bucket_name, request_tracker_file_path_s3_key, TEMP_TRACKER_FILE)
