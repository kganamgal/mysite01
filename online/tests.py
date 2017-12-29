from django.test import TestCase
from online.views.offical import *

# Create your tests here.

# python manage.py test online.tests --keepdb


class baseAPI_TestCase(TestCase):

    def setUp(self):
        '''
            excute before test.
        '''
        print("baseAPI will be tested. Now, Let's ride!")

    def tearDown(self):
        '''
            excute after test.
        '''
        print("baseAPI has been tested.")

    def test_get_All_Grandchildren_UDID(self):
        '''
            1.get all grandchildren by myql.
            2.get all grandchildren by pandas.
        '''
        test_datas = [
            42,
            43,
            44,
            45,
            46,
            90,
            116,
        ]
        for element in test_datas:
            self.assertEqual(set(get_All_Grandchildren_UDID(element)), set(new_get_All_Grandchildren_UDID(element)))