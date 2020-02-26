from utils.global_variables import *
from utils.weblogger.weblogger import *
from library.txt_get_cat_from_attr.get_cat_from_attr import getRootCatFromAttr


getCat = api.model('GetCat', {
'attribute': fields.String(required=True, description='Attribute for which Category is to be searched.',location='form', example='subject'),
})


@txt.route(getCategoryNameFromAttributeNameEndpoint, methods=['post'])
class GetCategoryFromAttribute(Resource):
	@txt.doc('get_attr')
	@txt.expect(getCat)
	def post(self):
		attribute = api.payload['attribute']		

		logger.info('Possible Category for {}'.format(attribute))
		categoryJson = getRootCatFromAttr(attribute)
		return {'attribute':categoryJson}