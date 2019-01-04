import pandas as pd


class DataframeOptimizer(object):


	def __init__(self, unoptimized_df):

		self.unoptimized_df = unoptimized_df


	'''
	Returns dictionary of each dtype along with memory usage.
	'''

	def get_memory_usage_for_datatypes(self, df):
		self.dtype_mem_usage = {}
		for dtype in ['float','int','object']:
			selected_dtype = df.select_dtypes(include=[dtype])
			mean_usage_b = selected_dtype.memory_usage(deep=True).mean()
			mean_usage_mb = mean_usage_b / 1024 ** 2
			# print("Average memory usage for {} columns: {:03.2f} MB".format(dtype,mean_usage_mb))
			self.dtype_mem_usage[dtype] = "{:03.2f} MB".format(mean_usage_mb)

		return self.dtype_mem_usage

	'''
	Check memory usage for Dataframe or Series.
	'''
	def get_memory_usage(self, pandas_obj):
		if isinstance(pandas_obj,pd.DataFrame):
			usage_b = pandas_obj.memory_usage(deep=True).sum()
		else: # we assume if not a df it's a series
			usage_b = pandas_obj.memory_usage(deep=True)
		usage_mb = usage_b / 1024 ** 2 # convert bytes to megabytes
		return "{:03.2f} MB".format(usage_mb)

	'''
	Downcasting Integer column types.
	'''
	def optimize_int_columns(self):
		self.int_subset_df = self.unoptimized_df.select_dtypes(include=['int'])
		self.optimized_int_subset_df = self.int_subset_df.apply(pd.to_numeric,downcast='unsigned')

	'''
	Downcasting Float column types.
	'''

	def optimize_float_columns(self):
		self.float_subset_df = self.unoptimized_df.select_dtypes(include=['float'])
		self.optimized_float_subset_df = self.float_subset_df.apply(pd.to_numeric,downcast='float')


	'''
	Iterate over each object column and check if the number of unique values is less than 50%, and if so, convert it to the category type.
	'''
	def optimize_string_columns(self):
		self.object_subset_df = self.unoptimized_df.select_dtypes(include=['object']).copy()

		self.optimized_object_subset_df = pd.DataFrame()
		for col in self.object_subset_df.columns:
			num_unique_values = len(self.object_subset_df[col].unique())
			num_total_values = len(self.object_subset_df[col])

			if num_unique_values / num_total_values < 0.5:
				self.optimized_object_subset_df.loc[:,col] = self.object_subset_df[col].astype('category')
			else:
				self.optimized_object_subset_df.loc[:,col] = self.object_subset_df[col]

	'''
	Optimizing process.
	'''

	def optimize_dataframe(self):

		self.optimize_int_columns()
		self.optimize_float_columns()
		self.optimize_string_columns()

		self.optimized_df = self.unoptimized_df.copy()
		self.optimized_df[self.optimized_int_subset_df.columns] = self.optimized_int_subset_df
		self.optimized_df[self.optimized_float_subset_df.columns] = self.optimized_float_subset_df
		self.optimized_df[self.optimized_object_subset_df.columns] = self.optimized_object_subset_df

	'''
	return optimized dataframe.
	'''
	def get_optimized_dataframe(self):
		return self.optimized_df

