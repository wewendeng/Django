import requests
import unittest
import json
import  time

class GetEventTest(unittest.TestCase):
    '''查询发布会接口'''

    def setUp(self):
        self.url = 'http://127.0.0.1:8000/api/get_event_list/'

    def tearDown(self):
        pass

    def test_event_list(self):
        '''过去event列表'''
        r = requests.get(self.url)
        result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result['status'], '110')
        self.assertEqual(result['message'], '查询成功')
        self.assertEqual(result['data'][0]['name'], '一加1发布会')

    def test_request_error(self):
        '''请求方式错误'''
        r = requests.post(self.url)
        result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result["status"], "100")
        self.assertEqual(result["message"], "请求方法错误")

class AddEventTest(unittest.TestCase):
    '''添加发布会接口'''

    def setUp(self):
        self.url = 'http://127.0.0.1:8000/api/add_event/'

    def tearDown(self):
        pass

    def test_request_error(self):
        '''请求方式错误'''
        r = requests.get(self.url)
        result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result["status"], "100")
        self.assertEqual(result["message"], "请求方法错误")

    def test_not_json_format(self):
        '''参数不是JSON格式'''
        r = requests.post(self.url)
        result = r.json()
        print(result)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result["status"], "201")
        self.assertEqual(result["message"], "参数不是JSON格式")

    def test_parameter_key_null(self):
        '''必传参数key为空'''
        headers = {"Content-Type":"application/json"}
        r = requests.post(self.url, json={}, headers=headers)
        result = r.json()
        print(result)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result["status"], "202")
        self.assertEqual(result["message"], "必传参数key不能为空")

    def test_parameter_value_null(self):
        '''必传参数value为空'''
        headers = {"Content-Type": "application/json"}
        data = {"id":"", "name":"", "limit":"", "status":"",
                "address":"", "start_time":""}
        r = requests.post(self.url, json=data, headers=headers)
        result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result["status"], "101")
        self.assertEqual(result["message"], "必传参数value为空")

    def test_parameter_id_not_int(self):
        '''必传参数id类型不是int'''
        headers = {"Content-Type": "application/json"}
        data = {"id":"abc", "name":"测试发布会", "limit":"10", "status":"1",
                "address":"深圳", "start_time":"2019-02-17 12:00:00"}
        r = requests.post(self.url, json=data, headers=headers)
        result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result["status"], "103")
        self.assertEqual(result["message"], "发布会id类型错误")

    def test_event_id_exist(self):
        '''发布会id已存在'''
        headers = {"Content-Type": "application/json"}
        data = {"id":"1", "name":"测试发布会", "limit":"10", "status":"1",
                "address":"深圳", "start_time":"2019-02-17 12:00:00"}
        r = requests.post(self.url, json=data, headers=headers)
        result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result["status"], "102")
        self.assertEqual(result["message"], "发布会id已经存在")

    def test_event_name_exist(self):
        '''发布会name已存在'''
        headers = {"Content-Type": "application/json"}
        data = {"id": "12", "name": "一加1发布会", "limit": "10",
                "status": "1", "address": "深圳", "start_time": "2019-02-17 12:00:00"}
        r = requests.post(self.url, json=data, headers=headers)
        result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result["status"], "104")
        self.assertEqual(result["message"], "发布会名称已存在")

    def test_event_time_format_error(self):
        '''发布会时间格式错误'''
        headers = {"Content-Type": "application/json"}
        data = {"id": "12", "name": "一加12发布会", "limit": "10", "status": "1",
                "address": "深圳", "start_time": "abc"}
        r = requests.post(self.url, json=data, headers=headers)
        result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result["status"], "105")
        self.assertEqual(result["message"], "日期格式错误.格式：YYYY-MM-DD HH:MM:SS.")

    def test_add_event_success(self):
        '''添加发布会成功'''
        headers = {"Content-Type": "application/json"}
        eid = int(time.time())
        data = {"id": eid, "name": "一加发布会" + str(eid), "limit": "10",
                "status": "1","address": "深圳", "start_time": "2019-02-17 12:00:00"}
        r = requests.post(self.url, json=data, headers=headers)
        result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result["status"], "200")
        self.assertEqual(result["message"], "创建成功")


if __name__ == "__main__":
    unittest.main()
