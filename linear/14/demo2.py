import math
from operator import *

dic = {'贝贝': ('战狼 2', '哪吒之魔童降世', '红海行动'), '晶晶': ('战狼 2', '流浪地球'), '欢欢': ('哪吒之魔童降世', '唐人街探案 2'), '迎迎': ('流浪地球', '红海行动', '唐人街探案 2')}
def userSim(dicc):
    item_user=dict()
    for u,items in dicc.items():
        for i in items:
            if i not in item_user.keys():
                item_user[i]=set()
            item_user[i].add(u)
    C=dict()
    N=dict()
    for item,users in item_user.items():
        for u in users:
            if u not in N.keys():
                N[u]=0
            N[u]+=1 
            for v in users:
                if u==v:
                    continue
                if (u,v) not in C.keys():
                    C[u,v]=0
                C[u,v]+=1
    W=dict()
    for co_user,cuv in C.items():
        W[co_user]=cuv / math.sqrt(N[co_user[0]]*N[co_user[1]])
    return W

def userRec(user,dicc,W2,K):
    rvi=1 
    rank=dict()
    related_user=[]
    interacted_items=dicc[user]
    for co_user,item in W2.items():
        if co_user[0]==user:
            related_user.append((co_user[1],item))

    for v,wuv in sorted(related_user,key=itemgetter(1),reverse=True)[0:K]:
        for i in dicc[v]:
            if i in interacted_items:
                continue
            if i not in rank.keys():
                rank[i]=0
            rank[i]+=wuv*rvi
    return rank

if __name__=='__main__':
    W3=userSim(dic)
    Last_Rank=userRec('晶晶',dic,W3,2)
    print (Last_Rank)