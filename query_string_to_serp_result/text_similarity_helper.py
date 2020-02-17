import pandas as pd
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from scipy.spatial import distance
from sklearn.metrics.pairwise import euclidean_distances
from nltk.stem.porter import PorterStemmer

stemmer = PorterStemmer()
stop_words = set(stopwords.words('english'))



def preprocess(text):
	tokenized = text.lower().split()
	preprocess_tokens = [stemmer.stem(term) for term in tokenized if term not in stop_words]
	return ' '.join(preprocess_tokens)


def generateSimilarity(df,query_string, target_column):
	df[target_column] = df['Name'].apply(preprocess)

	allsentences = [query_string] + df[target_column].tolist()

	# BOW representation
	vectorizer = CountVectorizer()
	cnt_vectorizer = vectorizer.fit_transform(allsentences)

	# TF-IDF representation
	tfidf_transformer = TfidfTransformer()
	tfidf_transformer.fit(cnt_vectorizer)

	# df['query_string'] = query_string

	q_string_cnt_vector = vectorizer.transform([query_string])
	q_string_tfidf_vector = tfidf_transformer.transform(q_string_cnt_vector)

	TFIDF_COSINE = []

	def getTextSimilarity(result_name):
		nonlocal q_string_cnt_vector, q_string_tfidf_vector
		result_string_cnt_vector = vectorizer.transform([result_name])
		result_string_tfidf_vector = tfidf_transformer.transform(result_string_cnt_vector)

		# TFIDF Cosine
		tfidf_cosine = distance.cosine(q_string_tfidf_vector[0].toarray(),result_string_tfidf_vector[0].toarray())
		TFIDF_COSINE.append(tfidf_cosine)

	df[target_column].apply(getTextSimilarity)

	df['TFIDF_COSINE'] = TFIDF_COSINE
	del df[target_column]			# removing temp preprocessed column
	
	return df

if __name__=='__main__':
	query = 'biker leather jacket'

	df = pd.read_csv('allmerged.tsv',sep='\t')
	additional_query = [query,'leather jacket red', 'leather jacket large','jacket leather']

	for add_q in additional_query:
		df = df.append({'Name':add_q}, ignore_index=True)
	df['Name'] = df['Name'].apply(preprocess)

	df = generateSimilarity(df, query)

	df.to_csv('Test.tsv',index=False,sep='\t')