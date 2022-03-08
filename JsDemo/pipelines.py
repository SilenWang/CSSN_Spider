# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pandas import DataFrame
import json

class JsdemoPipeline:
    
    
    def __init__(self):
        self.full = []
        self.col_map = {
            'yf001': '识别号',
            'a000': '状态',
            'a104': '发布单位',
            'a104name': '发布单位名称',
            'a100': '标准号',
            'yf100': '其他标准号',
            'a298': '中文题名(仅供参考)',
            'a301': '原文题名',
            'a826': 'ICS分类号',
            'a101': '发布日期'
        }

    def open_spider(self, spider):
        self.file = open('items.jl', 'w')
        
        
    def process_item(self, item, spider):
        self.full.extend(item['raw'])
        line = json.dumps(item['raw']) + "\n"
        self.file.write(line)
        return item

    
    def close_spider(self, spider):
        print("#########run##########")
        df = DataFrame(self.full)[self.col_map.keys()].rename(columns=self.col_map)
        df.to_csv('full.data.csv', index=0)
        self.file.close()
        
        