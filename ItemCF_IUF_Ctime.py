import math
import operator
from  Recent_Popular import Recent_Popular
from Normalize import Normalize

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


def Recommend(user_id, train, W, K=3):
    rank = dict()
    ru = train[user_id]
    for i, pi in ru.items():  # i 表示物品， pi表示相关信息
        for j, wij in sorted(W[i].items(), key=operator.itemgetter(1), reverse=True)[0:K]:
            if j in ru:
                continue
            rank.setdefault(j, 0)
            punish_time = Recent_Popular(pi)  # 惩罚用户对新闻的兴趣，随时间降低，alpha表示时间衰减因子
            rank[j] += pi[0] * wij * punish_time
    rank = sorted(rank.items(), key=operator.itemgetter(1), reverse=True)
    return rank


def Recommendation(users, train, W, K=3):
    result = dict()
    for user in users:
        rank = Recommend(user, train, W, K)
        result[user] = rank
    return result
