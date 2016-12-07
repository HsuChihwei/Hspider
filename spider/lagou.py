#coding:utf-8

import urllib
import urllib2
import os
import time

class Spider(object):
    """
    拉勾爬虫类
    """
    def __init__(self):
        """
        参数初始化：
        """
        self.url = "https://www.lagou.com/jobs/positionAjax.json?"
        self.job = raw_input("请输入想要查找的岗位:")
        self.city = raw_input("请输入想删选的城市:")
        self.start = raw_input("请输入开始爬取的页码:")
        self.pages = raw_input("请输入想爬取的总页数:")
        if not self.city:
            self.city = '全国'
        if not self.start:
            self.start = 1
        if not self.pages:
            self.pages = 10

    def lagou_spider(self):
        """
        拉勾网爬虫核心程序：
        """
        url_data = {"city":self.city}
        job = {"kd":self.job}
        url_data = urllib.urlencode(url_data)
        url = self.url + url_data + "&needAddtionalResult=false"
        job = urllib.urlencode(job)
        for page in range(int(self.start), int(self.start) + int(self.pages)):
            data = "first=true&pn=" + str(page) + "&" + job
            print "正在下载第" + str(page) + "页！"
            time.sleep(2)
            page_data = self.load_page(url,data)
            if len(page_data) < 500:
                print "所有符合条件页面均爬取完毕～，共爬取" + str(page-1) + "页！"
                break
            print "正在保存第" + str(page) + "页！"
            self.save_page(page_data, page)
        print "已爬取完毕！"

    def load_page(self,url,data):
        """
        爬取页面信息：
        url：爬取页面的url
        data：请求提交的数据
        """
        header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
        request = urllib2.Request(url, data = data, headers=header)
        response = urllib2.urlopen(request)
        page_data = response.read()
        return page_data

    def save_page(self,data,page):
        """
        保存爬取数据：
        data：爬取的数据
        page：爬取的页码
        """
        path = "./" + self.job
        if os.path.isdir(path):
            pass
        else:
            os.mkdir(path)
        filename = path + "/" + self.job + "第" + str(page) + "页.json"
        file = open(filename, "w")
        file.write(data)
        file.close()

def main():
    """
    爬虫主程序
    """
    spider = Spider()
    spider.lagou_spider()

if __name__ == "__main__":
    main()
