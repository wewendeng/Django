from collections import defaultdict

str = input("请输入要统计的单词：")
 
res = {}
for i in str:
    if i in res:
        res[i] = res[i] + 1
    else:
        res[i] = 1
print(res)


s = 'mississippi'
d = defaultdict(int)
for k in s:
  d[k] += 1
print(d)