# -*- codeing = utf-8 -*-
# @Time : 2022/7/26 17:12
# @Author : Xing
# @File : film_two.py
# @Software: PyCharm


import requests
import re
import xlwt


def main():
    baseurl = "https://www.dytt8.net/index2.htm"  # 每一个网页的url都是有规律的
    # 1.爬取网页并逐个页面解析
    data_list = getData(baseurl)
    # 2.保存数据
    sava_path = "电影天堂迅雷板块.xls"
    saveData(data_list, sava_path)


# 正则匹配
"""正则写不好，爬的东西太乱了，根本不是自己想要的"""
obj1 = re.compile(r"迅雷电影资源</a>]<a href='(?P<child_ul>.*?)'", re.S)  # 匹配子链接
obj2 = re.compile(r'<title>(?P<name>.*?)</title>.*?<a target="_blank" href="(?P<download>.*?)">', re.S)


# 爬取网页
def getData(baseurl):
    # 从页面中匹配子链接
    result1 = obj1.finditer(ask(baseurl))

    # 把拿到的子链接拼接为可以访问的url链接并存在列表里
    child_url_list = []  # 储存拿到的子链接
    for it in result1:
        url = it.group("child_ul")
        # print(url)
        # 拼接子页面链接并存到列表
        child_url = "https://www.dytt8.net" + url
        child_url_list.append(child_url)

    # 遍历访问子链接url进行数据抓取（类似有点重复操作）
    data_list = []  # 保存板块所有电影信息
    for itt in child_url_list:
        result2 = obj2.finditer(ask(itt))
        for ittt in result2:  # 不能直接用result2.group（），返回的依旧是一个对象要遍历，search可以直接group,finditer不行需要遍历
            # print(ittt.group("name"))
            # print(ittt.group("download"))
            data = []  # 保存一部电影的信息（放在上一层循环里，可能在一层用不了不互通，最好在那一层用（变动）就定义在那一层）
            data.append(ittt.group("name"))
            data.append(ittt.group("download"))
        data_list.append(data)
    # print(data_list)
    return data_list


def saveData(data_list, sava_path):
    print("save...")
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)  # 创建workbook对象
    sheet = book.add_sheet('电影天堂', cell_overwrite_ok=True)  # 创建工作表（在同一个文件下，新建的工作表：不行！）
    col = ("电影名", "磁力链接")
    for i in range(0, 2):
        sheet.write(0, i, col[i])  # 添加表的列名

    for j in range(0, 18):  # 逐条写入
        print("第%d条" % j)
        data = data_list[j]  # 从列表中逐个电影拿出来，写入表格
        for k in range(0, 2):
            sheet.write(j + 1, k, data[k])
    book.save(sava_path)  # 保存


# 访问指定的url链接并返回页面源代码
def ask(url):
    resp = requests.get(url)
    resp.encoding = "gb2312"  # requests默认utf-8解码需要改动一下
    # print(resp.text)  # 能拿到由服务器加载的页面目标代码
    return resp.text  # 返回一个网页源代码


if __name__ == "__main__":
    main()
    print("爬取完毕！")