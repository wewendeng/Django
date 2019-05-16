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


with open('./data.txt', 'r') as datas:
    result = {}
    for line in datas.readlines():
        data = line.strip().split('/')
        for i in data:
            if i in result:
                result[i] = result[i] + 1
            else:
                result[i] = 1
    print(result)

# 99乘法表
for i in range(1,10):
    for j in range(1, i+1):
        result = i * j
        print("{0} * {1} = {2}\t".format(j, i, result), end='')
    print()

