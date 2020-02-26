from utils.global_variables import *
from utils.weblogger.weblogger import *
from library.txt_infer_attribute_value_category.infer_attrval_category import *


inferAttrValueCat = api.model('InferAttrValueCat', {
	'platform': fields.String(required=True, description='Platform for which attribute value and category is infered. E.g.:amazon or ebay',location='form', example='amazon'),
	'text': fields.String(required=True, description='Text from which attribute value is to be identified and then subsequently category is infered.',location='form', example='Some text here.')

})


@txt.route(detectAttributeValueCategoryFromTextEndpoint, methods=['post'])
class InferAttrValCategory(Resource):
	@txt.doc('inferAttrValueCat')
	@txt.expect(inferAttrValueCat)
	def post(self):
		text = api.payload['text']		
		platform = api.payload['platform']

		logger.info('{} Category inference from attribute value called'.format(platform))

		if platform not in ['amazon','ebay']:
			return {'error_msg': 'Invalid Platform'}
		else:
			inferedCatJson = inferAttrValCategoryFromText(text,platform)
			return {'Infered {} Categories'.format(platform):inferedCatJson}



inferAttrValueCatFromPatt = api.model('InferPatternAttrValueCat', {
	'platform': fields.String(required=True, description='Platform for which attribute value and category is infered. E.g.:amazon or ebay',location='form', example='amazon'),
	'filename': fields.String(required=True, description='File name location.File should be csv.',location='form', example='./dir/sample.csv'),
	'keyField': fields.String(required=True, description='Field which is the unique identifier of each row. The field should be present in the file header.',location='form', example='sku'),
	'valField': fields.String(required=True, description='Field which is to be patternized and infered. The field should be present in the file header.',location='form', example='description'),
	'category': fields.String(required=True, description='Platform category to be used.',location='form', example='Home')

})


@txt.route(detectAttributeValueCategoryPatternFromTextEndpoint, methods=['post'])
class InferAttrValCategory(Resource):
	@txt.doc('inferAttrValueCatFromPatt')
	@txt.expect(inferAttrValueCatFromPatt)
	def post(self):
		filename = api.payload['filename']		
		platform = api.payload['platform']
		keyField = api.payload['keyField']
		valField = api.payload['valField']
		category = api.payload['category']
		logger.info('{} pattern category inference called for file: {}'.format(platform,filename))


		if filename.split('.')[-1] !='csv':
			return {'error_msg': 'Not a csv file.'}

		elif platform not in ['amazon','ebay']:
			return {'error_msg': 'Invalid Platform'}
		else:
			outputResult = inferAttrValCatPattern(platform,filename,keyField,valField,category)
			return outputResult
