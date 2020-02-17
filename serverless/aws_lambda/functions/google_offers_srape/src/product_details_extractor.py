VERTICAL_COLUMNS = ['URL','FIELD','INDEX','VALUE']

XPATH_JSON = {
					"SELLER_ROWS_XPATH"  : "//tr[contains(@class,'offer-row')]",
					"SELLER_NAME" : ".//a[contains(@class,'seller-link')]",
					"SELLER_OFFERS" : ".//td[2]",
					"SELLER_BASE_PRICE" : ".//td[3]",
					"SELLER_TOTAL_PRICE" : ".//td[4]",
					"SELLER_SITE_ACLK" : ".//td[5]/a"
					}

def checkForProductPageExists():
	try:
		driver.find_element_by_xpath("//div[@class='product-not-found']")
		return False

	except:
		return True

def getRowStringFromList(row_list):
	row_list = list(map(lambda x:str(x).replace('\n',';;'), row_list))			# substituting line break
	return '\t'.join(row_list) + '\n'

def getProductSellerDetails(driver, url):
	row_string = ''
	if checkForProductPageExists():
		seller_rows = driver.find_elements_by_xpath(XPATH_JSON['SELLER_ROWS_XPATH'])
		if len(seller_rows)>0:
			for cnt,seller_row_elem in enumerate(seller_rows):
				
				# Seller name and url
				try:
					seller_name_url_elem = seller_row_elem.find_element_by_xpath(XPATH_JSON['SELLER_NAME'])
					seller_name = seller_name_url_elem.text
					seller_url = seller_name_url_elem.get_attribute('href')
				except:
					seller_name = ''
					seller_url = ''

				row_string += getRowStringFromList([url,"SELLER_NAME",cnt,seller_name])
				row_string += getRowStringFromList([url,'SELLER_URL',cnt,seller_url])
				
				# Seller offer
				try:
					seller_offer = seller_row_elem.find_element_by_xpath(XPATH_JSON['SELLER_OFFERS']).text
				except:
					seller_offer = ''
				row_string += getRowStringFromList([url,'SELLER_OFFERS',cnt,seller_offer])

				# Seller Base Price
				try:
					seller_base_price = seller_row_elem.find_element_by_xpath(XPATH_JSON['SELLER_BASE_PRICE']).text
				except:
					seller_base_price = ''
				row_string += getRowStringFromList([url,'SELLER_BASE_PRICE',cnt,seller_base_price])

				# Seller Total Price
				try:
					seller_total_price = seller_row_elem.find_element_by_xpath(XPATH_JSON['SELLER_TOTAL_PRICE']).text
				except:
					seller_total_price = ''
				row_string += getRowStringFromList([url,'SELLER_TOTAL_PRICE',cnt,seller_total_price])

				# Seller aclk url
				try:
					seller_URL = seller_row_elem.find_element_by_xpath(XPATH_JSON['SELLER_SITE_ACLK']).get_attribute('href')
				except:
					seller_URL = ''
				row_string += getRowStringFromList([url,'SELLER_SITE_ACLK',cnt,seller_URL])
				
		else:
			# for Product with no sellers
			row_string += getRowStringFromList([url,'NoSellers','','True'])

	else:
		# for non-existent products
		row_string += getRowStringFromList([url,'ProductNotFound','',True])
	return row_string