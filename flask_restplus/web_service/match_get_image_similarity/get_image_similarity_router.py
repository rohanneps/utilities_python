from utils.global_variables import *
from utils.weblogger.weblogger import *
from utils.match_config.match_global_variables import match_model_dict
from library.match_get_image_similarity.get_image_similarity import get_image_similarity_confidence



imageSimilarityParams = api.model('MATCH', {
'image_url1': fields.String(required=True, description='Image url which is to be classified.',example='https://images-na.ssl-images-amazon.com/images/I/81SfLX17glL._UX385_.jpg'),
'image_url2': fields.String(required=True, description='Image url which is to be classified.',example='https://images-na.ssl-images-amazon.com/images/I/81R-HiKVluL._SX342_.jpg'),
'model': fields.String(required=True, description='Models to be used. View available Models from /get_models.',example='GoogleModel')
})



@match.route(getImageSimilarityEndpoint)
class ImageClassifier(Resource):
    @match.doc('image_similarity')
    @match.expect(imageSimilarityParams)
    def post(self):
        request = api.payload
        imageUrl1 = request['image_url1']
        imageUrl2 = request['image_url2']
        model = request['model']
        logger.info('Image Similarity called for urls {} and {} with model {}'.format(imageUrl1,imageUrl2, model))
        
        if model not in match_model_dict.keys():
            logger.info('Invalid model {} called'.format(model))
            return {'error_msg': 'Invalid Model Called.Models to be used. View available Models from /get_models.'}
        else:
            responseJson = get_image_similarity_confidence(model, imageUrl1, imageUrl2)
           
            return responseJson