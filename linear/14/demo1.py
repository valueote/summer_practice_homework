import numpy as np
users = ["贝贝", "晶晶", "欢欢", "迎迎", "妮妮"]
movies = ["战狼 2", "哪吒之魔童转世", "流浪地球", "红海行动", "唐人街探案 2", "美人鱼", "我和我的祖国"]
UsMoList=[
    [1, 1, 1, 0, 1, 0, 0],
    [0, 1, 1, 0, 0, 1, 0],
    [1, 0, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 0, 0],
    [1, 1, 0, 1, 0, 1, 1]]

def RowConverCol():
    return np.array(UsMoList).transpose().tolist()
def euc_mv_sim(movieFirst: list, movieSecond:list):
     return np.sqrt(((np.array(movieFirst) - np.array(movieSecond)) ** 2).sum())
def allmv_sim():
    resDic = {}
    tempList = RowConverCol()
    for i in range(0, len(tempList)):
        for j in range(i+1, len(tempList)):
            resDic[str(i) + '-' + str(j)] = euc_mv_sim(tempList[i], tempList[j])
    return resDic
def comput_Rec_mo(username: str) -> list:
    temp = {}
    mo_sim_dic = allmv_sim()
    userindex = users.index(username)
    TargetUsermovieList = UsMoList[userindex]
    for i in range(0, len(TargetUsermovieList)):
        for j in range(i+1, len(TargetUsermovieList)):
            if TargetUsermovieList[i] == 1 and TargetUsermovieList[j] == 0 and\
                (mo_sim_dic.get(str(i) + '-' + str(j)) != None or mo_sim_dic.get(str(j) + '-' + str(i)) != None):
                sim = mo_sim_dic.get(str(i) + '-' + str(j)) if(mo_sim_dic.get(str(i) + '-' + str(j)) != None) else mo_sim_dic.get(str(j) + '-' + str(i))
                temp[j] = sim
            elif TargetUsermovieList[i] == 0 and TargetUsermovieList[j] == 1 and \
            (mo_sim_dic.get(str(i) + '-' + str(j)) != None or mo_sim_dic.get(str(j) + '-' + str(i)) != None):
                sim = mo_sim_dic.get(str(i) + '-' + str(j)) if(mo_sim_dic.get(str(i) + '-' + str(j)) != None) else mo_sim_dic.get(str(j) + '-' + str(i))
                temp[i] = sim
    temp = sorted(temp.items(), key=lambda d:d[1])
    print("推荐列表：",temp)
    recommendlist = [movies[i] for i,v in temp]
    print("电影推荐：", recommendlist)
    return recommendlist
print(allmv_sim())
comput_Rec_mo("贝贝")
comput_Rec_mo("欢欢")