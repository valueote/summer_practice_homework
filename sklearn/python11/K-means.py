import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans
from sklearn import datasets

# 导入数据
iris = datasets.load_iris()
print(iris.DESCR)

# 特征提取
X = iris.data
y = iris.target

# 建立KMeans聚类模型
kmeans = KMeans(n_clusters=3, random_state=0).fit(X)

# 模型评估
labels = kmeans.labels_
acc = float((labels == y).sum()) / len(y)
print('KMeans 的准确率为：%.2f' % acc)

# 可视化
fig = plt.figure(num=1, figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

for name, label in [('Setosa', 0), ('Versicolour', 1), ('Virginica', 2)]:
    ax.text3D(X[y == label, 3].mean(),
              X[y == label, 0].mean() + 1.5,
              X[y == label, 2].mean(), name,
              horizontalalignment='center',
              bbox=dict(alpha=.5, edgecolor='w', facecolor='w'))

# 重新排序标签以使颜色与聚类结果匹配
y = np.choose(y, [1, 2, 0]).astype(float)
sc = ax.scatter(X[:, 3], X[:, 0], X[:, 2], c=y, cmap='viridis', edgecolor='k')

ax.set_xlabel('Petal width')
ax.set_ylabel('Sepal length')
ax.set_zlabel('Petal length')

# 添加颜色条以显示类别
plt.colorbar(sc)

plt.show()
