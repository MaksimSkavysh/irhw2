# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class WikipediaPipeline(object):
    limit = 0

    def process_item(self, item, spider):
        self.limit = self.limit + 1
        print()
        return item
