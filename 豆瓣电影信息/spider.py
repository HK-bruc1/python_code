# -*- codeing = utf-8 -*-
# @Time : 2022/7/18 17:51
# @Author : Xing
# @File : spider.py
# @Software: PyCharm


from bs4 import BeautifulSoup  # 网页解析，获取数据
import re  # 正则表达式，进行文字匹配
import urllib.request,urllib.error   # 制定url，获取网页数据
import xlwt  # 进行excel操作


def main():
    baseurl = "https://movie.douban.com/top250?start="  # 每一个网页的url都是有规律的
    # 1.爬取网页并逐个页面解析
    datalist = getData(baseurl)
    # 2.保存数据
    sava_path = "豆瓣电影Top250.xls"
    saveData(datalist, sava_path)


# 影片详情链接的抽象特征（正则匹配）
# .*:贪婪匹配（匹配所有字符）  .*?:惰性匹配（匹配到了一个字符就不匹配了）
# 括号是匹配到一个后，把括号里面的东西拿出来
findLink = re.compile(r'<a href="(.*?)">')  # 创建正则表达式对象，表示规则（字符串的模式）模糊查找的抽象特征
# 影片图片
findImgSrc = re.compile(r'<img.*src="(.*?)"', re.S)  # 让换行符包含在里面
# 影片名
findTitle = re.compile(r'<span class="title">(.*)</span>')
# 评分
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
# 评价人数
findJudge = re.compile(r'<span>(\d*)人评价</span>')
# 找到概况
findInq = re.compile(r'<span class="inq">(.*)</span>')
# 找到影片的相关内容
findBd = re.compile(r'<p class="">(.*?)</p>', re.S)


# 爬取网页
def getData(baseurl):
    datalist = []
    for i in range(0, 10):  # 左闭右开，拿到250条所有页面
        url = baseurl + str(i*25)
        html = askURL(url)  # 保存获取到的网页

        # 2.逐一解析数据
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all('div', class_="item"):  # 查找符合要求的字符串形成列表,加个下划线表示属性
            data = []  # 保存一部电影的所有信息
            item = str(item)  # 转换为字符串进行进一步筛选

            link = re.findall(findLink, item)[0]  # re库用来通过正则表达式来查找指定的字符串
            data.append(link)  # 添加详情链接

            ImgSrc = re.findall(findImgSrc, item)[0]
            data.append(ImgSrc)  # 添加图片

            titles = re.findall(findTitle, item)  # 片名可能只有中文名，没有外国名
            if(len(titles) == 2):
                ctitle = titles[0]
                data.append(ctitle)
                otitle = titles[1].replace("/", "").replace("\xa0", "")  # 去掉两种无关符号
                data.append(otitle)  # 添加外国名
            else:
                data.append(titles[0])
                data.append(' ')    # 没有外国名就留空

            rating = re.findall(findRating, item)[0]
            data.append(rating)  # 添加评分

            judgeNum = re.findall(findJudge, item)[0]
            data.append(judgeNum)  # 添加评价人数

            inq = re.findall(findInq, item)
            if len(inq) != 0:
                inq = inq[0].replace("。", "")  # 去掉句号
                data.append(inq)   # 添加概述
            else:
                data.append(' ')   # 留空

            bd = re.findall(findBd, item)[0].replace("\xa0", "")  # 去掉无关符号
            bd = re.sub('<br(\s+)?/>(\s+)?', " ", bd)   # 去掉<br/>
            bd = re.sub('/', " ", bd)  # 替换/
            data.append(bd.strip())  # 去掉前后的空格

            datalist.append(data)  # 把处理好的一部电影信息放入datalist

    # print(datalist)
    return datalist

# 得到指定一个url的网页内容
def askURL(url):
    head = {  # 模拟浏览器头部信息，向豆瓣服务器发送消息
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 103.0.0.0Safari / 537.36"
    }  # 用户代理，表示告诉豆瓣服务器，我们是什么样机器，能接受什么样的信息
    request = urllib.request.Request(url, headers=head)  # 封装好的请求对象
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


# 3.保存数据
def saveData(datalist, sava_path):
    print("save...")
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)  # 创建workbook对象
    sheet = book.add_sheet('豆瓣电影250', cell_overwrite_ok=True)  # 创建工作表
    col = ("电影详情链接", "图片链接", "电影中文名", "电影外国名", "评分", "评分人数", "概述", "相关信息")
    for i in range(0, 8):
        sheet.write(0, i, col[i])  # 添加表的列名

    for j in range(0, 250):  # 逐条写入
        print("第%d条" % j)
        data = datalist[j]  # 每一个元素都是列表
        for k in range(0, 8):
            sheet.write(j+1, k, data[k])

    book.save(sava_path)  # 保存


if __name__ == "__main__":
    main()
    print("爬取完毕！")
