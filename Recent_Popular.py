import re
import math

def Recent_Popular(pi, alpha=0.5):
    temp = pi[2]
    temp = temp[:int(temp.rfind("日"))]
    temp = re.sub(r'\D', '',temp)
    if len(temp) != 8:
        temp = '20140301'
    year = int(temp[:4]) - 1970
    month = int(temp[4:6]) - 1
    day = int(temp[6:8]) - 1
    time = year * 365 + month * 30 + day + 10
    punish = 1 / (1 + alpha *  (int(pi[1]) / (24 * 3600) - time))
    if punish > 1 or punish < 0:
        punish = 0  #未发生的新闻不可能进行推荐
    return punish