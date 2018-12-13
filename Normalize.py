"""
    对矩阵进行归一化,提高推荐多样性
"""
def Normalize(W):
    for i, wj in W.items():
        if wj == {}:  # 去除商品自己对自己的相似度
            continue
        max_wj = max(wj.values())
        if max_wj == 0:
            continue
        for j, w in wj.items():
            w = w / max_wj
            W[i][j] = w
    return W