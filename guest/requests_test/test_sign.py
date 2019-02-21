import requests
import unittest
import json
import time

class UserSignTest(unittest.TestCase):
    '''
    测试用户签到接口
    '''

    def setUp(self):
        self.url = 'http://127.0.0.1:8000/api/user_sign/'

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
        '''请求参数key为空'''
        headers = {"Content-Type": "application/json"}
        r = requests.post(self.url, json={}, headers=headers)
        result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result["status"], "102")
        self.assertEqual(result["message"], "parameter key null")

    def test_parameter_value_null(self):
        '''请求参数值为空'''
        headers = {"Content-Type": "application/json"}
        data = {"id":"", "phone":""}
        r = requests.post(self.url, json=data, headers=headers)
        result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result["status"], "10021")
        self.assertEqual(result["message"], "parameter value null")

    def test_event_id_null(self):
        '''发布会id不存在'''
        headers = {"Content-Type": "application/json"}
        data = {"id":"999", "phone":"13612345600"}
        r = requests.post(self.url, json=data, headers=headers)
        result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result["status"], "10022")
        self.assertEqual(result["message"], "event id null")

    def test_event_status_not_available(self):
        '''发布会的状态为关闭'''
        headers = {"Content-Type": "application/json"}
        data = {"id":"2", "phone":"13612345601"}
        r = requests.post(self.url, json=data, headers=headers)
        result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result["status"], "10023")
        self.assertEqual(result["message"], "event status is not available")

    def test_event_has_started(self):
        '''发布会已开始'''
        headers = {"Content-Type": "application/json"}
        data = {"id":"3", "phone":"13612345605"}
        r = requests.post(self.url, json=data, headers=headers)
        result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result["status"], "10024")
        self.assertEqual(result["message"], "event has started")

    def test_user_phone_null(self):
        '''手机号不正确'''
        headers = {"Content-Type": "application/json"}
        data = {"id":"4", "phone":"13612345699"}
        r = requests.post(self.url, json=data, headers=headers)
        result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result["status"], "10025")
        self.assertEqual(result["message"], "user phone is null")

    def test_event_and_phont_not_match(self):
        '''手机号不属于该发布会'''
        headers = {"Content-Type": "application/json"}
        data = {"id":"4", "phone":"13612345600"}
        r = requests.post(self.url, json=data, headers=headers)
        result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result["status"], "10026")
        self.assertEqual(result["message"], "user did not participate in the conference")

    def test_user_has_sign_in(self):
        '''用户已签到'''
        headers = {"Content-Type": "application/json"}
        data = {"id":"4", "phone":"13612345606"}
        r = requests.post(self.url, json=data, headers=headers)
        result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result["status"], "10027")
        self.assertEqual(result["message"], "user has sign in")

    def test_sign_success(self):
        '''签到成功'''
        headers = {"Content-Type": "application/json"}
        data = {"id":"4", "phone":"13612345609"}
        r = requests.post(self.url, json=data, headers=headers)
        result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result["status"], "200")
        self.assertEqual(result["message"], "sign success")


if __name__ == '__main__':
    unittest.main()