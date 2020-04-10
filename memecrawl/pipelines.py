# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.python import to_bytes
from scrapy import Request
import hashlib
import os

class MemecrawlPipeline(ImagesPipeline):
    def process_item(self, item, spider):
        with open("files.txt", "a") as text_file:
            urls = item["image_urls"]
            for url in urls:
                hash = hashlib.sha1(to_bytes(url)).hexdigest()
                meme = item["image_names"]
                text_file.write(hash + "," + meme + "\n")
        return item

    def file_path(self, request, response=None, info=None):
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return 'full/%s.jpg' % (image_guid)