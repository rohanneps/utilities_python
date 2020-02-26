from utils.global_variables import *
from utils.weblogger.weblogger import *
from library.txt_infer_google_category.infer_google_cat import *


inferGoogleCat = api.model('InferGoogleCat', {
'url': fields.String(required=True, description='Url for which Google Category is to be infered.',location='form', example='https://www.something.com'),
})


@txt.route(detectGoogleCategoryFromUrlEndpoint, methods=['post'])
class InferGoogleCategory(Resource):
	@txt.doc('inferGoogleCat')
	@txt.expect(inferGoogleCat)
	def post(self):
		url = api.payload['url']		

		logger.info('Google Cat Detection for {}'.format(url))
		inferedGooglCatJson = inferGoogleCategoryFromUrl(url)
		if inferedGooglCatJson['status_code'] == 404:
			del inferedGooglCatJson['status_code']
			return {'error_msg': '404 Error!! Page not found!!'}
		else:
			del inferedGooglCatJson['status_code']
			return {'Infered Google Categories':inferedGooglCatJson}