import unittest
from count import Calculator

class CountTest(unittest.TestCase):

    def setUp(self):
        print("test start")

    def tearDown(self):
        print("test end")

    def test_cace1(self):
        self.c = Calculator(1, 2)
        result = self.c.add()
        self.assertEqual(result, 3)

    def test_cace2(self):
        self.c = Calculator(3.0, 4.0)
        result = self.c.add()
        self.assertEqual(result, 7)

    def test_cace3(self):
        self.c = Calculator(0.3, 0.4)
        result = self.c.add()
        self.assertEqual(result, 0.7)


if __name__ == "__main__":
    # unittest.main()

    # 构造测试集
    suite = unittest.TestSuite()
    #suite.addTest(CountTest("test_cace*"))
    
    suite.addTest(CountTest("test_cace1"))
    suite.addTest(CountTest("test_cace2"))
    suite.addTest(CountTest("test_cace3"))

    # 测试执行
    runner = unittest.TextTestRunner()
    runner.run(suite)