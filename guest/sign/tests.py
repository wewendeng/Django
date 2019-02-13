from django.test import TestCase
from django.contrib.auth.models import User
from sign.models import Event,Guest


# Create your tests here.
# django单元测试，不是直接使用unittest


class MyTest(TestCase):

    def setUp(self):
        User.objects.create_user("test01", "test01@mail.com", "test123456")


    def test_user01(self):
        user = User.objects.get(username="test01")
        self.assertEqual(user.username, "test01")
        self.assertEqual(user.email, "test01@mail.com")


class LoginActionTest(TestCase):
    '''测试登录动作'''

    def setUp(self):
        User.objects.create_user("test01", "test01@mail.com", "test123456")

    def test_add_auther_email(self):
        '''测试添加用户'''
        user = User.objects.get(username="test01")
        self.assertEqual(user.username, "test01")
        self.assertEqual(user.email, "test01@mail.com")

    def test_login_action_username_password_null(self):
        '''用户名或者密码为空'''
        response = self.client.post('/login_action/', {'username':'', 'password':''})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"username or password null", response.content)

    def test_login_username_password_error(self):
        '''用户名或者密码错误'''
        response = self.client.post('/login_action/', {'username':'abc', 'password':'123'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'username or password is error', response.content)

    def test_login_action_success(self):
        '''登录成功'''
        response = self.client.post('/login_action/', {'username':'test01', 'password':'test123456'})
        self.assertEqual(response.status_code, 302)


class EventManageTest(TestCase):
    '''测试发布会管理'''

    def setUp(self):
        User.objects.create_user("test01", "test01@mail.com", "test123456")
        Event.objects.create(name='xiaomi5', limit=2000, address='beijing',
                             status='1', start_time='2019-2-13 12:30:00')
        login_user = {'username':'test01', 'password':'test123456'}
        self.client.post('/login_action/', data=login_user) # 先登录

    def test_add_event_data(self):
        '''测试添加发布会'''
        event = Event.objects.get(name='xiaomi5')
        self.assertEqual(event.address, "beijing")

    def test_event_manage_success(self):
        '''测试发布会小米5'''
        response = self.client.post('/event_manage/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"xiaomi5", response.content)
        self.assertIn(b"beijing", response.content)

    def test_event_manage_sreach_success(self):
        '''测试发布会搜索'''
        response = self.client.post('/search_name/', {"name":"xiaomi5"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"xiaomi5", response.content)
        self.assertIn(b"beijing", response.content)

class GuestManageTest(TestCase):
    '''测试嘉宾管理'''

    def setUp(self):
        User.objects.create_user("test01", "test01@mail.com", "test123456")
        Event.objects.create(id =1, name='xiaomi5', limit=2000, address='beijing',
                             status='1', start_time='2019-2-13 12:30:00')
        Guest.objects.create(realname="alen", phone=13612345678, email="alen@mail.com", sign=0, event_id=1)
        login_user = {'username':'test01', 'password':'test123456'}
        self.client.post('/login_action/', data=login_user) #预先登录

    def test_add_guest_data(self):
        '''测试添加嘉宾'''
        guest = Guest.objects.get(realname='alen')
        self.assertEqual(guest.phone, '13612345678')
        self.assertEqual(guest.realname, "alen")
        self.assertFalse(guest.sign)

    def test_guest_manage_success(self):
        '''测试嘉宾信息：alen'''
        response = self.client.post('/guest_manage/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"alen", response.content)
        self.assertIn(b"13612345678", response.content)

    def atest_guest_sreach_success(self):
        '''测试嘉宾搜索'''
        response = self.client.post('/search_name/', {"phone":"13612345678"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'alen', response.content)
        self.assertIn(b'13612345678', response.content)

class SignIndexActionTest(TestCase):
    '''测试发布会签到'''

    def setUp(self):
        User.objects.create_user("test01", "test01@mail.com", "test123456")
        Event.objects.create(id=1, name='xiaomi5', limit=2000, address='beijing',
                             status=1, start_time='2019-2-13 12:30:00')
        Event.objects.create(id=2, name='oneplus4', limit=2000, address='shenzhen',
                             status=1, start_time='2019-2-13 12:30:00')
        Guest.objects.create(realname='alen', phone=13612345678, email='alen@mail.com', sign=0, event_id=1)
        Guest.objects.create(realname='una', phone=13612345679, email='una@mail.com', sign=1, event_id=2)
        login_user = {"username":"test01", "password":"test123456"}
        self.client.post('/login_action/', data=login_user) #预先登录

    def test_sign_index_action_phone_null(self):
        '''手机号为空'''
        response = self.client.post('/sign_index_action/1/', {"phone":""})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Phone error', response.content)

    def test_sign_index_action_phone_or_event_id_error(self):
        '''手机号或者发布会id错误'''
        response = self.client.post('/sign_index_action/2/', {"phone":"13612345678"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Event or Phone error', response.content)

    def test_sign_index_action_user_sign_has(self):
        '''用户已签到'''
        response = self.client.post('/sign_index_action/2/', {"phone":"13612345679"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User has sign in', response.content)

    def test_sign_index_action_sign_success(self):
        '''签到成功'''
        response = self.client.post('/sign_index_action/1/', {"phone":"13612345678"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sign in success!', response.content)













