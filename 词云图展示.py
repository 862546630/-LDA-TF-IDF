# @Time : 2023/3/25 
# @Author : Lei Cong
# @File : 词云图展示.py
# @Software : PyCharm

"""导入相关库"""
import jieba
import PIL.Image
import pandas as pd
import numpy as np
from wordcloud import WordCloud
from matplotlib import pyplot as plt
import csv
import re

file1 = rf"品牌爬取汇总.csv"

with open(file1, "r", encoding="utf-8-sig") as fn:
    re1 = csv.reader(fn)
    name = []
    for i in re1:
        name.append(i[0])
for j in range(len(name)):
    file = r"品牌汇总\\" + str(name[j]) + "\评论信息.csv"
    odata = pd.read_csv(file, encoding='UTF-8', engine='python')
    content = odata['content'].drop_duplicates()  # 去重
    delete = re.compile('[0-9a-zA-Z]|\n|\t|#|京东|云鲸|科沃|机器人|360|扫地机器人|噪音大小|吸力大小|华为|智能程度|灵敏程度|越障能力|小米|斯沃特|此用户未填写评价内容| |')
    content = content.apply(lambda x: delete.sub('', x))
    # print(content)

    jieba.load_userdict(r"dict.txt")  # 安装字典
    data_cut = [jieba.lcut(x) for x in content]  # 分词后结果，形式为二维列表（里面是列表）
    # data_cut

    """读取停用词文档"""
    with open(r"stopwords.txt", 'r') as f:
        stop = f.read()
    stop = stop.split()
    stop = [' '] + stop
    # stop
    data_after = [[j for j in i if j not in stop] for i in data_cut]  # 判断是否为停用词
    # data_after #二维列表

    """统计词频"""
    all_words = []
    for i in data_after:
        all_words.extend(i)
    # all_words #一维列表
    # # all_words.count('不错')  #计算词频

    # 去除单个字的词
    for i in range(len(all_words) - 1, -1, -1):
        if (len(all_words[i]) < 2):
            all_words.pop(i)

    num = pd.Series(all_words).value_counts()  # 统计词频
    # print(num)

    """词云参数"""
    wc = WordCloud(background_color='white', font_path='‪C:\\Windows\\Fonts\\simkai.ttf',
                   max_words=1000,
                   max_font_size=48, width=500, height=500)
    wc2 = wc.fit_words(num)  # 词频传入

    """词云展示"""
    plt.figure(figsize=(10, 10))  # 图片的大小
    plt.imshow(wc2)
    plt.axis('off')  # 关闭坐标
    # plt.show()
    wc.to_file(r"品牌汇总\\" + str(name[j]) + "\词云图.png")  # 保存图片
    print("第{}个词云图保存成功".format(j + 1))
