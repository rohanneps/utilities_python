from utils.global_variables import *
from utils.weblogger.weblogger import *
from library.txt_profile_data.profile_data import *



profileData = api.model('profileData', {
	'filename': fields.String(required=True, description='File name location.File should be csv.',location='form', example='./dir/sample.csv')

})


@txt.route(profileDataEndpoint, methods=['post'])
class DataProfiler(Resource):
	@txt.doc('profileData')
	@txt.expect(profileData)
	def post(self):
		
		filename = api.payload['filename']		
		
		if filename.split('.')[-1] !='csv':
			return {'error_msg': 'Not a csv file.'}

		logger.info('Data profiler called for file: {}'.format(filename))
		dataProfile = generateDataProfile(filename)

		return dataProfile