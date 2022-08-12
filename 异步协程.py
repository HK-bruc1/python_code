# -*- codeing = utf-8 -*-
# @Time : 2022/8/4 10:39
# @Author : Xing
# @File : 异步协程.py
# @Software: PyCharm

# 所有章节的标题和详情链接
# base_url = "https://www.yqzww.cc/book_15409/"
# 开个线程池把所有详情链接

import requests
from lxml import etree
from concurrent.futures import ThreadPoolExecutor
import time


def get_date(url):
    """
    1.同步访问:访问https://www.yqzww.cc/book_15409/ 拿到所有章节的详情链接和标题
    2.异步操作：访问各个详情链接 下载所有文章内容（有700多个章节他的请求次数是比较多的）,速度快但是无法保证下载的顺序
    3.异步还是不太会，步骤太多麻烦，还是用线程池吧
    """
    resp = requests.get(url)
    resp.encoding = "gbk"
    # print(resp.text)  #成功拿到章节主界面

    # 这里任务比较重复，而且是不断请求url的
    # 开线程池
    with ThreadPoolExecutor(100) as t:
        """可能提交的顺序是一样的，但是各个线程拿到的任务和完成的先后不一样"""
        for i in range(13, 821):
            t.submit(work, i, resp)


def work(i, resp):
    """这里拿的是每一章节的详情链接和标题都是一个任务一个链接"""
    # 提取详情链接和标题dd[13]-dd[820]
    tree = etree.HTML(resp.text)
    title = tree.xpath(f'//*[@id="list"]/dl/dd[{i}]/a/text()')[0]
    child_url = tree.xpath(f'//*[@id="list"]/dl/dd[{i}]/a/@href')[0]
    child_url = base_url + child_url
    # print(title)
    # print(child_url)
    # # 这里下载数据就不要分开了，直接获取到一个链接后直接请求详情链接下载数据
    download(child_url, title)


def download(child_url, title):
    resp = requests.get(child_url)
    tree2 = etree.HTML(resp.text)
    # 这个文本一段话为列表的一个元素先切个片把广告去除
    contents = tree2.xpath('//*[@id="content"]/text()')[1:]
    # 下载文件
    with open("novel/" + title + ".text", mode="w", encoding="utf-8") as f:
        # 对每一段话的文本进行一次符号处理后写入文件
        for content in contents:
            content = content.replace("\xa0", "")
            f.write(content + "\n")  # 一段一段的写,写完一段换一行
    print(f"{title}" + "下载完毕！")


if __name__ == '__main__':
    # 程序开始时间
    begin_time = time.time()
    base_url = "https://www.yqzww.cc/book_15409/"
    get_date(base_url)
    print("全部下载完毕！ ")
    # 程序结束时间
    end_time = time.time()
    # 运行时间run_time。round()函数取整
    run_time = round(end_time - begin_time)
    print(f"总耗时:{run_time}秒")
