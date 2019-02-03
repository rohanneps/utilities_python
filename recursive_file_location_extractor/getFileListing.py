import os
import pandas as pd
	
INPUT_DIR = 'data'						#Input DIR

df = pd.DataFrame(columns=['FilePath','FileName','FileExt'])	

FILE_PATH_LIST = []
FILE_NAME_LIST = []
FILE_EXT_LIST = []

def recursiveFilePathFinder(current_dir, root_dir):
	print(current_dir)
	current_dir_full_path = os.path.join(root_dir, current_dir)

	current_dir_file_list = os.listdir(current_dir_full_path)

	for file_or_dir in current_dir_file_list:
		file_or_dir_path = os.path.join(current_dir_full_path,file_or_dir)

		# checking if it is file or directory
		if os.path.isdir(file_or_dir_path):			# For dir
			recursiveFilePathFinder(file_or_dir, current_dir_full_path)
		else:
			file_ext = file_or_dir.split('.')[-1]
			FILE_PATH_LIST.append(file_or_dir_path)
			FILE_NAME_LIST.append(file_or_dir)
			FILE_EXT_LIST.append(file_ext)

	print('----------------------------------------------------------------')





if __name__ =='__main__':
	recursiveFilePathFinder(current_dir = INPUT_DIR, root_dir = '.')
	df['FilePath'] = FILE_PATH_LIST
	df['FileName'] = FILE_NAME_LIST
	df['FileExt'] = FILE_EXT_LIST

	df.to_csv('ALL_FILE_LOC.tsv',index=False, sep='\t')
