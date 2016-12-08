#coding:utf-8

import requests
import json
import os
import logging
from lxml import etree

# logging 配置
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='qiubai.log',
                filemode='a')

class Qiubai_spider(object):
    """
    糗百爬虫类
    """
    def __init__(self):
        """
        参数初始化:
        """
        # http://www.qiushibaike.com/8hr/page/3/  热门 （以此为例）
        # http://www.qiushibaike.com/hot/page/5/  24小时
        # http://www.qiushibaike.com/imgrank/page/5/ 热图
        # http://www.qiushibaike.com/text/page/5/  文字
        # http://www.qiushibaike.com/pic/page/5/  糗图
        # http://www.qiushibaike.com/textnew/page/5/ 新鲜
        self.url = "http://www.qiushibaike.com/8hr/page/"
        self.start = int(raw_input("请输入开始爬取的页码："))
        self.pages = int(raw_input("请输入想要爬取的页数："))

    def run(self):
        """
        糗百爬虫核心程序：
        """
        for page in range(self.start,self.start + self.pages):
            url = self.url + str(page) + "/"
            print "正在爬取第" + str(page) + "页！"
            try:
                req = self.load_page(url)
            except Exception as e:
                logging.error(e)
            print "正在清洗第" + str(page) + "页！"
            try:
                data = self.clean_data(req.text)
            except Exception as e:
                logging.error(e)
            if len(data) < 100:
                print "所有符合条件页面均爬取完毕～，共爬取" + str(page-1) + "页！"
                break
            print "正在保存第" + str(page) + "页！"
            try:
                self.write_page(data, page)
            except Exception as e:
                logging.error(e)
        print "已爬取完毕！"

    def load_page(self,url):
        """
        爬取页面：
        url:爬取的页面url
        """
        header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
        req = requests.get(url,headers = header)
        return req

    def clean_data(self,req):
        """
        数据抓取：
        req：需要清洗的数据
        """
        html = etree.HTML(req)
        result = html.xpath('//div[contains(@id,"qiushi_tag_")]')
        items = []
        for each in result:
            item = {}
            item['avatar'] = each.xpath('./div[@class="author clearfix"]//img/@src')[0]
            item['name'] = each.xpath('.//h2')[0].text
            item['content'] = each.xpath('.//div[@class="content"]/span')[0].text
            item['vote'] = each.xpath('.//i')[0].text
            item['comments'] = each.xpath('.//i')[1].text
            if each.xpath('./div[@class="thumb"]//img/@src'):
                item['images'] = each.xpath('./div[@class="thumb"]//img/@src')[0]
            items.append(item)
        data = json.dumps(items,ensure_ascii = False)
        return data

    def write_page(self, data, page):
        """
        数据存储：
        data：将要存储的数据
        page：爬取的页码
        """
        if os.path.isdir("./糗百段子"):
            pass
        else:
            os.mkdir("./糗百段子")
        file_name = "./糗百段子/第" + str(page) + "页.json"
        with open(file_name,"w") as file:
            file.write(data.encode("utf-8"))

def main():
    """
    主函数
    """
    spider = Qiubai_spider()
    spider.run()

if __name__ == "__main__":
    main()
