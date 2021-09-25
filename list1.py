import numpy as np
## 从.txt文件中读取数据
def loadData(flieName):
    data = np.loadtxt(fileName, dtype='int', delimiter=' ')

    # 定义两个空list，用来存放文件中的数据
    x = []
    y = []

    for line in data:
        x.append(line[1])#第一部分，即文件中的第一列数据逐一添加到list X 中
        y.append(line[2])# 第二部分，即文件中的第二列数据逐一添加到list y 中

    result1=[x,y]# x,y组成一个列表，这样可以通过函数一次性返回
    return result1
fileName='/home/deng/traindata300-300_zw44_list/uv7_1-1.list'
result=loadData(fileName)
for i in result:
    print(i)


