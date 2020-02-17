import os
import pandas as pd
from threading import Thread
from InformationExtractor import InformationExtractor
import numpy as np
import time


INPUT_DIR = 'input'
OUTPUT_DIR = 'output'

output_column_list = ['URL','raw','Seller','SellerPageLink','BasePrice','TotalPrice','ShippingCost','Tax','MinimumOrderAndShipping','PriceDroppedPercentage', 'PriceDropValue','PriceDroppedInformation']
output_df = pd.DataFrame(columns=output_column_list)

NUMBER_OF_THREAD = 700

class InformationExtractorThread(Thread):
	def __init__(self,thread_name,input_df):
		Thread.__init__(self)
		self.output_df = pd.DataFrame(columns=output_column_list)
		self.thread_name = thread_name
		self.input_df = input_df


	def run(self):
		self.input_df.apply(self.extraInfo, axis=1)



	def extraInfo(self, row):
		row_dict = dict(row)
		url = row['URL']
		base_price = row['BasePrice']
		seller = row['Seller']
		seller_pagelink = row['SellerPageLink']
		total_price = row['TotalPrice']
		row_dict['raw'] = base_price

		# print('{} ::: For url: {}'.format(self.thread_name, url))
		# print(base_price)
		# extracting info here
		inf_ext = InformationExtractor(row_dict)
		inf_ext.start_extraction()
		row_dict = inf_ext.retrieve_information()
		
		self.output_df = self.output_df.append(row_dict, ignore_index= True)
		# print('-----------------------------------------------------')
	# exit(1)



if __name__=='__main__':
	print(INPUT_DIR)
	# for roots, dirs, files in os.walk(INPUT_DIR):
	# 	for file in files[::-1]:
	file = '5c5c271bcf51886abfee9607.tsv'
	print(file)
	output_file = os.path.join(OUTPUT_DIR, file)
	start_time = time.time()
	if not os.path.exists(output_file):
		df = pd.read_csv(os.path.join(INPUT_DIR, file), sep='\t')
		print(len(df))
		df = df.fillna(value='')
		df_list = np.array_split(df, NUMBER_OF_THREAD)
		print(len(df_list[0]))
		thread_list = []

		for item in range(0, NUMBER_OF_THREAD):
			df_subset = df_list[item]
			thread_name = 'Thread{}'.format(item)
			thread = InformationExtractorThread(thread_name, df_subset)
			thread_list.append(thread)		
			thread.start()
		df = df.iloc[0:0]

		for thread in thread_list:
			thread.join()
			output_df = output_df.append(thread.output_df)


		output_df.to_csv(output_file, sep='\t', index=False)
	print(len(output_df))
	print(time.time()-start_time)