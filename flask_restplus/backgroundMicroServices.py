from utils.global_variables import *
from utils.weblogger.weblogger import *
from library.img_classify_image.classify_image_from_url import classifyImage

#App Initializer
app = Flask(__name__)
api = Api(app, version='1.0', title='API Micro Services',
    description='Micro Services Listings',
)



img = api.namespace('img', description='RestAPI Micro Services')

imgClassifierParams = api.model('IMG', {
'image_url': fields.String(required=True, description='Image url which is to be classified.',example='http://www.kinyu-z.net/data/wallpapers/61/916941.jpg'),
'model': fields.String(required=True, description='Models to be used viz: vgg16, vgg19,inception, resnet',example='vgg16')
})

logPrefix = 'MicroServices:'

@img.route(getImageClassification)
class ImageClassifier(Resource):
    @img.doc('image_classifier')
    @img.expect(imgClassifierParams)
    def post(self):
        request = api.payload
        imageUrl = request['image_url']
        model = request['model']
        microServiceLogger.info('{} Image Classification called for url :{} with model {}'.format(logPrefix,imageUrl, model))
    
        # call to main function here
        classificationJson = classifyImage(imageUrl, model)
        return  classificationJson

# Loading Image Classfication Models
from utils.image_classification_models_loader.load_image_models import *

if __name__ =='__main__':
	microServiceLogger.info('{} Background Micro Services Started'.format(logPrefix))


	app.run(debug=True,host='0.0.0.0',port=5002,use_reloader=False)
