import pandas as pd
import numpy as np
from matplotlib import pyplot as plt2
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

offense = pd.read_csv("/home/vivy/sklearn/18/offense.csv")
defense = pd.read_csv("/home/vivy/sklearn/18/defense.csv")

offense['ToP/G'] = offense['ToP/G'] * 60
combined = pd.merge(offense, defense, how="outer", on='Team')
combined.rename(columns={'G_x': "Games", "Pts/G_x": "OffPPG", "Yds/G_x": "OffYPG", "PasY/G": "OffPassYPG", "RusY/G": "OffRushYPG", "Pts/G_y": "DefPPG", "Yds/G_y": "DefYPG", "RushYds/G": "DefRushYPG", "PassYds/G": "DefPassYPG"}, inplace=True)

# 数据探索性分析，分析各个特征之间的相关性
plt2.subplot2grid((2, 2), (0, 0))
plt2.scatter(combined.OffYPG, combined.OffPPG)
plt2.xlabel("Yards per Game")
plt2.ylabel("Points per Game")
plt2.title("Offense Yards vs Points per Game")

plt2.subplot2grid((2, 2), (0, 1))
plt2.scatter(combined.DefYPG, combined.DefPPG)
plt2.xlabel("Yards Allowed per Game")
plt2.ylabel("Points Alloed per Game")
plt2.title("Defense Yards vs Points per Game")

plt2.subplot2grid((2, 2), (1, 0))
plt2.scatter(combined['OffPassYPG'], combined.OffPPG)
plt2.xlabel("average passing yards per game")
plt2.ylabel("Points per Game")
plt2.title("Time of Possession vs Points per Game")

plt2.subplot2grid((2, 2), (1, 1))
plt2.scatter(combined['ToP/G'], combined.OffPPG)
plt2.xlabel("Time of Possession(Seconds)")
plt2.ylabel("Points per Game")
plt2.title("Time of Possession vs Points per Game")

# 数据变换，构建度量攻防能力的指标
combined['OPassStrength'] = max(combined.OffPassYPG) - combined.OffPassYPG
combined['OPassStrength'] = (1 - combined.OPassStrength / max(combined.OPassStrength)) ** 100
combined['ORushStrength'] = max(combined.OffRushYPG) - combined.OffRushYPG
combined['ORushStrength'] = (1 - combined.ORushStrength / max(combined.ORushStrength)) ** 100
combined['OPPGStrength'] = max(combined.OffPPG) - combined.OffPPG
combined['OPPGStrength'] = (1 - combined.OPPGStrength / max(combined.OPPGStrength)) ** 100
combined['OYPGStrength'] = max(combined.OffYPG) - combined.OffYPG
combined['OYPGStrength'] = (1 - combined.OYPGStrength / max(combined.OYPGStrength)) ** 100
combined['OffStrength'] = (combined.OPassStrength + combined.ORushStrength + combined.OPPGStrength + combined.OYPGStrength) / 4
combined['DPassStrength'] = max(combined.DefPassYPG) - combined.DefPassYPG
combined['DPassStrength'] = combined.DPassStrength / max(combined.DPassStrength) ** 100
combined['DRushStrength'] = max(combined.DefRushYPG) - combined.DefRushYPG
combined['DRushStrength'] = combined.DRushStrength / max(combined.DRushStrength) ** 100
combined['DPPGStrength'] = max(combined.DefPPG) - combined.DefPPG
combined['DPPGStrength'] = combined.DPPGStrength / max(combined.DPPGStrength) ** 100
combined['DYPGStrength'] = max(combined.DefYPG) - combined.DefYPG
combined['DYPGStrength'] = combined.DYPGStrength / max(combined.DYPGStrength) ** 100
combined['DefStrength'] = (combined.DPassStrength + combined.DRushStrength + combined.DPPGStrength + combined.DYPGStrength) / 4
combined['ODStrength'] = combined['OffStrength'] + combined['DefStrength']

# 数据预处理，随机拆分30%为测试数据，70%数据为训练数据
train, test = train_test_split(combined, test_size=0.3)
train_x = train.iloc[:, -6:-5]
train_y = train.iloc[:, 13]
test_x = test.iloc[:, -6:-5]
test_y = test.iloc[:, 13]

# 建立模型，并用测试数据进行预测
model = LinearRegression()
model.fit(train_x, train_y)
test_pred = model.predict(test_x)

# 模型评估，输出模型的残差平方和与方差分数
print("true value:\n", test_y)
print("pred value:\n", test_pred)
print('Residual sum of squares: %.2f' % np.mean((test_y - test_pred) ** 2))
print('variance score: %.2f' % model.score(test_x, test_y))

plt2.show()
