import requests
import unittest
import json

class GetGuestTest(unittest.TestCase):
    '''
    获取嘉宾列表接口
    '''

    def setUp(self):
        self.url = 'http://127.0.0.1:8000/api/get_guest_list/'

    def tearDown(self):
        pass

    def test_get_guest_list(self):
        '''获取嘉宾列表'''
        r = requests.get(self.url)
        result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result["status"], "201")
        self.assertEqual(result["message"], "查询成功")
        self.assertEqual(result["data"][0]["realname"], "alen")

    def test_request_error(self):
        '''请求方法错误'''
        r = requests.post(self.url)
        result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result["status"], "404")
        self.assertEqual(result["message"], "请求方法错误")

class AddGuestTest(unittest.TestCase):
    '''
    添加嘉宾接口
    '''

    def setUp(self):
        self.url = 'http://127.0.0.1:8000/api/add_guest/'

    def tearDown(self):
        pass

    def test_request_error(self):
        '''请求方法错误'''
        r = requests.get(self.url)
        result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result["status"], "100")
        self.assertEqual(result["message"], "请求方法错误")

    def test_not_json_format(self):
        '''请求参数不是JSON格式'''
        r = requests.post(self.url)
        result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result["status"], "101")
        self.assertEqual(result["message"], "parameter not json format")

    def test_parameter_key_null(self):
        '''请求参数的key为空'''
        headers = {"Content-Type":"application/json"}
        r = requests.post(self.url, json={}, headers=headers)
        result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result["status"], "10020")
        self.assertEqual(result["message"], "parameter key null")

    def test_parameter_value_null(self):
        '''请求参数value为空'''
        headers = {"Content-Type":"application/json"}
        data = {"eid":"", "realname":"", "phone":"", "email":""}
        r = requests.post(self.url, json=data, headers=headers)
        result = r.json()
        print(result)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result["status"], "10021")
        self.assertEqual(result["message"], "parameter value null")







if __name__ == '__main__':
    unittest.main()