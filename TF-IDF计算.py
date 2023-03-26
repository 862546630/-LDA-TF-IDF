# @Time : 2023/3/25 
# @Author : Lei Cong
# @File : TF-IDF计算.py
# @Software : PyCharm


from collections import defaultdict
import jieba
import csv
import math
import operator
import re


def stripword(stop, seg):
    stripword_list = []
    for i in seg:
        if i not in stop:
            stripword_list.append(i)
    return stripword_list


def loadDataSet(file):
    dataset = []
    with open(file, 'r', encoding='utf-8') as f:
        read_t = csv.reader(f)
        for i in read_t:
            pattern = re.compile(
                u'\t|\n|\.|-|——|：|！|、|，|,|。|;|\)|\(|\?|"|content|\ufeff|&|hellip|^|_| |')  # 建立正则表达式匹配模式
            content = re.sub(pattern, '', i[0])
            jieba.load_userdict(r"dict.txt")
            seg = list(jieba.cut(content.encode('utf-8')))
            stripword_list = stripword(stop, seg)
            dataset.append(stripword_list)
    classVec = [0, 1, 0, 1, 0, 1]  # 类别标签向量，1代表好，0代表不好
    return dataset, classVec


"""
函数说明：特征选择TF-IDF算法
Parameters:
     list_words:词列表
Returns:
     dict_feature_select:特征选择词字典
"""


def feature_select(list_words):
    # 总词频统计
    doc_frequency = defaultdict(int)
    for word_list in list_words:
        for i in word_list:
            doc_frequency[i] += 1

    # 计算每个词的TF值
    word_tf = {}  # 存储没个词的tf值
    for i in doc_frequency:
        word_tf[i] = doc_frequency[i] / sum(doc_frequency.values())

    # 计算每个词的IDF值
    doc_num = len(list_words)
    word_idf = {}  # 存储每个词的idf值
    word_doc = defaultdict(int)  # 存储包含该词的文档数
    for i in doc_frequency:
        for j in list_words:
            if i in j:
                word_doc[i] += 1
    for i in doc_frequency:
        word_idf[i] = math.log(doc_num / (word_doc[i] + 1))

    # 计算每个词的TF*IDF的值
    word_tf_idf = {}
    for i in doc_frequency:
        word_tf_idf[i] = word_tf[i] * word_idf[i]

    # 对字典按值由大到小排序
    dict_feature_select = sorted(word_tf_idf.items(), key=operator.itemgetter(1), reverse=True)
    return dict_feature_select


if __name__ == '__main__':

    """去除停用词"""
    file1 = rf"品牌爬取汇总.csv"
    path1 = r"品牌汇总"

    with open(file1, 'r', encoding="utf-8-sig") as fn:
        re0 = csv.reader(fn)
        name = []
        for i in re0:
            name.append(i[0])
    for j in range(len(name)):
        stop = [line.strip() for line in open('stopwords.txt').readlines()]
        data_list, label_list = loadDataSet(rf'品牌汇总/{name[j]}/情感倾向性详细分析结果.csv')
        features = feature_select(data_list)  # 所有词的TF-IDF值
        with open(rf"品牌汇总/{name[j]}/TF-IDF统计.csv", 'a', newline='', encoding='utf-8-sig') as f:
            wr = csv.writer(f)
            for i in features:
                print(i)
                wr.writerow([i[0], i[1]])