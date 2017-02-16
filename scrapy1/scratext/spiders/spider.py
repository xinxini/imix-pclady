# -*- coding:utf-8 -*-
import scrapy
import requests
import re
from scratext.items import ScratextItem
class MySpider(scrapy.Spider):
    name='sspider'
    allowed_domains = ["dress.pclady.com.cn"]
    start_urls = ["http://dress.pclady.com.cn/stature/"]


    def parseitem(self, item):
        web = requests.get(item['url'][0])
        p0 = re.compile(r'<a.*?class="viewAll".*?href="(.*?)".*?>', re.S)
        k = re.findall(p0, web.content)
        if len(k)>0:
            url=k[0]
            web = requests.get(url)

        p1s = re.compile(r'<span style="font-family:.*?;">(.*?)</span>', re.S)
        p4 = re.compile(r'<p style="text-align: center;">.*?<img alt=".*?".*?#src="(.*?)".*?>')

        imgs = re.findall(p4, web.content)
        t=''
        for img in imgs:
            t=t+img+'*'
        imgs=[t]
        result1 = re.findall(p1s, web.content)
        p2 = re.compile(r'<br/>')
        p3 = re.compile(r'<.*?>')
        s = ""
        for results in result1:
            result = re.sub(p2, '\n', results)
            result = re.sub(p3, ' ', result)
            # f.write(result)
            s = s + result
        t = s.decode('gbk').encode('utf8')
        item['text'] = [t]
        item['img']=imgs
        return item
    def parse(self, response):

        url=response.url
        if 'stature' in url:
            items = []
            results = response.xpath('//i[@class="iPic"]')
            for result in results:
                item = ScratextItem()
                item['url'] = result.xpath('a/@href').extract()
                print '111'
                item=self.parseitem(item)
                print '333'
                items.append(item)
                yield item
            next_page = response.xpath('//div[@class="pclady_page"]/a[@class="next"]/@href')

            if next_page:
                p = re.compile(r'index_(.*?).html')
                w = re.findall(p, next_page[0].extract())
                print '444'
                if w < 2:
                    # 爬每一页
                    yield scrapy.Request(next_page[0].extract(), self.parse)

