from utils.global_variables import *
from utils.weblogger.weblogger import *
from library.txt_get_one_gram_word_errors.generateOneGramWordError import GenerateDictionary


oneGramWordError = api.model('oneGramWordError', {
	'filename': fields.String(required=True, description='File name location.File should be csv.',location='form', example='./dir/sample.csv')

})


@txt.route(getOneGramWordErrors, methods=['post'])
class DataProfiler(Resource):
	@txt.doc('oneGramWordError')
	@txt.expect(oneGramWordError)
	def post(self):
		
		filename = api.payload['filename']		
		
		if filename.split('.')[-1] !='csv':
			return {'error_msg': 'Not a csv file.'}

		logger.info('One gram word error identifier called for file: {}'.format(filename))
		oneGramResponse = GenerateDictionary(filename)

		return oneGramResponse