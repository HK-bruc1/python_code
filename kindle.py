# -*- codeing = utf-8 -*-
# @Time : 2022/8/9 16:44
# @Author : Xing
# @File : kindle.py
# @Software: PyCharm
import xlwt
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import time


# 创建浏览器对象
web = Chrome()
# 用一个列表保存一个页面所有漫画信息
all_list = []
# 保存路径
sava_path = "豆瓣电影2Top250.xls"
# 设置开始写数据的行数(从第一行开始，第零行已经写了)
j = 1


def base_page():
    """进入到第一个主页面，爬完所有列表后切回视角进入到第二个主页面"""
    # 打开一个网址
    web.get("https://kindle.smgzd.com/")
    time.sleep(1)
    # 登录知道漫画
    web.find_element(By.XPATH, '//*[@id="ls_username"]').send_keys('319334854@qq.co')
    web.find_element(By.XPATH, '//*[@id="ls_password"]').send_keys('20171410618good')
    web.find_element(By.XPATH, '//*[@id="lsform"]/div/div/table/tbody/tr[2]/td[3]/button').click()
    time.sleep(1)
    # 进入耽美漫画板块(标签有超链接(会开一个新窗口)，先获取再访问)click有时候不管用
    a = web.find_element(By.XPATH, '//*[@id="thread_types"]/li[18]/a')
    url = a.get_attribute("href")
    web.get(url)
    time.sleep(1)


def base_work(num):
    """num为爬取漫画的编号，一个漫画爬取的任务（拿名字和链接以及密码）,用列表返回数据"""
    # 用列表存放一个漫画的信息
    baidu_list = []
    # 进入漫画的详情页面
    a = web.find_element(By.XPATH, f'//*[@id="threadlisttableid"]/tbody[{num}]/tr[1]/th[1]/a[2]')
    url = a.get_attribute("href")
    # web.get(url)  这种不会打开新窗口
    js = f'window.open("{url}")'
    web.execute_script(js)
    # 加载新窗口要等待，慢一点，免得报错
    time.sleep(5)
    # 切换到详情窗口
    web.switch_to.window(web.window_handles[-1])
    # 点击回复
    web.find_element(By.XPATH, '//*[@class="locked"]/a').click()
    time.sleep(1)
    # 输入回复内容并发送(先点击一下在输入)
    web.find_element(By.XPATH, '//*[@id="postmessage"]').click()
    web.find_element(By.XPATH, '//*[@id="postmessage"]').send_keys("来了来了来了兄弟们！")
    web.find_element(By.XPATH, '//*[@id="postsubmit"]').click()
    time.sleep(2)

    # 拿漫画id编号，用id直接定位链接位置
    kindle_id = web.find_element(By.XPATH, '//*[@id="postlist"]/div[1]').get_attribute("id")
    kindle_id = kindle_id.split("_")[1]
    title = web.find_element(By.XPATH, '//*[@id="thread_subject"]').text
    baidu = web.find_element(By.XPATH, f'//*[@id="postmessage_{kindle_id}"]/div').text
    # 数据处理（字符串截取,删除空白,去掉换行）
    baidu = baidu.strip("本帖隐藏的内容").strip("复制这段内容后打开百度网盘手机App，操作更方便哦").replace('\n', "").strip()
    # 拿一个存一个
    baidu_list.append(title)
    baidu_list.append(baidu)
    # 声明改变的是全局变量，引用不需要关键字
    global j
    save_data(baidu_list, sava_path, j)
    print(f"第{j}条保存成功!")
    j += 1
    # 关闭子页面，视角切换到主页面
    web.close()
    web.switch_to.window(web.window_handles[0])


def save_data(datalist, path, row):
    """j从哪一行开始写入"""
    """保存一个漫画"""
    col = ("漫画名字", "百度云")
    for r in range(0, 2):
        sheet.write(0, r, col[r])  # 添加表的列名
    for k in range(0, 2):
        sheet.write(row, k, datalist[k])
    book.save(path)  # 保存

def main_work():
    # 计算一下这个页面漫画的数量
    tbody_list = web.find_elements(By.XPATH, f'//*[@id="threadlisttableid"]/tbody')
    # 循环遍历一个页面所有漫画 (从3开始)
    for i in range(7, len(tbody_list)+1):
        base_work(i)
        print("等待60秒...")
        # 论坛有发言时间限制，就不能用多线程（进程）异步完成，也可以直接点击所有子页面，但是还是要等，无所谓
        time.sleep(60)
    # 当前页面爬取完之后，点击下一页(href属性是javascript不能直接点击)
    a = web.find_element(By.XPATH, '//*[@id="autopbn"]')
    web.execute_script("arguments[0].click()", a)


if __name__ == '__main__':
    # 创建表格
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)  # 创建workbook对象
    sheet = book.add_sheet('漫画', cell_overwrite_ok=True)  # 创建工作表

    # 登录进入主页面，进入格斗板块
    base_page()
    # 爬取完所有页面
    status = True
    # 从板块的第二页开始
    count = 1
    while status:
        main_work()
        if(count == 1):
            status = False
        else:
            count += 1




