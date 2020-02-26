from utils.global_variables import *
from utils.weblogger.weblogger import *
from library.txt_generate_gram_matrix.generate_gram_matrix import *



generateGramMatrixModel = api.model('generateGramMatrix', {
	'filename': fields.String(required=True, description='File name location.File should be csv.',location='form', example='./dir/sample.csv'),
	'keyField': fields.String(required=True, description='Field which is the unique identifier of each row. The field should be present in the file header.',location='form', example='sku'),
	'valField': fields.String(required=True, description='Field of which gram matrix is to be generated. The field should be present in the file header.',location='form', example='description')
})


@txt.route(generateGramMatrixEndpoint, methods=['post'])
class GenerateGramMatrix(Resource):
	@txt.doc('generateGramMatrix')
	@txt.expect(generateGramMatrixModel)
	def post(self):
		filename = api.payload['filename']		
		keyField = api.payload['keyField']
		valField = api.payload['valField']

		logger.info('Gram Matrix Generator called for file: {}'.format(filename))


		if filename.split('.')[-1] !='csv':
			return {'error_msg': 'Not a csv file.'}

		
		else:
			zippedOpPath = generateGramMatrix(filename,keyField,valField)
			logger.info('Zipped file path for file {} : {}'.format(filename,zippedOpPath)) 
			return { 'DownloadablePath': zippedOpPath }