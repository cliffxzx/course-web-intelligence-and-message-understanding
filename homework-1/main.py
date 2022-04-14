from operator import truediv
from scrapy.crawler import CrawlerProcess

from AniGamerCrawler import AniGamerCrawler
from AniGamerPipeline import CSVPipeline

from elk import elk

ELK = False
RE_CRAWL=True
if RE_CRAWL:
    if ELK:
        elk.indices.delete(index='danmu', ignore=[400, 404])
        elk.indices.create(index='danmu', body={
            "settings": {
                "index": { "number_of_shards": 1,  "number_of_replicas": 1 }
            },
            'mappings': {
                'properties': {
                    'color': {
                        'type': 'text',
                        "fielddata": True
                    },
                    'position': {
                        'type': 'integer',
                    },
                    'size': {
                        'type': 'integer',
                    },
                    'sn': {
                        'type': 'integer',
                    },
                    'text': {
                        'type': 'text',
                        "fielddata": True,

                        # Add and search both split word by chinese
                        'analyzer': 'ik_smart',
                        'search_analyzer': 'ik_smart',
                    },
                    'time': {
                        'type': 'integer',
                    },
                    'userid': {
                        'type': 'text',
                        "fielddata": True
                        # 'analyzer': 'ik_smart',
                    },
                }
            }
        })

    common_settings = {
        # 'COMPRESSION_ENABLED': False,
        # 'HTTPCACHE_ENABLED': True,
        # 'INVANA_CRAWLER_COLLECTION': "weblinks",
        # 'INVANA_CRAWLER_EXTRACTION_COLLECTION': "weblinks_extracted_data",
        'LOG_LEVEL': 'WARN',
        'ITEM_PIPELINES': {CSVPipeline: 1},
        'CLOSESPIDER_ITEMCOUNT': 30000
        # 'HTTPCACHE_STORAGE': "webcrawler.httpcache.elasticsearch.ESCacheStorage",
    }

    process = CrawlerProcess(common_settings)
    process.crawl(AniGamerCrawler)
    process.start()



while keyword := input('請輸入要搜尋的關鍵字：'):
    try:
        result = elk.search(index='danmu',
                sort=[{ "time" : {"order" : "desc"}}],
                query={'bool': {
                    'must': {'query_string': {'query': keyword}},
                }}
            )

        print(f'Counts: {result["hits"]["total"]["value"]}', *map(lambda x: x["_source"], result["hits"]["hits"]), sep='\n')
    except:
        print('search failed')
        continue