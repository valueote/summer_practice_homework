# -*-coding:utf-8-*-

# 定义一个树，保存树的每一个结点
class treeNode:
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue
        self.count = numOccur
        self.parent = parentNode
        self.children = {}  # 用于存放节点的子节点
        self.nodeLink = None  # 用于连接相似的元素项

    # 对count变量增加给定值
    def inc(self, numOccur):
        self.count += numOccur

    # 用于将树以文本形式显示，对于构建树来说并不是需要的
    def disp(self, ind=1):
        print("  " * ind, self.name, "  ", self.count)
        for child in self.children.values():
            child.disp(ind + 1)

# 生成数据集
def loadSimpDat():
    simpDat=[['r', 'z', 'h', 'j', 'p'],
             ['z', 'y', 'x', 'w', 'v', 'u', 't','s'],
             ['z'],
             ['r', 'x', 'n', 'o','s'],
             ['y', 'r', 'x', 'z', 'q', 't', 'p'],
             ['y', 'z', 'x', 'e', 'q','s', 't','m']]
    return simpDat

def createInitSet(dataSet):
    retDict={}
    for trans in dataSet:
        retDict[frozenset(trans)]=1
    return retDict

# FP树的构建函数
def createTree(dataSet,minSup=1):
    #     ''' 创建FP树 '''
    #     # 第一次遍历数据集，创建头指针表
    headerTable={}
    for trans in dataSet:
        #print(trans)
        for item in trans:
            #print(item)
            headerTable[item]=headerTable.get(item,0)+dataSet[trans]
            #print(headerTable)
    label = []
    #print(headerTable)
    for k in headerTable.keys():
        if headerTable[k]<minSup:
            label.append(k)
    for i in label:
        del(headerTable[i])
    freqItemSet=set(headerTable.keys())
    if len(freqItemSet)==0:
        return None,None
    for k in headerTable:
        #print(k)
        headerTable[k]=[headerTable[k],None]
        #print(headerTable)
    retTree=treeNode("Null Set",1,None)
    for tranSet,count in dataSet.items():
        localD={}
        #print(tranSet,count)
        for item in tranSet:
            if item in freqItemSet:
                localD[item]=headerTable[item][0]
        #print(localD.items())
        if len(localD)>0:
            orderedItems=[v[0] for v in sorted(localD.items(),key=lambda e: e[1],reverse=True)]
            #print(orderedItems)
            updateTree(orderedItems,retTree,headerTable,count)
    return retTree,headerTable

def updateTree(items,inTree,headerTable,count):
    # 判断事务中的第一个元素项是否作为子节点存在，如果存在则更新该元素项的计数
    #print(items)
    #inTree.disp()
    if items[0] in inTree.children:
        #print(items[0])
        inTree.children[items[0]].inc(count)
    # 如果不存在，则创建一个新的treeeNode并将其作为子节点添加到树中
    else:
        inTree.children[items[0]]=treeNode(items[0],count,inTree)
        #print("NO",items[0])
        if headerTable[items[0]][1]==None:
            headerTable[items[0]][1]=inTree.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1],inTree.children[items[0]])
    if len(items)>1:
        #print(items[1::])
        updateTree(items[1::],inTree.children[items[0]],headerTable,count)

# 获取头指针表中该元素项对应的单链表的尾节点，然后将其指向新节点targetNode
def updateHeader(nodeToTest,targetNode):
    while(nodeToTest.nodeLink!=None):
        nodeToTest=nodeToTest.nodeLink
    nodeToTest.nodeLink=targetNode

# 辅助函数，直接修改prefixPath的值，将当前节点leafNode添加到prefixPath的末尾，然后递归添加其父节点
def ascendTree(leafNode,prefixPath):
    if leafNode.parent!=None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent,prefixPath)

# 给定元素项生成一个条件模式基（前缀路径）
# basePat表示输入的频繁项，treeNode为当前FP树中对应的第一个节点（可在函数外部通过headerTable[basePat][1]获取）
def findPrefixPath(basePat,treeNode):
    condPats={}
    while treeNode!=None:
        prefixPath=[]
        ascendTree(treeNode,prefixPath)
        if len(prefixPath)>1:
            condPats[frozenset(prefixPath[1:])]=treeNode.count
        treeNode=treeNode.nodeLink
    return condPats

# 参数：inTree和headerTable是由createTree()函数生成的数据集的FP树
#     ：minSup表示最小支持度
#     ：preFix请传入一个空集合（set([])），将在函数中用于保存当前前缀
#     ：freqItemList请传入一个空列表（[]），将用来储存生成的频繁项集
def mineTree(inTree,headerTable,minSup,preFix,freqItemList):
    #print("start")
    #print(headerTable.items())
    bigL=[v[0] for v in sorted(headerTable.items(),key=lambda e: e[1][0])]
    #print(bigL)
    for basePat in bigL:
        newFreqSet=preFix.copy()
        newFreqSet.add(basePat)
        freqItemList.append(newFreqSet)
        condPattBases=findPrefixPath(basePat,headerTable[basePat][1])
        #print(condPattBases)
        myCondTree,myHead=createTree(condPattBases,minSup)
        if myHead!=None:
            print("conditional tree for: ", newFreqSet)
            myCondTree.disp(1)
            mineTree(myCondTree,myHead,minSup,newFreqSet,freqItemList)

# 封装算法
def fpGrowth(dataSet, minSup=3):
    initSet = createInitSet(dataSet)
    myFPtree, myHeaderTab = createTree(initSet, minSup)
    freqItems = []
    mineTree(myFPtree, myHeaderTab, minSup, set([]), freqItems)
    return freqItems