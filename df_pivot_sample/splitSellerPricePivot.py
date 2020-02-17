import os
import pandas as pd


INPUT_DIR = 'Sellers'
OUTPUT_DIR = 'splitted_output'


if __name__ == '__main__':
	for roots, dirs, files in os.walk(INPUT_DIR):
		for __dir__ in dirs:
		# for __dir__ in ['Output.5c4afc6fcf51886abfedd5ba']:
			print(__dir__)
			
			dir_path = os.path.join(INPUT_DIR, __dir__)
			for sroots, sdirs, sfiles in os.walk(dir_path):
				for file in sfiles:
					# output_df = pd.DataFrame(columns=['URL','Seller','SellerPageLink','BasePrice','TotalPrice'])
					if file=='vertical.tsv':
						filename = __dir__.split('.')[1]
						output_file_path = os.path.join(OUTPUT_DIR, '{}.tsv'.format(filename))

						if not os.path.exists(output_file_path):
							print(file)
							
							df = pd.read_csv(os.path.join(dir_path, file), sep='\t')
							df=df[['INDEX','URL','FIELD','VALUE']]

							df = df[df['FIELD'].isin(['Seller','SellerPageLink','BasePrice','TotalPrice'])]
							pivoted =  df[['URL', 'INDEX','FIELD','VALUE']].pivot_table(values=['VALUE'], index=['INDEX','URL'], columns='FIELD', aggfunc='first').reset_index()
							pivoted.columns = [j if i == 'VALUE' else i for i,j in pivoted.columns]
							del pivoted['INDEX']
							pivoted.to_csv(output_file_path, sep='\t', index=False)
							
							
						
			print('------------------------------------------')
