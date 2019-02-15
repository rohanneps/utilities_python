import os
from core.crawler import Crawler


if __name__=='__main__':
	home_page = 'https://example.com/'
	crawler = Crawler(domain = home_page)
	crawler.start_crawling()
	# crawl.print_crawled_list()
	crawler.write_to_file()
