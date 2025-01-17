from __future__ import print_function
import pandas as pd

# 自定义连接函数，用于实现 L_{k - 1}到 C_k 的连接
def connect_string(x, ms):
    x = list(map(lambda i: sorted(i.split(ms)), x))
    l = len(x[0])
    r = []
    for i in range(len(x)):
        for j in range(i, len(x)):
            if x[i][:l - 1] == x[j][:l - 1] and x[i][l - 1] != x[j][l - 1]:
                r.append(x[i][:l - 1] + sorted([x[j][l - 1], x[i][l - 1]]))
    return r

# 寻找关联规则的函数
def find_rule(d, support, confidence, ms='--'):
    result = pd.DataFrame(index=['support', 'confidence'])  # 定义输出结果
    support_series = 1.0 * d.sum() / len(d)  # 支持度序列
    column = list(support_series[support_series > support].index)  # 初步根据支持度筛选
    k = 0
    while len(column) > 1:
        k += 1
        print(f'\n正在进行第{k}次搜索...')
        column = connect_string(column, ms)
        print(f'数目：{len(column)}...')
        sf = lambda i: d[i].prod(axis=1, numeric_only=True)  # 新一批支持度的计算函数
        # 创建连接数据，这一步耗时、耗内存最严重。当数据集较大时，可以考虑并行运算优化。
        d_2 = pd.DataFrame(list(map(sf, column)), index=[ms.join(i) for i in column]).T
        support_series_2 = 1.0 * d_2[[ms.join(i) for i in column]].sum() / len(d)  # 计算连接后的支持度
        column = list(support_series_2[support_series_2 > support].index)  # 新一轮支持度筛选
        support_series = pd.concat([support_series, support_series_2])  # 修改此处
        column2 = []
        for i in column:  # 遍历可能的推理，如{A,B,C}究竟是 A + B-->C 还是 B + C-->A 还是 C + A-->B？
            i = i.split(ms)
            for j in range(len(i)):
                column2.append(i[:j] + i[j + 1:] + i[j:j + 1])
        cofidence_series = pd.Series(index=[ms.join(i) for i in column2])  # 定义置信度序列
        for i in column2:  # 计算置信度序列
            key = ms.join(sorted(i))
            base_key = ms.join(i[:len(i) - 1])
            if key in support_series and base_key in support_series:
                cofidence_series[ms.join(i)] = support_series[key] / support_series[base_key]
        for i in cofidence_series[cofidence_series > confidence].index:  # 置信度筛选
            result[i] = 0.0
            result[i]['confidence'] = cofidence_series[i]
            result[i]['support'] = support_series[ms.join(sorted(i.split(ms)))]
    result = result.T.sort_values(['confidence', 'support'], ascending=False)  # 结果整理，输出
    print('\n结果为：')
    print(result)
    return result
