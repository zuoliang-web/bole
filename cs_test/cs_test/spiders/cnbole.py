# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
from scrapy.http import Request
import json
from cs_test.items import ArticleItem

class CnboleSpider(scrapy.Spider):
    name = 'cnbole'
    allowed_domains = ['news.cnblogs.com']
    start_urls = ['http://news.cnblogs.com/']

    def parse(self, response):

        #获取所有文章的url
        # all_url = response.xpath("//div[@id='sideleft']/div[@id='news_list']//h2[@class='news_entry']/a/@href").extract()
        all_url = response.xpath("//div[@id='sideleft']/div[@id='news_list']//div[@class='content']")
        for url in all_url:
            image_url = url.xpath("//div[@class='entry_summary']/a/img/@src").extract_first("")
            url = url.xpath("//h2[@class='news_entry']/a/@href").extract_first("")
            title_url = parse.urljoin(response.url,url)  #response.url 当前主域名的url
            yield Request(url=title_url, meta={'from_image_url':image_url},callback=self.parse_detail)


        # 获取下一页的url，并交给scrapy进行下载
        next_urls = response.xpath("//div[@class='pager']/a[contains(text(),'Next >')]/@href").extract()[0]
        if next_urls:
            next_url = parse.urljoin(response.url, next_urls)
            yield Request(url=next_url, callback=self.parse)




    def parse_detail(self,response):
        article_item = ArticleItem()

        # 获取具体文章的url，并进行具体字段的解析
        image_url = response.meta.get("from_image_url", "")  #封面图片
        title = response.xpath("//div[@id ='sideleft']//div[@id='news_title']/a/text()").extract()
        create_time = response.xpath("//div[@id='news_main']/div[@id='news_info']/span[@class='time']/text()").extract()
        author = response.xpath("//div[@id='news_main']/div[@id='news_info']/span[@class='news_poster']/text()").extract()
        target = response.xpath("//div[@id='news_more_info']/input/@value").extract()

        # 获取点赞数，评论数、阅读数
        ajax_mainurl = 'https://news.cnblogs.com/NewsAjax/GetAjaxNewsInfo?contentId='
        str_num = response.url
        ajax_id = str_num.split('/')[-2]
        ajax_url = ajax_mainurl + str(ajax_id)
        article_item['title_name'] = title
        article_item['creat_time'] = create_time
        article_item['author'] = author
        article_item['target'] = target
        article_item['image_url'] = image_url
        yield Request(url=ajax_url, callback=self.parse_page_detail)
        print("能不能过来")
        # yield article_item


    def parse_page_detail(self,response):
        json_list = json.loads(response.body)
        if json_list:
            read_num = json_list['TotalView']           #阅读数
            praise_num = json_list['DiggCount']         #推荐数
            comment_num = json_list['CommentCount']     #评论数
            burry_num = json_list['BuryCount']          #反对数
        # article_item['read_num'] = read_num
        # article_item['raise_num'] = raise_num
        # article_item['comment_num'] = title
        # article_item['burry_num'] = title



