import TextRank4Keyword

def readData(filename):
    data = []
    fileName = '../data/' + filename + '.txt'
    with open(fileName, 'r', encoding='utf-8') as fr:
        for line in fr.readlines():
            lineArr = line.strip().split('\t')
            # 用户编号	新闻编号	浏览时间	新闻标题	新闻详细内容	新闻发表时间
            data.append([lineArr[0], lineArr[1], lineArr[2], lineArr[3], lineArr[4], lineArr[5]])
    return data


"""
    构建每篇文档的关键词
"""
def keyWords(oriData):
    news = dict()
    tr4w = TextRank4Keyword.TextRank4Keyword()
    full = len(oriData)
    i = 0
    for user, item, viewtime, title, content, updatatime in oriData:
        i += 1
        if i%100 == 0:
            print("*************************** finish:",i/full)
        if item in news:
            continue
        tr4w.analyze(text=title, lower=True, window=2)  # py2中text必须是utf8编码的str或者unicode对象，py3中必须是utf8编码的bytes或者str对象
        keywords = []
        for words in tr4w.get_keywords(5, word_min_len=1):
            keywords.append(words.word)
        news[item] = keywords
    return news

"""
    计算jaccard系数
"""
def jaccard(A, B):
    A = set(A)
    B = set(B)
    return len(A&B)/len(A|B)

if __name__ == '__main__':
    traindata = readData('user_click_data')
    news = keyWords(traindata)
    print("聚类前类别数目：", len(news))
    cluster = dict()
    classes = 0
    cover = []
    for itemidA, keywordsA in news.items():
        if itemidA in cover:
            continue
        cover.append(itemidA)
        classes += 1
        cluster[classes] = [itemidA]
        for itemidB, keywordsB in  news.items():
            if itemidB in cover:
                continue
            else:
                if len(keywordsB)==0 and len(keywordsA)==0:
                    continue
                jacard_num = jaccard(keywordsA, keywordsB)
            if jacard_num > 0.2:
                cluster[classes].append(itemidB)
                cover.append(itemidB)

    print("聚类后类别数目：", len(cluster))
    with open("聚类.txt", "a", encoding="utf-8") as fw:
        for (key, value) in cluster.items():
            fw.write(str(key) + " : " + str(value) + "\n")