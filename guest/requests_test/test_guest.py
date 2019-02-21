import requests
import unittest
import json
import time

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
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result["status"], "10021")
        self.assertEqual(result["message"], "parameter value null")

    def test_event_id_null(self):
        '''发布会id不存在'''
        headers = {"Content-Type":"application/json"}
        data = {"eid":"100", "realname":"flen", "phone":"13612345611",
                "email":"flen@mail.com"}
        r = requests.post(self.url, json=data, headers=headers)
        result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result["status"], "10022")
        self.assertEqual(result["message"], "event id null")

    def test_event_status_not_available(self):
        '''发布会的状态未打开'''
        headers = {"Content-Type":"application/json"}
        data = {"eid":"2", "realname":"alen", "phone":"13612345678",
                "email":"alen@mail.com"}
        r = requests.post(self.url, json=data, headers=headers)
        result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result["status"], "10023")
        self.assertEqual(result["message"], "event status is not available")

    def test_event_number_is_full(self):
        '''发布会人数已满'''
        headers = {"Content-Type":"application/json"}
        data = {"eid":"1", "realname":"flen", "phone":"13612345606",
                "email":"flen@mail.com"}
        r = requests.post(self.url, json=data, headers=headers)
        result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result["status"], "10024")
        self.assertEqual(result["message"], "event number is full")

    def test_event_has_stared(self):
        '''发布会已开始'''
        headers = {"Content-Type":"application/json"}
        data = {"eid":"3", "realname":"glen", "phone":"13612345607",
                "email":"glen@mail.com"}
        r= requests.post(self.url, json=data, headers=headers)
        result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result["status"], "10025")
        self.assertEqual(result["message"], "event has started")

    def test_guest_phone_repeat(self):
        '''同一个发布会，嘉宾手机号不能重复'''
        headers = {"Content-Type":"application/json"}
        data = {"eid":"4", "realname":"llen", "phone":"13612345606",
                "email":"llen@mail.com"}
        r = requests.post(self.url, json=data, headers=headers)
        result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result["status"], "10026")
        self.assertEqual(result["message"], "the event guest phone number repeat")

    def test_add_guest_success(self):
        '''添加嘉宾成功'''
        eid = int(time.time()) # 用时间戳代替手机号，实现参数化
        headers = {"Content-Type":"application/json"}
        data = {"eid":"4", "realname":"llen", "phone": eid,
                "email":"llen@mail.com"}
        r = requests.post(self.url, json=data, headers=headers)
        result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result["status"], "200")
        self.assertEqual(result["message"], "add guest success")


if __name__ == '__main__':
    unittest.main()