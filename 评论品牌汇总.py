# @Time : 2023/3/25 
# @Author : Lei Cong
# @File : 评论品牌汇总.py
# @Software : PyCharm


import csv
import os


def getcsv(file):
    with open(file, encoding="utf-8-sig") as f:
        re = csv.reader(f)
        dic_ = {}
        for i in re:
            dic_[i[0]] = i[1]
        return dic_


def creatfile(path):
    if not os.path.exists(path):
        os.makedirs(path)


if __name__ == '__main__':
    list_ = ["科沃斯", "米家", "石头", "云鲸", "美的", "海尔", "iRobot", "追觅", "360"]
    for i in list_:
        creatfile(rf"品牌汇总\{i}")
        with open(rf"品牌汇总\{i}\评论信息1.csv", "a", encoding="utf-8-sig",
                  newline="") as f:
            wr = csv.writer(f)
            wr.writerow(["nikename", "publishtime", "content"])
            path1 = r"京东"
            file1 = "京东爬取项目URL.csv"
            dict_ = getcsv(file1)
            name = []
            for key, value in dict_.items():
                name.append(key)
            for j in name:
                if i in j:
                    with open(rf"京东\{j}\评论信息.csv", 'r', encoding="utf-8-sig") as fn:
                        re = csv.reader(fn)
                        for line in re:
                            if "publishtime" not in list(line):
                                wr.writerow(line)

    for k in list_:
        with open(rf"品牌汇总\{k}\评论信息1.csv", "r", encoding="utf-8-sig") as f:
            re = csv.reader(f)
            with open(rf"品牌汇总\{k}\评论信息.csv", "a", encoding="utf-8-sig",
                  newline="") as f2:
                wr = csv.writer(f2)
                wr.writerow(["nikename", "publishtime", "content"])
                for i in re:
                    if "publishtime" not in list(i):
                        wr.writerow(i)
        os.remove(rf"品牌汇总\{k}\评论信息1.csv")
