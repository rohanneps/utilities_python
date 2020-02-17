import urllib.parse
import boto3
import json
import os
import pandas as pd
from serp_helper import (
							getAmazonSerpCatalog,
							getGoogleSerpCatalog,
							getEbaySerpCatalog,
							getWalmartSerpCatalog
						)

from text_similarity_helper import generateSimilarity
import time
import argparse


AMAZON_SERP_QUERY_STRING =  "https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords={}"
GOOGLE_SERP_QUERY_STRING = "https://www.google.com/search?output=search&tbm=shop&tbs=vw:l&q={}"
EBAY_SERP_QUERY_STRING = "https://www.ebay.com/sch/i.html?_nkw={}"
WALMART_SERP_QUERY_STRING = "https://www.walmart.com/search/?query={}"



BUCKET = "gbd-daf-dump"
BUCKET_PREFIX = "scrape_test_lambda"
TRACKER_FILE = "q_string_url_map.tsv"


SERP_PRODUCT_CATALOG_HEADERS = ['Name','Url','Image','Price','Platform']

OUTPUT_FOLDER = 'output'

def invokeLambdaFunction(url_list):
	lambd_client = boto3.client('lambda')

	payload = {
				"bucket": BUCKET,
				"project_root_folder": BUCKET_PREFIX,
				"request_tracker_file": TRACKER_FILE,
				"urls":url_list,
				}

	print('sending request')
	response = lambd_client.invoke(
								FunctionName='rndPageSourceAndScreenshotFunction',
								# InvocationType='Event',
								InvocationType='RequestResponse',
								LogType='Tail',
								Payload=json.dumps(payload)
							)

	print(response)

def downloadS3Files():
	s3_res = boto3.resource('s3')
	s3_bucket = s3_res.Bucket(BUCKET)

	filter_objs = s3_bucket.objects.filter(Prefix=BUCKET_PREFIX)

	for obj in filter_objs:
		obj_key = obj.key

		download_path = os.path.join(OUTPUT_FOLDER, obj_key.split('/')[-1])
		s3_res.Object(BUCKET, obj_key).download_file(download_path)




def sendPageSourceRequest(query):
	# lambda function invoker
	url_encode_query = urllib.parse.quote(query)
	
	amazon_q_string = AMAZON_SERP_QUERY_STRING.format(url_encode_query)
	google_q_string = GOOGLE_SERP_QUERY_STRING.format(url_encode_query)
	ebay_q_string = EBAY_SERP_QUERY_STRING.format(url_encode_query)
	walmart_q_string = WALMART_SERP_QUERY_STRING.format(url_encode_query)

	search_url_list = [amazon_q_string, google_q_string, ebay_q_string, walmart_q_string]

	invokeLambdaFunction(search_url_list)


def getS3KeyResponse(bucket, key):
	s3_client = boto3.client('s3')
	response = s3_client.get_object(Bucket=bucket,Key=key)
	return response


def processMatchRequest(query):
	# Request Tracker Dataframe
	key = '{}/{}'.format(BUCKET_PREFIX, TRACKER_FILE)
	response = getS3KeyResponse(BUCKET, key)
	df = pd.read_csv(response['Body'], sep='\t')

	serp_catalog_df = pd.DataFrame(columns=SERP_PRODUCT_CATALOG_HEADERS)

	def getProductSerpCatalog(row):
		nonlocal serp_catalog_df
		url = row['url']
		page_source_s3_key = row['page_source']
		print(url)
		print(page_source_s3_key)

		response = getS3KeyResponse(BUCKET, page_source_s3_key)

		page_source = response['Body'].read()

		if 'amazon' in url:
			# call amazon serp handler
			amazon_catalog_df = getAmazonSerpCatalog(page_source, SERP_PRODUCT_CATALOG_HEADERS)
			if len(amazon_catalog_df) > 0:
				serp_catalog_df = serp_catalog_df.append(amazon_catalog_df)

		elif 'google' in url:
			# call google serp handler
			google_catalog_df = getGoogleSerpCatalog(page_source, SERP_PRODUCT_CATALOG_HEADERS)
			if len(google_catalog_df) > 0:
				serp_catalog_df = serp_catalog_df.append(google_catalog_df)

		elif 'ebay' in url:
			# call ebay serp handler
			ebay_catalog_df = getEbaySerpCatalog(page_source, SERP_PRODUCT_CATALOG_HEADERS)
			if len(ebay_catalog_df) > 0:
				serp_catalog_df = serp_catalog_df.append(ebay_catalog_df)

		else:
			# call walmart serp handler
			walmart_catalog_df = getWalmartSerpCatalog(page_source, SERP_PRODUCT_CATALOG_HEADERS)
			if len(walmart_catalog_df) > 0:
				serp_catalog_df = serp_catalog_df.append(walmart_catalog_df)

		
		
	df.apply(getProductSerpCatalog, axis=1)

	serp_catalog_df = serp_catalog_df[SERP_PRODUCT_CATALOG_HEADERS]
	# serp_catalog_df.to_csv('allmerged.tsv',index=False,sep='\t')

	
	serp_catalog_similarity = generateSimilarity(serp_catalog_df, query,'PreProcessedName')
	
	serp_catalog_similarity = serp_catalog_similarity.sort_values(by=['TFIDF_COSINE','Price','Name'],ascending=True)
	serp_catalog_similarity.iloc[:20].to_csv('allmerged_similarity.tsv',index=False,sep='\t')

if __name__=='__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("--query", help="One of the models provided: vgg16, vgg19, resnet and inception", type=str)
	args = parser.parse_args()
	
	query = args.query
	print(query)
	# query = 'Converse Shoes Black'

	start_time = time.time()
	sendPageSourceRequest(query)
	# downloadS3Files()
	processMatchRequest(query)
	end_time = time.time()
	total_time = end_time - start_time
	print('total_time',total_time)