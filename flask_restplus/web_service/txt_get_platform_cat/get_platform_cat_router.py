from utils.global_variables import *
from utils.weblogger.weblogger import *
from library.txt_get_platform_cat.get_platform_cat import getPlatformCat


getPlatformCatModel = api.model('GetPlatformCat', {
'platform': fields.String(required=True, description='Platform for which Category is to be Listed. ebay, amazon',location='form', example='amazon'),
})


@txt.route(getPlatfromCategoriesEndpoint, methods=['post'])
class getPlatformCategories(Resource):
	@txt.doc('get_platform_cat')
	@txt.expect(getPlatformCatModel)
	def post(self):
		platform = api.payload['platform']		
		logger.info('Categories for {}'.format(platform))

		if platform not in ['amazon','ebay']:
			logger.info('Incorrect platform {}'.format(platform))
			return {'error_msg': 'Invalid Platform'}
		else:	

			categoryList = sorted(getPlatformCat(platform))
			return { platform:categoryList }