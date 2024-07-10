import FP_grow

# 将数据集加载到列表
parsedDat = [line.split() for line in open('C:/Users/Lenovo/Desktop/workspace/pythonProject/算法演练/python16/kosarak.dat').readlines()]

# 初始集合格式化
initSet = FP_grow.createInitSet(parsedDat)

# 构建FP树
myFPtree, myHeaderTab = FP_grow.createTree(initSet, 100000)

# 创建空列表，保存频繁项集
myFreqList = []
FP_grow.mineTree(myFPtree, myHeaderTab, 100000, set([]), myFreqList)

print(len(myFreqList))
print(myFreqList)