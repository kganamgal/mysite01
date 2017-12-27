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

    # def test_get_All_Grandchildren_UDID(self):
    #     '''
    #         thousands(n)
    #     '''
    #     test_datas = [
    #         [42,     set(old_get_All_Grandchildren_UDID(42))],
    #         [90,     set(old_get_All_Grandchildren_UDID(90))],
    #     ]
    #     for element in test_datas:
    #         self.assertEqual(set(get_All_Grandchildren_UDID(element[0])), element[1])
    def test_get_All_Grandchildren_UDID(self):
        '''
            thousands(n)
        '''
        test_datas = [
            [1,     2],
            [2,     4],
        ]
        for element in test_datas:
            self.assertEqual(element[0] * 2, element[1])


# class baseAPI_TestCase(TestCase):

#     def setUp(self):
#         '''
#             excute before test.
#         '''
#         print("baseAPI will be tested. Now, Let's ride!")

#     def tearDown(self):
#         '''
#             excute after test.
#         '''
#         print("baseAPI has been tested.")

#     def test_thousands_can_work(self):
#         '''
#             thousands(n)
#         '''
#         test_datas = [
#             [100,     '100.00'],
#             [1000,     '1,000.00'],
#             [0.2,     '0.20'],
#             [-0.2,     '-0.20'],
#             [-1000,     '-1,000.00'],
#         ]
#         for element in test_datas:
#             self.assertEqual(thousands(element[0]), element[1])

#     def test_percents_can_work(self):
#         '''
#             percents(n)
#         '''
#         test_datas = [
#             [100,     '10000.00%'],
#             [0.37289,     '37.29%'],
#             [0.2,     '20.00%'],
#             [-0.2,     '-20.00%'],
#             [-3.14,     '-314.00%'],
#         ]
#         for element in test_datas:
#             self.assertEqual(percents(element[0]), element[1])


# class permission_TestCase(TestCase):

#     def setUp(self):
#         '''
#             excute before test.
#         '''
#         print("baseAPI will be tested. Now, Let's ride!")

#     def tearDown(self):
#         '''
#             excute after test.
#         '''
#         print("baseAPI has been tested.")

#     def test_user_Is_Exist_can_work(self):
#         tP = table_Permission(用户名="guxiang")
#         tP.save()
#         test_datas = [
#             ['guxiang',     True],
#             ['reyunfei',     False],
#         ]
#         for element in test_datas:
#             self.assertEqual(getUserPermission(
#                 element[0]).user_Is_Exist(), element[1])

#     def test_user_Is_Exist_can_work(self):
#         tP = table_Permission(用户名="guxiang", 查看数据概览=1)
#         tP.save()
#         test_datas = [
#             ['guxiang',     True],
#             ['reyunfei',     False],
#         ]
#         for element in test_datas:
#             self.assertEqual(getUserPermission(
#                 element[0]).user_Is_Exist(), element[1])
