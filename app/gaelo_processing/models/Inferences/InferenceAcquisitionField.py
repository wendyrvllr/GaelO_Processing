import numpy as np
import tensorflow as tf
from django.conf import settings

from tensorflow.core.framework.tensor_pb2 import TensorProto
from ..AbstractInference import AbstractInference

from skimage.transform import resize

from dicom_to_cnn.model.reader.Nifti import Nifti 
from dicom_to_cnn.model.post_processing.mip.MIP_Generator import MIP_Generator 


class InferenceAcquisitionField(AbstractInference):  

    def pre_process(self, idImage:str) -> TensorProto:
        """[summary]

        Args:
            idImage (str): [description]

        Returns:
            TensorProto: [description]
        """
        data_path = settings.STORAGE_DIR
        path_ct =data_path+'/image/image_'+idImage+'.nii'
        objet = Nifti(path_ct)
        resampled = objet.resample(shape=(256, 256, 1024))
        mip_generator = MIP_Generator(resampled)
        array=mip_generator.project(angle=0)
        #Ici va disparaitre avec un nouvel entrainement sur des tailles natives et tete en bas (reference dicom)
        #et image normalisee de 0 a 1024 puis normalise de 0 a 1
        array = np.flip(array, 0)
        array = resize(array, (503, 136))
        #fin
        array[np.where(array < 500)] = 0 #500 UH
        array[np.where(array > 1024)] = 0 #1024 UH
        array = array[:,:,]/1024
        array = np.array(array).astype('float32')
        return tf.make_tensor_proto(array, shape=[1,503,136,1])

    def post_process(self, result) -> dict:
        resultDict = {}
        for output in result.outputs:
            outputResult = result.outputs[output]
            resultDict[str(output)] = list(outputResult.float_val)
            
        dict={}
        #lef_arm down true/false
        if resultDict['left_arm'][0]>resultDict['left_arm'][1]:
            left_arm=True
        else :
            left_arm=False
        #right_arm down true/false
        if resultDict['right_arm'][0]>resultDict['right_arm'][1]:
            right_arm=True
        else :
            right_arm=False
        #vertex true/false
        if resultDict['head'][0]>resultDict['head'][1]:
            head=True
        else :
            head=False
        
        maxPosition = resultDict['leg'].index(max(resultDict['leg']))
        if(maxPosition == 0) : leg='Hips'
        if(maxPosition == 1) : leg='Knee'
        if(maxPosition == 2) : leg='Foot'

        dict={'left_arm_down':left_arm,'right_arm_down':right_arm,'head':head,'leg':leg}
        return dict

    def get_input_name(self) -> str:
        return 'input_1'
    
    def get_model_name(self) -> str:
        return 'aquisition_field_model'
        
