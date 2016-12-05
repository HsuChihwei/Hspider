#coding:utf-8
"""
 https://www.lagou.com/jobs/positionAjax.json?
 gj=3年及以下,3-5年
 &xl=本科,博士
 &jd=A轮,B轮
 &hy=移动互联网
 &px=new
 &yx=5k-10k
 &gx=全职
 &city=北京
 &district=朝阳区
"""
import urllib
import urllib2
import os
import time

def lagou_spider(job,city):
    """
    拉勾网爬虫核心程序：
    job：爬取的岗位
    city：爬去的地区
    """
    url_data = {"city":city,"kd":job}
    url_data = urllib.urlencode(url_data)
    for page in range(1,100):
        pages = {"pn":page}
        pages = urllib.urlencode(pages)
        url = "https://www.lagou.com/jobs/positionAjax.json?" + url_data + "&" + pages + "&needAddtionalResult=false"
        # data = "first=true&pn=" + str(page) + "&" + job
        print "正在下载第" + str(page) + "页！"
        page_data = load_page(url)
        print "正在保存第" + str(page) + "页！"
        save_page(page_data, page)

def load_page(url):
    """
    爬取页面信息：
    url：爬取页面的url
    data：请求提交的数据
    """
    header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
    request = urllib2.Request(url,headers=header)
    response = urllib2.urlopen(request)
    page_data = response.read()
    return page_data

def save_page(data,page):
    """
    保存爬取数据：
    data：爬取的数据
    page：爬取的页码
    """
    if os.path.isdir('./拉勾'):
        pass
    else:
        os.mkdir('./拉勾')
    filename = "./拉勾/拉勾第" + str(page) + "页.html"
    file = open(filename, "w")
    file.write(data)
    file.close()

def main():
    """
    爬虫主程序
    """
    job = raw_input("Please input the job that you want to search:")
    city = raw_input("Please input the city :")
    lagou_spider(job,city)

if __name__ == "__main__":
    main()
