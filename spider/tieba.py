#coding:utf-8

import urllib2
import urllib

def tieba_spider(title,start,end):
    """爬虫"""
    title = {"kw":title}
    title = urllib.urlencode(title)
    for each in range(start,end+1):
        page = (each-1)*50
        url = "http://tieba.baidu.com/f?" + str(title) + "&pn=" + str(page)
        html = load_page(url,each)
        write_file(html,each)
    print "all already done!"

def load_page(url,page):
    """加载页面"""
    print "start download the " + str(page) + " page!"
    header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
    request = urllib2.Request(url,headers = header)
    response = urllib2.urlopen(request)
    data = response.read()
    return data

def write_file(html,page):
    """保存文件"""
    print "start save the " + str(page) + " page!"
    filename = "第" + str(page) + "页.html"
    file = open(filename,"w")
    file.write(html)
    file.close()

def main():
    """主函数"""
    title = raw_input("Please input the name of Tieba:")
    start_page = int(raw_input("The page you want start:"))
    end_page = int(raw_input("The page that you want end:"))
    tieba_spider(title,start_page,end_page)

if __name__ == "__main__":
    main()
