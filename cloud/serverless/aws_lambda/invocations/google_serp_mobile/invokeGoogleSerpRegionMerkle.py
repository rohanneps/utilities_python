import pandas as pd
import boto3
import json
import os
import time

START_INDEX = 1
BATCH_SIZE = 30


def invokeLambdaFunction(keyword_list_batch, region):
	payload = {
				"query_list":keyword_list_batch
				}

	CLIENT = boto3.client('lambda', region_name=region)

	## Invocation for PC Page Source
	response = CLIENT.invoke(
								FunctionName='rndRegionGoogleSerp',
								InvocationType='Event',
								LogType='Tail',
								Payload=json.dumps(payload)
							)

	## Invocation for Mobile Page Source
	mobile_response = CLIENT.invoke(
								FunctionName='rndRegionGoogleSerpMobile',
								InvocationType='Event',
								LogType='Tail',
								Payload=json.dumps(payload)
							)

	print(response)
	print(mobile_response)

if __name__=='__main__':
	df = pd.read_csv(os.path.join('GrowByData - Merkle - Initial Keyword List Sephora CustomInk Sweetwater.csv'), sep=',')
	df['keyword'] = df['keyword'].str.strip()
	keyword_list = df['keyword'].unique().tolist()
	print(len(keyword_list))

	num_unique_keywords = len(keyword_list) 
	num_list = num_unique_keywords/BATCH_SIZE
	rem_rows = num_unique_keywords % BATCH_SIZE


	if rem_rows != 0:
		num_list += 1

	start_index = 0
	list_counter = 1
	num_list = int(num_list)

	for df_num in range(0,num_list):
		if list_counter == num_list and rem_rows!=0:
			last_index = start_index+rem_rows
		else:	
			last_index = start_index + BATCH_SIZE

		keyword_list_batch = keyword_list[start_index:last_index]
		print(start_index, last_index)
		print(list_counter)
		start_index = last_index

		# function here
		print('us-east-1')
		invokeLambdaFunction(keyword_list_batch, 'us-east-1')
		print('us-east-2')
		invokeLambdaFunction(keyword_list_batch, 'us-east-2')
		print('us-west-1')
		invokeLambdaFunction(keyword_list_batch, 'us-west-1')
		print('us-west-2')
		invokeLambdaFunction(keyword_list_batch, 'us-west-2')
		exit(1)
		list_counter += 1
		print('-----------------------------------------------------------')
		# exit(1)