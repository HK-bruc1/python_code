# -*- codeing = utf-8 -*-
# @Time : 2022/7/25 10:21
# @Author : Xing
# @File : spider_two.py
# @Software: PyCharm


# 拿到页面源代码  requests
# 通过re来提取想要的有效数据  re
import requests
import re
import xlwt

def main():
    baseurl = "https://movie.douban.com/top250?start="  # 每一个网页的url都是有规律的
    # 1.爬取网页并逐个页面解析
    datalist = getData(baseurl)
    # 2.保存数据
    sava_path = "豆瓣电影2Top250.xls"
    saveData(datalist, sava_path)


# 联合的正则匹配
# obj = re.compile(r'<span class="title">(?P<name>.*?)</span>', re.S)  # 拿到了很多名字，都是一样的标签（太模糊了，所有这个标签的内容都拿了）
obj = re.compile(r'<li>.*?<div class="item">.*?<span class="title">(?P<name>.*?)'
                 r'</span>.*?<p class="">.*?<br>(?P<year>.*?)&nbsp.*?'
                 r'<span class="rating_num" property="v:average">(?P<score>.*?)</span>.*?'
                 r'<span>(?P<number>.*?)人评价</span>', re.S)  # 层层向下，内容多一点匹配的越接近


# 爬取网页
def getData(baseurl):
    datalist = []  # 储存250部的电影信息
    for i in range(0, 10):  # 左闭右开，拿到250条所有页面
        url = baseurl + str(i * 25)  # 字符串凭借可比带参数好多了

        # 获取到每一个html页面逐个解析
        html = ask(url)
        # 开始匹配传过来的网页源代码
        result = obj.finditer(html)
        # print(result)  #  直接打印就是一个对象而已
        for it in result:
            # print(it.group("name"))
            # print(it.group("year").strip())  # <br>后面的空白页拿过来了，去掉一下
            # print(it.group("score"))
            # print(it.group("number"))
            # 把一部电影信息保存进列表
            data = []
            data.append(it.group("name"))
            data.append(it.group("year").strip())
            data.append(it.group("score"))
            data.append(it.group("number"))
            # print(data)  # ok可以存一部电影的信息
            datalist.append(data)  # 解析出一部电影之后保存
    # print(datalist)  # 可以显示保存的电影信息
    return datalist


# 给定一个url访问
def ask(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
    }
    resp = requests.get(url, headers=head)
    # print(resp.text) 能拿到由服务器加载的页面目标代码
    return resp.text  # 返回一个网页源代码


def saveData(datalist, sava_path):
    print("save...")
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)  # 创建workbook对象
    sheet = book.add_sheet('豆瓣电影250', cell_overwrite_ok=True)  # 创建工作表（在同一个文件下，新建的工作表：不行！）
    col = ("电影名", "年份", "豆瓣评分", "评分人数")
    for i in range(0, 4):
        sheet.write(0, i, col[i])  # 添加表的列名

    for j in range(0, 250):  # 逐条写入
        print("第%d条" % j)
        data = datalist[j]  # 从列表中逐个电影拿出来，写入表格
        for k in range(0, 4):
            sheet.write(j + 1, k, data[k])
    book.save(sava_path)  # 保存


if __name__ == "__main__":
    main()
    print("爬取完毕！")
