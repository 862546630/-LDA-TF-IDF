import json
import time
import random
import requests
import pandas as pd
from tqdm import tqdm
import csv

# 请求头部信息

agent1 = "Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; BLA-AL00 Build/HUAWEIBLA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/8.9 Mobile Safari/537.36"
agent2 = "Mozilla/5.0 (Linux; Android 8.1; PAR-AL00 Build/HUAWEIPAR-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044304 Mobile Safari/537.36 MicroMessenger/6.7.3.1360(0x26070333) NetType/WIFI Language/zh_CN Process/tools"
agent3 = "Mozilla/5.0 (Windows NT 6.1; rv,2.0.1) Gecko/20100101 Firefox/4.0.1"
agent4 = "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)"
agent5 = "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"
list1 = [agent1, agent2, agent3, agent4, agent5]

https1 = "https://139.196.112.90:8080"
https2 = "https://183.173.144.193:10080"
https3 = "https://118.184.179.6:8001"
https4 = "https://1.12.224.175:8888"
https5 = "https://103.166.110.254:83"
list2 = [https1, https2, https3, https4, https5]

def getcsv(file):
    with open(file, encoding="utf-8-sig") as f:
        re = csv.reader(f)
        dic_ = {}
        for i in re:
            dic_[i[0]] = i[1]
        return dic_


if __name__ == '__main__':
    name = []
    naurl = []
    file1 ="京东爬取项目URL.csv"
    dict_ = getcsv(file1)
    for key, value in dict_.items():
        name.append(key)
        naurl.append(value)
    for k in range(len(name)):
        all_content = []
        content_url = []  # 建立空列表，用来存放网页链接
        n = 100
        for i in range(0, n):
            url = str(naurl[k]) + str(i) + '&pageSize=10&isShadowSku=0&fold=1'
            content_url.append(url)
        print(f"正在爬取{name[k]}的评论内容")
        """爬取内容"""
        all_content = pd.DataFrame()  # 建立数据框，用来存放爬取的内容
        for j in tqdm(range(0, n)):
            # print("正在爬取第{}页的内容".format(j))
            agent = random.choice(list1)
            ip = random.choice(list2)
            headers = {"referer": "https://item.jd.com/",
                       "user-agent": agent}
            proxy = {"https": ip}
            response = requests.get(content_url[j], headers=headers)  # 请求网页内容
            html = str(response.text)  # 网页内容转化成字符串
            html = html.replace("fetchJSON_comment98(", "")
            html = html[:-2]  # 以上两步转化成标准的JSON格式
            data = json.loads(html)  # 标准的JSON格式转化为python中的字典类型
            productColor = [x['productColor'] for x in data['comments']]
            nickname = [x['nickname'] for x in data['comments']]  # 列表推导式提取昵称
            content = [x['content'] for x in data['comments']]  # 列表推导式提取评论内容
            creationTime = [x['creationTime'] for x in data['comments']]  # 列表推导式提取时间
            all_content = all_content.append(
                pd.DataFrame({'nickname': nickname, 'publishtime': creationTime, 'content': content}))  # 获取的内容存入数据框中
            time.sleep(random.randint(1, 2))  # 暂缓1~2之间的随机数秒
        print(f'{name[k]}的评论信息爬取完成')
        """保存文件"""

        file2 = rf"评论数据\京东\{name[k]}\评论信息.csv"
        all_content.to_csv(file2, index=False, encoding="UTF-8-sig")