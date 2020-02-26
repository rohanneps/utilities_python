from utils.global_variables import *
from utils.weblogger.weblogger import *
# from library.img_classify_image.classify_image_from_url import classifyImage
import requests, json

imgClassifierParams = api.model('IMG', {
'image_url': fields.String(required=True, description='Image url which is to be classified.',example='http://www.kinyu-z.net/data/wallpapers/61/916941.jpg'),
'model': fields.String(required=True, description='Models to be used viz: vgg16, vgg19,inception, resnet',example='vgg16')
})



@img.route(getImageClassification)
class ImageClassifier(Resource):
    @img.doc('image_classifier')
    @img.expect(imgClassifierParams)
    def post(self):
        request = api.payload
        imageUrl = request['image_url']
        model = request['model']
        logger.info('Image Classification called for url :{} with model {}'.format(imageUrl, model))
        imageClassificationModelList = ["vgg16","vgg19","inception","xception","resnet"]
        if model not in imageClassificationModelList:
            logger.info('Invalid model {} for url {}'.format(model, imageUrl))
            return {'error_msg': 'Invalid Model Called.'}
        else:
            # call to main function here
            # classificationJson = classifyImage(imageUrl, model)

            # background Micro Service for Server
            headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
            reqJson = { 'image_url': imageUrl,'model': model}
            imageClassifcationMicroServiceUrl = 'http://localhost:5002/img/get_image_classification'
            try:
                microServiceResponse = requests.post(imageClassifcationMicroServiceUrl,data=json.dumps(reqJson),headers=headers)
                return  microServiceResponse.json()
            except Exception as exp:
                logger.info(exp)
                return {'error_msg': 'Micro Service is not responding.'}
            
