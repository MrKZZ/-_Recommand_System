import UserCF
import UserCF_IIF
import ItemCF
import ItemCF_IUF
import ItemCF_IUF_Ctime
import random
import Evaluation
import UserCF_Ctime
import LFM
import UserCF_IIF_Ctime
import re

def readData(filename):
    data = []
    # fileName = './u.data'    # u.data的数据中 前两列分别为user 和 item，后两列可能是rating（打分）和timestamp
    fileName = './data/' + filename + '.txt'
    with open(fileName, 'r', encoding='utf-8') as fr:
        for line in fr.readlines():
            lineArr = line.strip().split('\t')
            # 用户编号	新闻编号	浏览时间	新闻标题	新闻详细内容	新闻发表时间
            data.append([lineArr[0], lineArr[1], lineArr[2], lineArr[3], lineArr[4], lineArr[5]])
    return data

"""
    切分数据集到 train 和 test
"""
def SplitData(data):
    lastuser = ''
    for user, item, viewtime, title, content, updatatime in data:
        try:
            date = int(re.sub(r'.*月', '', updatatime)[:2])
            if date<=20 or user != lastuser:
                with open("./data/train.txt", "a", encoding="utf-8") as fw:
                    fw.write(user + "\t" + item +"\t" + viewtime + "\t" + title + "\t" + content + "\t" + updatatime+"\n")
            else:
                with open("./data/test.txt", "a", encoding="utf-8") as fw1:
                    fw1.write(user + "\t" + item+"\t" + viewtime + "\t" + title + "\t" + content + "\t" + updatatime+"\n")
        except:
            with open("./data/train.txt", "a", encoding="utf-8") as fw:
                fw.write(user + "\t" + item + "\t" + viewtime + "\t" + title + "\t" + content + "\t" + updatatime + "\n")

        finally:
            lastuser = user

# u.data的数据中 前两列分别为user 和 item
# 将列表形式数据转换为dict形式，通过二维的字典对打分进行初始化。
def transform(oriData):
    ret = dict()
    for user, item, viewtime, title, content, updatatime in oriData:
        if user not in ret:
            ret[user] = dict()
        ret[user][item] = [1, viewtime, updatatime, title]
    return ret

if __name__ == '__main__':
    #data = readData("user_click_data")
    #SplitData(data)
    traindata = readData('train')
    testdata = readData('test')
    numFlod = 1
    precision = 0
    recall = 0
    coverage = 0
    popularity = 0
    result = ''
    train = transform(traindata)
    test = transform(testdata)

    print("读取数据完毕！")
    for i in range(0, numFlod):
        #这里的train的数据结构是{user1:{item1:0,item2:0,...}
        #                        user2:{itema:0,itemb:0,...}
        #                          ....
        #                        usern:{itemx:0,itemy:0,...} }

        P,Q = LFM.LatentFactorModel(train, 50, 50, 0.02, 0.01)
        result = LFM.Recommendation(train.keys(), train, P, Q)
        # 基于用户与用户之间的协同过滤
        # W = UserCF_IIF_Ctime.UserSimilarity(train)
        # result = UserCF_IIF_Ctime.Recommendation(test.keys(), train, W)
        # 基于商品与商品之间的协同过滤
        # W = ItemCF.ItemSimilarity(train)
        # {'5218791': [], '52550': [], '5756927': [('100658325', 1.0), ('100651469', 0.97), ('100637151', 0.9)], '719605': []}
        # result为空表示对用户的推荐信息为空，即他没有与其他人有相似的浏览记录
        #result中是关于某一个用户已经排好序的推荐商品列表
        # result = ItemCF.Recommendation(train.keys(), train, W)

        N = 10  #返回top10的结果
        precision += Evaluation.Precision(test, result, N)
        recall += Evaluation.Recall(test, result, N)
        coverage += Evaluation.Coverage(train, test, result, N)
        popularity += Evaluation.Popularity(train, test, result, N)

    precision = precision * 100 / numFlod
    recall = recall * 100 / numFlod
    coverage = coverage * 100 / numFlod
    popularity /= numFlod

    # 输出结果
    print('precision = ', precision, "%")
    print('recall = %f' % recall, "%")
    print('coverage = %f' % coverage, "%")
    print('popularity = %f' % popularity)
    print("输入用户id：")
    userid = '52550'
    rank = Evaluation.GetRecommendation(result, userid)
    print("对用户", userid, "的推荐新闻为", rank)