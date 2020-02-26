from utils.global_variables import *
from utils.weblogger.weblogger import *
from library.txt_striphtml.html_stripper import getStrippedHtml,getSourceCode

## to use
#a = {'url':'www.foxsportsasia.com'}
#headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
#res=requests.post('http://localhost:5001/txt/get_url_to_text',data=json.dumps(a),headers=headers)



# Stripping html from URL source Code

urlToHtml = api.model('UrlToHtml', {
'url': fields.String(required=True, description='Url from which Html is to be stripped.',location='form', example='https://www.something.com'),
})

# # Form Body
# parser = api.parser()
# parser.add_argument('url',required=True, type=str, help='Url from which Html is to be stripped.', location='form')


@txt.route(getStrippedHtmlTextFromUrlEnpoint, methods=['post'])
class HtmlStripFromURLService(Resource):
	@txt.doc('strip_html_from_url')
	@txt.expect(urlToHtml)
	def post(self):
		url = api.payload['url']
		logger.info('Html Stripping API service called for url {}'.format(url))
		try:
			response = getSourceCode(url)
		except Exception as exp:
			logger.info('{} is not responding'.format(url))
			return {'error_msg':'Page is not responding.'}
		strippedHtmlContent = getStrippedHtml(response.content)
		strippedHtmlJson = {}
		strippedHtmlJson['status_code'] = response.status_code
		strippedHtmlJson['stripped_html'] = strippedHtmlContent

		if strippedHtmlJson['status_code'] == 404:
			del strippedHtmlJson['status_code']
			return {'error_msg': '404 Error!! Page not found!!'}
		else:
			del strippedHtmlJson['status_code']
			return strippedHtmlJson




# Stripping html from Text

htmlToText = api.model('HtmlToText', {
'html': fields.String(required=True, description='Text from which Html is to be stripped.',location='form', example='<html><head><title>This is a test</title</head></html>'),
})


@txt.route(getTextFromHtmlEnpoint, methods=['post'])
class HtmlStripFromTextService(Resource):
	@txt.doc('strip_html_from_text')
	@txt.expect(htmlToText)
	def post(self):
		htmlText = api.payload['html']
		logger.info('Html Stripping API service from text called.')
		strippedHtmlContent = getStrippedHtml(htmlText)
		strippedHtmlJson = {}
		strippedHtmlJson['stripped_html'] = strippedHtmlContent
		return strippedHtmlJson