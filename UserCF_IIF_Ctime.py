import math
import operator
from Recent_Popular import Recent_Popular

def UserSimilarity(train):
    # build inverse table for item_users
    item_users = dict()
    for u, items in train.items():
        for i in items.keys():
            if i not in item_users:
                item_users[i] = set()
            item_users[i].add(u)

    # calculate co-rated items between users
    C = dict()
    N = dict()
    for i, users in item_users.items():
        for u in users:
            N.setdefault(u, 0)
            N[u] += 1
            C.setdefault(u, {})
            for v in users:
                if u == v:
                    continue
                C[u].setdefault(v, 0)
                C[u][v] += 1 / math.log(1 + len(users))  #对共有商品进行惩罚
    # calculate finial similarity matrix W
    W = C.copy()
    for u, related_users in C.items():
        for v, cuv in related_users.items():
            W[u][v] = cuv / math.sqrt(N[u] * N[v])
    return W


def Recommend(user, train, W, K=3):
    rank = dict()
    interacted_items = train[user]
    for v, wuv in sorted(W[user].items(), key=operator.itemgetter(1), reverse=True)[0:K]:
        for i, rvi in train[v].items():
            # we should filter items user interacted before
            if i in interacted_items:
                continue
            rank.setdefault(i, 0)
            punish_time = Recent_Popular(rvi)
            rank[i] += wuv * rvi[0] * punish_time
    rank = sorted(rank.items(), key=operator.itemgetter(1), reverse=True)
    return rank

def Recommendation(users, train, W, K=3):
    result = dict()
    for user in users:
        rank = Recommend(user, train, W, K)
        result[user] = rank
    return result