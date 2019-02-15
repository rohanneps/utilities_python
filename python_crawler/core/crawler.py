import requests
import re
from urllib.parse import urlparse
from core.file_writer import FileWriter
from core.user_agents import get_random_user_agent

class Crawler():

	link_regex_pattern = re.compile('<a [^>]*href=[\'|"](.*?)[\'"][^>]*?>')


	def __init__(self, domain):
		self.domain = domain
		if not self.domain.endswith('/'):
			self.domain = self.domain + '/'
		self.crawled = []
		self.site_url_list = []
		url_parsed = urlparse(domain)
		self.target_domain = url_parsed.netloc
		self.scheme = url_parsed.scheme

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


	def get_path_response_and_code(self, link):
		headers = {'User-Agent': get_random_user_agent()}
		try:
			resp = requests.get(link,headers=headers, timeout=40)
			resp_status_code = resp.status_code
		except:
			resp = None
			resp_status_code = None
		return resp, resp_status_code

	def start_crawling(self):
		start_page = self.domain
		start_page = self.clean_links(start_page)
		print('Crawling {}'.format(start_page))
		resp ,resp_status_code = self.get_path_response_and_code(start_page)			# crawling home page

		if resp_status_code == 200 and resp_status_code:

			self.crawled.append(start_page)
			self.site_url_list.append(start_page)
			# path_page_content = resp.text.encode('utf-8')
			path_page_content = resp.text

			all_path_links = self.link_regex_pattern.findall(path_page_content) # 2nd level, extracting page links

			for path in all_path_links:
				# path = path.decode("utf-8") 
				cleaned_path = self.clean_links(path)
				self.site_url_list.append(cleaned_path)
				if self.path_needs_to_be_crawled(cleaned_path):
					print('2nd level')
					print(cleaned_path)
					resp ,resp_status_code = self.get_path_response_and_code(cleaned_path)
					self.crawled.append(cleaned_path)
					if resp_status_code == 200:
						all_sub_path_links = self.link_regex_pattern.findall(cleaned_path) 		# 3rd and final level
						for sub_paths in all_sub_path_links:
							sub_paths = sub_paths.decode("utf-8")
							cleaned_sub_path = self.clean_links(sub_paths)
							print('3rd level')
							print(cleaned_sub_path)
							self.site_url_list.append(cleaned_sub_path)
							
								

	def path_needs_to_be_crawled(self, path):
		path_url_parsed = urlparse(path)
		path_url_domain = path_url_parsed.netloc
		path_ext = path.split('.')[-1].split('#')[0].split('?')[0].lower()
		if path.startswith('#') or path.startswith('mailto:') or path.startswith('tel') or path in self.crawled or self.target_domain!=path_url_domain or path_ext in['.js','.css','.php'] or '#' in path or path_ext in ['jpg','jpeg','png','webp','gif','ico']:
			return False
		return True
		
	def print_crawled_list(self):
		print(self.crawled)

	def write_to_file(self):
		file_writer = FileWriter(self.target_domain, self.site_url_list)
		file_writer.write_to_file()