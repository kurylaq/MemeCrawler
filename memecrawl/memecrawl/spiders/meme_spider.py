import scrapy
import sys
from pathlib import Path

from memecrawl.items import MemecrawlItem



class MemeSpider(scrapy.Spider):
    name = "meme"

    def start_requests(self):
        self.num_memes = 5

        # urls = [
        #     'https://imgflip.com/memetemplates'
        # ]

        urls = ["https://imgflip.com/memetemplates?page=" + str(n+1) for n in range(self.num_memes)]

        print(urls)

        self.base_url = "https://imgflip.com"
        self.num_pages = 10

        for x in urls:
            yield scrapy.Request(url=x, callback=self.get_urls)
        


    def get_urls(self, response):
        url_list = response.css("h3.mt-title a::attr(href)").getall()
        for url in url_list:
            for n in range(self.num_pages):
                end = "?page=" + str((n+1))
                req_url = self.base_url + url + end
                
                yield scrapy.Request(url=req_url, callback = self.parse)

    def parse(self, response):
        url = response.request.url
        last_bit = url.split('/')[-1].split('?')

        meme_title = last_bit[0]
        # page_num = int(last_bit[1][-1])

        item = MemecrawlItem()
        image_urls = []
        # image_titles = []
        img_css_arr = response.css("img.base-img")
        

        for img_css in img_css_arr:
            img_url= img_css.css("img::attr(src)").get()
            image_urls.append("https:" + img_url)
        item['image_urls'] = image_urls
        item['image_names'] = meme_title
        return item
    
    def parse_img(self, response):
        print(response.url)

