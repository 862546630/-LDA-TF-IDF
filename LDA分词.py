# @Time : 2023/3/26 
# @Author : Lei Cong
# @File : LDA分词.py
# @Software : PyCharm
import csv
import re
import jieba as jb
import os


def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='gbk').readlines()]
    return stopwords


def creatfile(path):
    if not os.path.exists(path):
        os.makedirs(path)


def changecontent(file):
    file_csv = file + "/评论信息.csv"
    file_txt = file + "/contents.txt"
    with open(file_csv, "r", encoding='UTF-8') as f1, open(file_txt, 'a', encoding="utf-8") as f2:
        read = csv.reader(f1)
        for i in read:
            # print(i)
            f2.writelines((str(i[2].strip('/n'))))


# 对句子进行分词
def seg_sentence(sentence):
    sentence = re.sub(u'[0-9\.]+', u'', sentence)
    sentence_seged = jb.cut(sentence.strip())
    stopwords = stopwordslist('stopwords.txt')  # 这里加载停用词的路径
    outstr = ''
    for word in sentence_seged:
        if word not in stopwords and word.__len__() > 1:
            if word != '\t':
                outstr += word
                outstr += " "
    return outstr


if __name__ == '__main__':
    list_ = ["科沃斯", "米家", "石头", "云鲸", "美的", "海尔", "iRobot", "追觅", "360"]
    for i in list_:
        file = rf"品牌汇总/{i}/"
        file1 = rf"品牌汇总/{i}/contents.txt"
        file2 = rf"品牌汇总/{i}/contents_cut.txt"
        changecontent(file)
        inputs = open(file1, 'r', encoding='utf-8')
        outputs = open(file2, 'w', encoding='gbk')
        for line in inputs:
            line_seg = seg_sentence(line)  # 这里的返回值是字符串
            outputs.write(line_seg + '\n')
        outputs.close()
        inputs.close()
        print(rf'{i}完成')
