import os
import argparse
# from core.crawler import Crawler
from core.crawler_sel import Crawler


if __name__=='__main__':
	parser = argparse.ArgumentParser(description='Python Website Crawler upto n-depths')
	parser.add_argument("--website", help="Full website path here. E.g. https://somethings.com", type=str)
	parser.add_argument("--max_depth", help="Maximum deptho of crawling", type=int, default=3)


	args = parser.parse_args()
	website = args.website
	max_depth = args.max_depth

	crawler = Crawler(domain = website, max_depth = max_depth)
	try:
		crawler.start_crawling()
	except:
		pass
	
	crawler.write_to_file()	# file_writer_obj
	crawler.close_resources()
