import os
import pandas as pd


class FileWriter():

	def __init__(self, domain, crawled_url_list):
		self.df = pd.DataFrame(columns=['URLs'])
		self.filename = domain.replace('www.','').replace('.com','')+'.tsv'
		self.crawled_url_list = crawled_url_list
		self.output_dir = 'site_crawled_output'
	def write_to_file(self):
		self.df['URLs'] = self.crawled_url_list
		if not os.path.exists(self.output_dir):
			os.makedir(self.output_dir)

		self.df.to_csv(os.path.join(self.output_dir,self.filename), sep='\t', index=False)