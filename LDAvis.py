# @Time : 2023/3/26 
# @Author : Lei Cong
# @File : LDAvis.py
# @Software : PyCharm

from gensim import corpora
from gensim.models import LdaModel
import codecs
import pyLDAvis.gensim



def LDAvistrain(file):
    train = []
    file = file+'/contents_cut.txt'
    fp = codecs.open(file1, 'r', encoding='GBK')
    for line in fp:
        if line != '':
            line = line.split()
            train.append([w for w in line])

    dictionary = corpora.Dictionary(train)

    corpus = [dictionary.doc2bow(text) for text in train]

    lda = LdaModel(corpus=corpus, id2word=dictionary, num_topics=6, passes=60)
    # num_topics：主题数目
    # passes：训练伦次
    # num_words：每个主题下输出的term的数目

    for topic in lda.print_topics(num_words=20):
        termNumber = topic[0]
        print(topic[0], ':', sep='')
        listOfTerms = topic[1].split('+')
        for term in listOfTerms:
            listItems = term.split('*')
            print('  ', listItems[1], '(', listItems[0], ')', sep='')

    '''插入之前的代码片段'''
    d = pyLDAvis.gensim.prepare(lda, corpus, dictionary)

    '''
    lda: 计算好的话题模型

    corpus: 文档词频矩阵

    dictionary: 词语空间
    '''

    # d=pyLDAvis.gensim_models.prepare(lda, corpus, dictionary)
    pyLDAvis.show(d)
    # pyLDAvis.save_html(d, './LDAvis/lda_pass10.html')	# 将结果保存为该html文件


if __name__ == '__main__':
    list_ = ["科沃斯", "米家", "石头", "云鲸", "美的", "海尔", "iRobot", "追觅", "360"]
    for i in list_:
        file = rf"品牌汇总/{i}/"
        LDAvistrain(file)
