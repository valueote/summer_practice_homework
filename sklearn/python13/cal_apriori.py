# -*- coding: utf-8 -*-
# 使用Apriori算法挖掘菜品订单关联规则
from __future__ import print_function
import pandas as pd
from apriori import *  # 导入自行编写的apriori函数

# Path to input and output files
inputfile = 'C:/Users/Lenovo/Desktop/workspace/pythonProject/算法演练/python13/13. menu_orders.xls'
outputfile = 'C:/Users/Lenovo/Desktop/workspace/pythonProject/算法演练/python13/apriori_rules.xlsx'  # 结果文件

# Read the input file with the specified engine
data = pd.read_excel(inputfile, header=None, engine='xlrd')

print('\n转换原始数据至0 - 1矩阵...')
# 转换0 - 1矩阵的过渡函数
ct = lambda x: pd.Series(1, index=x[pd.notnull(x)])
# 用map方式执行
b = map(ct, data.to_numpy())
# print(list(b))
# 实现矩阵转换，空值用0填充
data = pd.DataFrame(list(b)).fillna(0)
print(u'\n转换完毕。')
# 删除中间变量b，节省内存
del b

# 设置最小支持度和最小置信度
support = 0.2  # 最小支持度
confidence = 0.5  # 最小置信度
ms = '---'  # 连接符，默认'--'，用来区分不同元素，如A--B。需要保证原始表格中不含有该字符

# 使用apriori函数发现规则并保存结果
find_rule(data, support, confidence, ms).to_excel(outputfile, engine='openpyxl')
