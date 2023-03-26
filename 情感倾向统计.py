# @Time : 2023/3/25 
# @Author : Lei Cong
# @File : 情感倾向统计.py
# @Software : PyCharm


from snownlp import SnowNLP
from snownlp import sentiment
import pandas as pd
import re
import csv
from tqdm import tqdm
import os


def getcsv(file):
    with open(file, encoding="utf-8-sig") as f:
        re = csv.reader(f)
        dic_ = {}
        for i in re:
            dic_[i[0]] = i[1]

        return dic_


file1 = rf"品牌爬取汇总.csv"
path1 = r"品牌汇总"

path = path1
file = file1

with open(file, 'r', encoding="utf-8-sig") as fn:
    re0 = csv.reader(fn)
    name = []
    for i in re0:
        name.append(i[0])

for j in range(len(name)):
    print(f"正在对{name[j]}的评论信息进行情感分析...")
    file_1 = path + rf"\{name[j]}\评论信息.csv"
    file_2 = path + rf"\{name[j]}\情感倾向性详细分析结果.csv"
    file_3 = path + rf"\{name[j]}\情感倾向性统计结果.csv"
    result = pd.read_csv(file_1, encoding='UTF-8', engine='python')

    try:
        os.remove(file_2)
        os.remove(file_3)
    except:
        pass

    """数据清洗"""
    content = result['content'].drop_duplicates()  ##提取content列去重
    delete = re.compile('|\n|\t|#| |')
    try:
        content = content.apply(lambda x: delete.sub('', x))
    except:
        pass

    # 改变result中content这一列的数据类型为字符串，转化成列表，其中每个元素为一条评论
    items = content.astype(str).tolist()
    # print(items)

    """情感得分的计算"""
    Data = []  # 建立一个空列表，用来存放评论和得分
    for i in tqdm(range(len(items))):
        t = SnowNLP(items[i]).sentiments  # 情感得分
        # print(t)
        a = [items[i], t]  # 评论数据和得分组成列表
        Data.append(a)  # 添加到列表Data里面
    # print(Data)
    print(f"正在对{name[j]}的情感分析进行储存...")
    head = ["content", "score"]  # 建立列表，作为文件中数据的表头
    with open(file_2, 'a', encoding='utf-8-sig', newline='') as f1:
        writer = csv.DictWriter(f1, head)
        writer.writeheader()  # 写入表头数据的时候，调用writeheader方法
        write = csv.writer(f1)
        write.writerows(Data)

    print(f"正在对{name[j]}的情感分析结果进行统计并储存...")
    # 统计结果并输出
    count_1 = 0
    count_2 = 0
    count_3 = 0
    count_4 = 0
    count_5 = 0
    count_6 = 0
    count_7 = 0
    count_8 = 0
    count_9 = 0
    count_10 = 0
    for i in Data:
        if i[1] >= 0.9:
            count_1 += 1
        elif i[1] >= 0.8:
            count_2 += 1
        elif i[1] >= 0.7:
            count_3 += 1
        elif i[1] >= 0.6:
            count_4 += 1
        elif i[1] >= 0.5:
            count_5 += 1
        elif i[1] >= 0.4:
            count_6 += 1
        elif i[1] >= 0.3:
            count_7 += 1
        elif i[1] >= 0.2:
            count_8 += 1
        elif i[1] >= 0.1:
            count_9 += 1
        elif i[1] >= 0.0:
            count_10 += 1
    count = count_1 + count_2 + count_3 + count_4 + count_5 + count_6 + count_7 + count_8 + count_9 + count_10
    with open(file_3, 'a', encoding="utf-8-sig", newline="") as f2:
        wr_1 = csv.writer(f2)
        wr_1.writerow(["分数段（满分100分）", "人数"])
        wr_1.writerow(["90~100", str(count_1)])
        wr_1.writerow(["80~89", str(count_2)])
        wr_1.writerow(["70~79", str(count_3)])
        wr_1.writerow(["60~69", str(count_4)])
        wr_1.writerow(["50~59", str(count_5)])
        wr_1.writerow(["40~49", str(count_6)])
        wr_1.writerow(["30~39", str(count_7)])
        wr_1.writerow(["20~29", str(count_8)])
        wr_1.writerow(["10~19", str(count_9)])
        wr_1.writerow(["0~9", str(count_10)])
        wr_1.writerow(["总计", str(count)])

    print(f"{name[j]}的情感分析完成")
    print("==============分割线============")

