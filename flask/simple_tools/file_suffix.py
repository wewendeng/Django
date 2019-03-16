import unittest
import os


def yaml_to_json(file_name):
    # 使用splitext函数取出文件扩展名
    file_suffix = os.path.splitext(file_name)[1]
    if file_suffix in (".yaml", ".YAML"):
        return os.path.splitext(file_name)[0] + ".json"
    elif file_suffix == "":
        return "文件没有后缀名"
    else:
        return "文件格式错误"


class MyTest(unittest.TestCase):

    def test_01(self):
        result = yaml_to_json("abc.abc")
        self.assertEqual(result, "文件格式错误")

    def test_02(self):
        result = yaml_to_json("abc.yaml")
        self.assertEqual(result, "abc.json")

    def test_03(self):
        result = yaml_to_json("abc.abc.yaml.yaml")
        self.assertEqual(result, "abc.abc.yaml.json")

    def test_04(self):
        result = yaml_to_json("yaml.yaml")
        self.assertEqual(result, "yaml.json")

    def test_05(self):
        result = yaml_to_json("yaml")
        self.assertEqual(result, "文件没有后缀名")

    def test_06(self):
        result = yaml_to_json("123.YAML")
        self.assertEqual(result, "123.json")

    def test_07(self):
        result = yaml_to_json("abc.yaml.lower()")
        self.assertEqual(result, "文件格式错误")


if __name__ == '__main__':
    unittest.main()