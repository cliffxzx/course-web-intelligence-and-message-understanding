import scrapy

class DanmuItem(scrapy.Item):
    color = scrapy.Field() # "#FF0026"
    position = scrapy.Field() # 0
    size = scrapy.Field() # 2
    sn = scrapy.Field() # 24675554
    text = scrapy.Field() # "17:20 不用謝了"
    time = scrapy.Field() # 0
    userid = scrapy.Field() # "ChrisKuo646"
    title = scrapy.Field()
    episode = scrapy.Field()