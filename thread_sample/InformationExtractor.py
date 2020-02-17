
class InformationExtractor():

	def __init__(self, row_dict):
		self.row_dict = row_dict
		self.raw_form = self.row_dict['raw'].lower()
		self.raw_form_splitted = self.raw_form.split(' ')
		self.shipping_seperate = True
		# print(self.raw_form)
	
	def start_extraction(self):
		# base price information extraction
		self.get_baseprice()


		# minimum order 
		self.check_minimum_order_and_shipping()

		# shipping cost
		self.get_shippingcost()

		# tax information
		self.get_taxinformation()

		# price drop
		self.check_pricedrop()

	def check_pricedrop(self):
	
		if 'price drop' in self.raw_form:
			price_drop_index = self.raw_form_splitted.index('dropped')
			self.row_dict['PriceDroppedPercentage'] = self.raw_form_splitted[price_drop_index + 1].replace('+','')
			self.row_dict['PriceDroppedInformation'] = ' '.join(self.raw_form_splitted[price_drop_index + 2 :])

			price_drop_below_index = self.raw_form_splitted.index('below')
			self.row_dict['PriceDropValue'] = self.raw_form_splitted[price_drop_below_index - 1].replace('+','')

		else:
			self.row_dict['PriceDroppedPercentage'] = ''
			self.row_dict['PriceDroppedInformation'] = ''
			self.row_dict['PriceDropValue'] = ''


	def get_baseprice(self):
		self.row_dict['BasePrice'] = self.raw_form.split(' ')[0].split('+')[0]
	
	def get_shippingcost(self):
		if 'shipping' in self.raw_form and self.shipping_seperate:
			try:
				shipping_index = self.raw_form_splitted.index('shipping')
			except:
				shipping_index = self.raw_form_splitted.index('shipping.')
			self.row_dict['ShippingCost'] = self.raw_form_splitted[shipping_index - 1].replace('+','')
		else:
			self.row_dict['ShippingCost'] = ''
		# print(self.row_dict['ShippingCost'])


	def get_taxinformation(self):
		if 'tax' in self.raw_form:
			try:
				tax_index = self.raw_form_splitted.index('tax')
			except:
				tax_index = self.raw_form_splitted.index('tax.')
			self.row_dict['Tax'] = self.raw_form_splitted[tax_index - 1].replace('+','')
		else:
			self.row_dict['Tax'] = ''
		# print(self.row_dict['Tax'])

	def check_minimum_order_and_shipping(self):
		if 'minimum order + shipping' in self.raw_form:
			self.shipping_seperate = False
			min_order_ship_index = self.raw_form_splitted.index('minimum')
			self.row_dict['MinimumOrderAndShipping'] = self.raw_form_splitted[min_order_ship_index - 1].replace('+','')
		else:
			self.row_dict['MinimumOrderAndShipping'] = ''


	def retrieve_information(self):
		# print(self.row_dict)
		return self.row_dict