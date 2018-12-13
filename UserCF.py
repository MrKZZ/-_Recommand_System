import math
import operator

"""
    create user similarity matrix
    w[u][v] 对称矩阵
"""
def UserSimilarity(train):
    # build inverse table for item_users
    item_users = dict()
    for u, items in train.items():# user - items
        for i in items.keys():
            item_users.setdefault(i, set())
            item_users[i].add(u)

    # calculate co-rated items between users
    C = dict()  # C represents common set
    N = dict()  # N represents user u's items set
    for i, users in item_users.items():# item - users
        for u in users:
            N.setdefault(u, 0)
            N[u] += 1
            C.setdefault(u, {})
            for v in users:
                if u == v:
                    continue
                C[u].setdefault(v, 0)
                C[u][v] += 1  #create similirity matrix, content represents weight

    W = C.copy()
    for u, related_users in C.items():
        for v, cuv in related_users.items():
            W[u][v] = cuv / math.sqrt(N[u] * N[v])  #calculate cos similirity
    return W

"""
    sort the W[u], find the most similiar user v  
    sort the items user u may need
"""
def Recommend(user, train, W, K=3):
    rank = dict()
    interacted_items = train[user]
    #given the user, sort the top K similiar users
    for v, wuv in sorted(W[user].items(), key=operator.itemgetter(1), reverse=True)[0:K]:
        for i, rvi in train[v].items():
            # we should filter items user interacted before
            if i in interacted_items:
                continue
            rank.setdefault(i, 0)
            #calculate the score of items that were not known by user(u) but they
            #were bought by user(v)
            rank[i] += wuv * rvi[0] #wuv = similiar user; rvi = user r 对 item(i) 的兴趣
    rank = sorted(rank.items(), key=operator.itemgetter(1), reverse=True)
    return rank

"""
    calculate all users may need items
"""
def Recommendation(users, train, W, K=3):
    result = dict()
    for user in users:
        rank = Recommend(user, train, W, K)
        result[user] = rank
    return result