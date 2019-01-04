import pandas as pd
import ast
import time


global col_list
new_col_list = []

def break_col(row):
	original_df_pos = row.name
	for cols in col_list:
		row_col_value = row[cols]
		if row_col_value !='':
			k_v_pair = ast.literal_eval(row_col_value)
			if None in k_v_pair.keys():
				del k_v_pair[None]
			for col_k,col_v in k_v_pair.iteritems():
				new_col = cols + ':'  + col_k
				df.ix[original_df_pos, new_col] = col_v
				new_col_list.append(new_col)
			break
	



if __name__ == '__main__':
	start_time = time.time()
	df = pd.read_csv('Input/Everything Else__Dehumidifiers_specification_cols.csv')
	df.fillna(value='', inplace=True)
	col_list = df.columns.tolist()
	df.apply(break_col,axis=1)

	new_df = pd.DataFrame()
	new_df = df[list(set(new_col_list))]
	new_df.to_csv('Output/updated.csv',index=False)
	stop_time = time.time()

	print(stop_time-start_time)
