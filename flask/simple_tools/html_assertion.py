from requests_html import HTMLSession
from sys import argv
DEBUG=True

USAGE='''
USAGE:
python html_assertion.py www.itest.info .thumbnail-img 4
'''

# 判断请求时参数是否为4个，是则往下执行程序，否则打印提示信息并退出程序
if len(argv) != 4:
    print(USAGE)
    exit(1)

# 赋值给变量
script_name, url, css_selector, lenght = argv

# 判断url的前四位是否为‘http’，是则往下执行程序，否则重新赋值url
if url[:4] != 'http':
    url = 'http://' + url

# 请求url并获取页面信息
session = HTMLSession()
r = session.get(url)

# 获取页面的css_selector
elements = r.html.find(css_selector)

# 定义debug方法，打印页面中的css_selector，并说明共有多少element元素，并输入每个元素的html和attrs
def debug():
    if DEBUG:
        print('*' * 100)
        print(f"css选择器：{css_selector}, 总共找到{len(elements)}个元素\n")
        for element in elements:
            print(element.html)
            print(element.attrs)
            print()

# 判断elements的长度是否为整型，是则输出成功，否则输入失败，并说明预期的个数和实际的个数
if len(elements) != int(lenght):
    print(f"失败，预期存在{lenght}，实际存在{len(elements)}个元素\n")
    debug()
    exit(1)
else:
    print(f"成功！\n")
    debug()