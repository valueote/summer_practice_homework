import pandas as pd
from sklearn.tree import DecisionTreeClassifier as DTC
from sklearn.tree import export_graphviz

filename = 'C:/Users/Lenovo/Desktop/workspace/pythonProject/算法演练/python12/12.sales_data.txt'
data = pd.read_csv(filename, index_col='序号',encoding='utf-8')
print(data.columns)
data[data=='好'] = 1
data[data=='是'] = 1
data[data=='高'] = 1
data[data!=1] = -1

x = data.iloc[:,:3].to_numpy().astype(int)
y = data.iloc[:,3].to_numpy().astype(int)

dtc = DTC(criterion="gini").fit(x, y)

from sklearn.tree import export_graphviz

with open('tree.dot','w') as f:
    f = export_graphviz(dtc,feature_names=data.iloc[:,:3].columns, out_file=f)
