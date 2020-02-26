from utils.global_variables import *
from utils.weblogger.weblogger import *
from library.txt_get_attr_from_cat.get_attr_from_cat import getAttrFromRootCat

getAttr = api.model('GetAttr', {
'category': fields.String(required=True, description='Category for which Attribute is to be searched.',location='form', example='electronic'),
})

@txt.route(getAttributeFromCategoryEndpoint, methods=['post'])
class GetAttributeFromCategory(Resource):
	@txt.doc('get_attr')
	@txt.expect(getAttr)
	def post(self):
		category = api.payload['category']		

		logger.info('Possible Attribute identification for category {}'.format(category))
		attributeJson = getAttrFromRootCat(category)
		return {'attribute':attributeJson}