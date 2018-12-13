import math
import json

def classes():
    with open("./Cluster/聚类.txt", "r", encoding="utf-8") as fr:
        file = fr.readlines()
        class_ = []
        for line in file:
            temp = line.split(":")
            temp = temp[1].replace("'", "")
            temp = json.loads(temp)
            class_.append(temp)
    return class_

def GetRecommendation(result, user, N=10):
    rank = result[user]
    if len(rank) > N:
        ret = rank[:N]
    else:
        ret = rank
    return ret

def check_cluster(item, tu, clusters):
    for cluster in clusters:
        if item in cluster:
            tu_ = set(tu)
            item_ = set(item)
            print(tu_, item_)
            if (tu_ & item_ != set()):
                return 1
            else:
                return 0
        else:
            return 0
def Precision(test, result, N=10):
    hit = 0
    all = 0
    clusters = classes()
    for user in test.keys():
        if user not in result:
            print("user ", user, "is a new user")
            continue
        tu = test[user] #得到user有过行为的items字典
        rank = GetRecommendation(result, user, N)  #得到推荐列表，取推荐列表中评分最高的topN
        k = int(len(rank))
        for item, pui in rank:
            if item in tu:
                hit += 1
                continue
            hit += check_cluster(item, tu, clusters)
        all += k
    print('precision命中：', hit, '总共：', all)
    return hit / (all * 1.0)

def Recall(test, result, N=10):
    hit = 0
    all = 0
    for user in test.keys():
        if user not in result:
            print("user ", user, "is a new user")
            continue
        tu = test[user]
        rank = GetRecommendation(result, user, N)
        for item, pui in rank:
            if item in tu:
                hit += 1
        all += len(tu)
    print('recall命中：',hit,'总共：', all)
    return hit / (all * 1.0)

def Coverage(train, test, result, N=5000):
    recommend_items = set()
    all_items = set()
    for user in train.keys():
        for item in train[user].keys():
            all_items.add(item)

    for user in test.keys():
        if user not in result:
            print("user ", user, "is a new user")
            continue
        rank = GetRecommendation(result, user, N)
        for item, pui in rank:
            recommend_items.add(item)
    return len(recommend_items) / (len(all_items) * 1.0)

def Popularity(train, test, result, N=5000):
    item_popularity = dict()
    for user, items in train.items():
        for item in items.keys():
            if item not in item_popularity:
                item_popularity[item] = 0
            item_popularity[item] += 1

    ret = 0
    n = 0
    for user in test.keys():
        if user not in result:
            print("user ", user, "is a new user")
            continue
        rank = GetRecommendation(result, user, N)
        for item, pui in rank:
            ret += math.log(1 + item_popularity[item])
            n += 1
    ret /= n * 1.0
    return ret