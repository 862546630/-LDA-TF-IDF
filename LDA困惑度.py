# @Time : 2023/3/25 
# @Author : Lei Cong
# @File : LDA困惑度.py
# @Software : PyCharm


# @Time : 2023/3/25
# @Author : Lei Cong
# @File : LDA困惑度.py
# @Software : PyCharm

import gensim
from gensim import corpora, models
import matplotlib.pyplot as plt
import matplotlib
import jieba
import re
import csv


def stripword(stop, seg):
    stripword_list = []
    for i in seg:
        if i not in stop:
            stripword_list.append(i)
    return stripword_list

##file：为所要分析评论信息的地址
def loadDataSet(file,stop):
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
    return dataset


# 计算困惑度
def perplexity(num_topics):
    ldamodel = Lda(corpus, num_topics=num_topics, id2word=dictionary, passes=50)  # passes为迭代次数，次数越多越精准
    print(ldamodel.print_topics(num_topics=num_topics, num_words=6))  # num_words为每个主题下的词语数量
    print(ldamodel.log_perplexity(corpus))
    return ldamodel.log_perplexity(corpus)

if __name__ == '__main__':
    stop = [line.strip() for line in open('stopwords.txt').readlines()]
    list_ = ["科沃斯", "米家", "石头", "云鲸", "美的", "海尔", "iRobot", "追觅", "360"]
    for i in list_:
        data_set = loadDataSet(rf'品牌汇总/{i}/情感倾向性详细分析结果.csv',stop)
        dictionary = corpora.Dictionary(data_set)  # 构建 document-term matrix
        corpus = [dictionary.doc2bow(text) for text in data_set]
        Lda = gensim.models.ldamodel.LdaModel  # 创建LDA对象

        # 绘制困惑度折线图
        x = range(1, 12)  # 主题范围数量
        y = [perplexity(i) for i in x]
        plt.plot(x, y)
        plt.xlabel('主题数目')
        plt.ylabel('困惑度大小')
        plt.rcParams['font.sans-serif'] = ['SimHei']
        matplotlib.rcParams['axes.unicode_minus'] = False
        plt.title('主题-困惑度变化情况')
        plt.savefig(rf'品牌汇总/{i}/困惑度.jpg')
        # plt.show()



