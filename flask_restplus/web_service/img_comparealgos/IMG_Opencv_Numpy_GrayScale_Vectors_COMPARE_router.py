from utils.global_variables import *
from utils.weblogger.weblogger import *
from library.img_comparealgos.ImageCompareAlgosClass import ImageCompareAlgosClass
from library.img_comparealgos.IMG_Opencv_Numpy_GrayScale_Vectors_COMPARE import main

imgParams = api.model('IMG', {
'download_base_directory': fields.String(required=True, description='Base Parent Directory'),
'log_dir': fields.String(required=True, description='Path and Log File Name'),
'src_f': fields.String(required=True, description='Source Images Folder to Compare'),
'dst_f': fields.String(required=True, description='Destination Images Folder to Compare With Source Folder')

})

@img.route('/imagecomparealgos')
class deeplearning(Resource):
    @img.doc('image_compare_algos')
    @img.expect(imgParams)
    @img.marshal_with(imgParams, code=201)
    def post(self):
        imgCompareAlgoObject = ImageCompareAlgosClass()
        request = imgCompareAlgoObject.create(api.payload)
        print (request)
        download_base_directory = request['download_base_directory']
        log_dir = request['log_dir']
        src_f = request['src_f']
        dst_f = request['dst_f']
        print(download_base_directory,log_dir,src_f,dst_f)
        final = main(download_base_directory,log_dir,src_f,dst_f)
        return final

if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0',port=5002)

