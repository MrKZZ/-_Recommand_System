import math
import operator
from Normalize import Normalize

def ItemSimilarity(train):
    # calculate co-rated users between items
    # create user-item invertable
    C = dict()
    N = dict()
    #这里train是一个user的商品列表{user1:{item1:0, item2:0,....}}
    # 已经按照user全部分好，是一张关于user-items的倒排索引
    for u, items in train.items():  #遍历所有users
        for i in items:
            N.setdefault(i, 0)
            N[i] += 1  # the num of users who like itemi
            C.setdefault(i, {})
            for j in items:
                if i == j:
                    continue
                C[i].setdefault(j, 0)
                C[i][j] += 1  # the num of users who like itemij

    # calculate finial similarity matrix W
    W = C.copy()
    for i, related_items in C.items():
        for j, cij in related_items.items():
            W[i][j] = cij / math.sqrt(N[i] * N[j])  # punish the popular items
    W = Normalize(W)
    return W


def Recommend(user_id, train, W, K=3):
    rank = dict()
    ru = train[user_id]  #useri {items}
    for i, pi in ru.items(): #i表示物品， pi表示分数
        #对物品i的相似物品j排序
        for j, wij in sorted(W[i].items(), key=operator.itemgetter(1), reverse=True)[0:K]:
            #j表示与i相关的排序最高的物品以及相似度分数
            if j in ru:
                continue
            rank.setdefault(j, 0)
            #这里计算了user_id感兴趣的一系列物品j的打分
            rank[j] += pi[0] * wij
            #得到的一个rank是关于某个用户的推荐商品列表
    return rank

def Recommendation(users, train, W, K = 3):
    result = dict()
    for user in users:
        rank = Recommend(user, train, W, K)
        R = sorted(rank.items(), key=operator.itemgetter(1), reverse=True)
        #result存储每个用户的推荐商品列表
        result[user] = R
    return result
# class Node:
#    def __init__(self):
#        self.weight = 0
#        self.reason = dict()
#    
# def Recommend(user_id,train, W,K =3):
#    rank = dict()
#    ru = train[user_id]
#    for i,pi in ru.items():
#        for j,wij in sorted(W[i].items(), \
#                           key = operator.itemgetter(1), reverse = True)[0:K]:
#            if j in ru:
#                continue
#            if j not in rank:
#                rank[j] = Node()
#            rank[j].reason.setdefault(i,0)
#            rank[j].weight += pi * wij
#            rank[j].reason[i] = pi * wij
#    return rank


