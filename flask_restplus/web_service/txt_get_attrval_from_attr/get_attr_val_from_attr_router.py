from utils.global_variables import *
from utils.weblogger.weblogger import *
from library.txt_get_attrval_from_attr.get_attr_val_from_attr import getAttrValueFromAttr

getAttrVal = api.model('GetAttrVal', {
'attribute': fields.String(required=True, description='Attribute for which value is to be searched.',location='form', example='color'),
})

@txt.route(getAttributeValueFromAttributeNameEndpoint, methods=['post'])
class GetAttributeValueFromAttribute(Resource):
	@txt.doc('get_attr_val')
	@txt.expect(getAttrVal)
	def post(self):
		attribute = api.payload['attribute']		

		logger.info('Possible Attribute Value for {}'.format(attribute))
		attributeValueJson = getAttrValueFromAttr(attribute)
		return {'attribute_value':attributeValueJson}