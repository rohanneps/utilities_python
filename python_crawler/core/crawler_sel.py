import requests
import re
from urllib.parse import urlparse
from core.file_writer import FileWriter
from core.user_agents import get_random_user_agent
from selenium import webdriver

class Crawler():

	# link_regex_pattern = re.compile('<a [^>]*href=[\'|"](.*?)[\'"][^>]*?>')
	link_regex_pattern = re.compile('(a|script|link) [^>]*(href|src)=[\'|"](.*?)[\'"][^>]*?')
	image_regex_pattern = re.compile ('<img [^>]*src=[\'|"](.*?)[\'"].*?>')

	def __init__(self, domain, max_depth):
		self.domain = domain
		if not self.domain.endswith('/'):
			self.domain = self.domain + '/'
		self.crawled = []							
		self.site_url_list = []
		self.site_image_list = []
		self.site_category_list = []
		url_parsed = urlparse(domain)
		self.target_domain = url_parsed.netloc
		self.scheme = url_parsed.scheme
		self.driver = webdriver.Chrome(executable_path='./chromedriver')
		self.max_depth_to_crawl = max_depth
		print('Max depth of Crawling is: {}'.format(self.max_depth_to_crawl))

	def clean_links(self, path):
		path = path.replace("./", "/")
		if path.startswith('//'):
			path = self.scheme + ':' + path
		elif path.startswith('/'):
			path = self.domain  + path.replace('/','',1)
		elif not path.startswith(('http', "https")):
			if 'www' in path:
				path = self.scheme + '://' + path
			else:
				path = self.domain + path

		if path.endswith('/'):
			path = path[:len(path)-1]

		# checking where ther the scheme is https or http
		path_scheme = urlparse(path).scheme
		if path_scheme != self.scheme:
			path = path.replace(path_scheme, self.scheme)
		return path


	def get_path_source_code(self, link):
		self.driver.get(link)
		return self.driver.page_source


	def check_if_path_is_category(self, path):
		path_before_serach_q_param = path.split('?')[0]
		if (path_before_serach_q_param != path):
			if (path_before_serach_q_param in self.site_url_list) or (path_before_serach_q_param in self.site_category_list):
				self.site_category_list.append(path_before_serach_q_param)
				self.site_category_list.append(path)


	def n_depth_crawler(self, current_path, current_depth):
		
		if current_depth <= self.max_depth_to_crawl:
			print('Crawling {}'.format(current_path))
			print('Crawling depth {}'.format(current_depth))

			path_page_content  = self.get_path_source_code(current_path)
			self.crawled.append(current_path)
			self.site_url_list.append(current_path)
			
			all_path_links = self.link_regex_pattern.findall(path_page_content) # n depth level, extracting page links
			self.site_image_list += self.image_regex_pattern.findall(path_page_content)	# getting image links
			for path in all_path_links:
				# path = path.decode("utf-8")
				
				if type(path)==tuple:
					path = path[2]
				cleaned_path = self.clean_links(path)
				self.site_url_list.append(cleaned_path)
				path_needs_to_be_crawled = self.path_needs_to_be_crawled(cleaned_path)

				if path_needs_to_be_crawled and current_depth != self.max_depth_to_crawl:
					#checking is it is category based on get request pagination
					self.check_if_path_is_category(cleaned_path)
					self.n_depth_crawler(cleaned_path, current_depth+1)


	def start_crawling(self):
		start_page = self.domain
		start_page = self.clean_links(start_page)
		# print('Crawling {}'.format(start_page))
		self.n_depth_crawler(start_page, current_depth = 1)

		
	def path_needs_to_be_crawled(self, path):
		path_url_parsed = urlparse(path)
		path_url_domain = path_url_parsed.netloc
		path_ext = path.split('.')[-1].split('#')[0].split('?')[0].lower()
		if path.startswith('#') or path.startswith('mailto:') or path.startswith('tel') or path in self.crawled or self.target_domain!=path_url_domain or path_ext in['js','css','php','pdf'] or '#' in path or path_ext in ['jpg','jpeg','png','webp','gif','ico'] or 'tel:' in path or 'mail:' in path or '/javascript' in path:
			return False
		if '?cat=' not in path:		# For express.google.com test
			return False
		return True

	def print_crawled_list(self):
		print(self.crawled)

	def write_to_file(self):
		url_list = self.site_url_list + self.site_image_list
		file_writer = FileWriter(self.target_domain, url_list, self.site_category_list)
		# file_writer.get_page_type()
		file_writer.write_to_file()
		# file_writer.generate_pagesource()


	def close_resources(self):
		self.driver.close()