from utils.global_variables import *
from library.txt_generate_gram.generate_ngram import *
from utils.weblogger.weblogger import *

gramGenerator = api.model('GramGenerator', {
'ngram': fields.Integer(required=True, description='Number of Grams between 1 to 10.',location='form',example=3),
'text': fields.String(required=True, description='Text from which gram is to be generated.',location='form',example = 'This is a test')
})



@txt.route(generateNGramFromHtmlEnpoint, methods=['post'])
class InferGoogleCategory(Resource):
	@txt.doc('generate_ngram')
	@txt.expect(gramGenerator)
	def post(self):
		numberOfGrams = api.payload['ngram']	
		textContent = api.payload['text']
		logger.info('{} Gram generator called'.format(numberOfGrams))
		if numberOfGrams <= 10 :
			ngrameResultList = generateNGram(numberOfGrams, textContent)
			# return {'Generated Gram':
			# 		{
			# 			numberOfGrams : ngrameResultList
			# 		}}
			return {'generated_grams': ngrameResultList}
		else:
			return {'error_msg': 'Please enter number of grams between 1 to 10'}