# from django.test import TestCase
# from django.test import Client
# from django.conf import settings

# class MyTest(TestCase):

#     def test_delete_image(self):
#         image = open(settings.STORAGE_DIR+'/image/image_3.nii', 'wb')
#         image.close()
#         c = Client()
#         response = c.delete('/app/image/3')
#         self.assertTrue(response.status_code == 200)

#     def test_get_metadata(self):
#         c=Client()
#         response=c.get('/app/image/8')
#         self.assertTrue(response.status_code == 200)
#         print('validate')