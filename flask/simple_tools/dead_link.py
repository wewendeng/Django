from requests_html import HTMLSession
import requests
from sys import argv
from urllib.parse import urlparse, urljoin
DEBUG=True

USAGE='''
USAGE:
python dead_link.py www.itest.info
'''

'''
判断请求时的参数是否为2个，如果为2个，往下执行，如果不是2个，则打印提示并退出程序
'''
if len(argv) != 2:
    print(USAGE)
    exit(1)

script_name, url = argv # 定义变量并赋值

# 判断请求url开头四位是否为‘http’，如果不是‘http’，则给url重新赋值
if url[:4] != 'http':
    url = 'http://' + url

res = urlparse(url) # 获取请求url的各项属性
# 判断请求url的domain是否为空，如果为空，则打印提示信息，并且退出程序，否则程序往下执行
if res.netloc == '':
    print("无法获取站点domain信息")
    exit(1)

domain = res.netloc # 获取网站domain并赋值
print(f"站点domain：{domain}") # 打印站点domain

session = HTMLSession() # 获取网站session
r = session.get(url) # 获取session中的url

links = r.html.find('a') # 获取带有‘a’标签的link

# 遍历links列表，并判断link的属性是否含有href，有则获取此link并请求获取其各项属性，无则退出此次循环
for link in links:
    if 'href' in link.attrs:
        href = link.attrs['href']
    else:
        continue
    result = urlparse(href)
    # 判断结果的domain是否为空，为空则使用url和href拼接完成的url，并指明url的type为‘内链’，否则判断domain是否存在href中，如果存在，则url的typy为‘内链’，否则为‘外链’
    if result.netloc == '':
        href = urljoin(url, href)
        url_type = '内链'
    else:
        if domain in href:
            url_type = '内链'
        else:
            url_type = '外链'
    # 捕抓异常，判断请求是否成功，code>=400即为失败，如果请求异常，则提示请求异常
    try:
        response = requests.get(href)
        if response.status_code >= 400:
            print(f"{url_type}{href}失败")
        else:
            print(f"{url_type}{href}成功")
    except:
        print("出现异常")
    