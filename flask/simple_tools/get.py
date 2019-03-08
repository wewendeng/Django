import requests
from sys import argv

USAGE='''
USAGE:
python get.py http://api.github.com
'''
# 判断请求参数个数是否为2个，不是则打印提示，是则往下执行程序，并赋值
if len(argv) != 2:
    print(USAGE)
    exit(1)

script_name, url = argv

# 判断url前四位是否为‘http’，否则重新赋值url，是则往下执行程序
if url[:4] != 'http':
    url = 'http://' + url

# 请求url并获得返回数据
r = requests.get(url)

# 打印请求的接口地址
print(f"接口地址：{url}\n")
# 打印请求返回的状态码
print(f"状态码：{r.status_code}\n")
# 打印请求的Headers
print(f"Headers:")

# 从headers中取出key，value并打印
for key, value in r.headers.items():
    print(f"{key}:{value}")

# 打印请求结果文本
print(r.text)