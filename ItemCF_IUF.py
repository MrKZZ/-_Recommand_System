import math
import operator

def ItemSimilarity(train):
    # calculate co-rated users between items
    C = dict()
    N = dict()
    for u, items in train.items():
        for i in items:
            N.setdefault(i, 0)
            N[i] += 1
            C.setdefault(i, {})
            for j in items:
                if i == j:
                    continue
                C[i].setdefault(j, 0)
                # 这里认为活跃用户对商品之间相似度的贡献度远小于不活跃用户，因此对活跃用户做出惩罚
                C[i][j] += 1 / math.log(1 + len(items) * 1.0)

    # calculate finial similarity matrix W
    W = C.copy()
    for i, related_items in C.items():
        for j, cij in related_items.items():
            W[i][j] = cij / math.sqrt(N[i] * N[j])
    W = Normalize(W)
    return W

"""
    对矩阵进行归一化,提高推荐多样性
"""
def Normalize(W):
    for i, wj in W.items():
        if wj == {}:  #去除商品自己对自己的相似度
            continue
        max_wj = max(wj.values())
        for j, w in wj.items():
            w = w / max_wj
            W[i][j] = w
    return W

def Recommend(user_id, train, W, K=3):
    rank = dict()
    ru = train[user_id]
    for i, pi in ru.items():
        for j, wij in sorted(W[i].items(), key=operator.itemgetter(1), reverse=True)[0:K]:
            if j in ru:
                continue
            rank.setdefault(j, 0)
            rank[j] += pi[0] * wij
    rank = sorted(rank.items(), key=operator.itemgetter(1), reverse=True)
    return rank


# class Node:
#    def __init__(self):
#        self.weight = 0
#        self.reason = dict()
#
# def Recommend(user_id,train, W,K=5):
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
#            rank[j].weight += pi *wij
#            rank[j].reason[i] = pi * wij
#    return rank

def Recommendation(users, train, W, K=3):
    result = dict()
    for user in users:
        rank = Recommend(user, train, W, K)
        result[user] = rank
    return result
