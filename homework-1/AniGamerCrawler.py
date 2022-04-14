from urllib.parse import urlparse, parse_qs
import json

import scrapy

from DanmuItem import DanmuItem

PAGE_PATTERN = 'a[href*=page]::text'
SN_PATTERN = '.animate-theme-list a[href*=sn]::attr("href")'
EPISODE_PATTERN = '.season a[href*=sn]::attr("href")'
TITLE_PATTERN = '.anime_name h1::text'

def _parse_url_sn(url):
    parsed_url = urlparse(url)
    sn = parse_qs(parsed_url.query)['sn'][0]

    return sn

class AniGamerCrawler(scrapy.Spider):
    name = 'ani_gamer'

    max_page = 100
    count = 0
    info = {}

    def start_requests(self):
        current_page = 1
        while current_page <= self.max_page:
            yield scrapy.Request(f'https://ani.gamer.com.tw/animeList.php?page={current_page}&c=All&sort=1', self.parse_anima)

            current_page += 1

    def parse_anima(self, response):
        self.max_page = min(self.max_page, max(*map(lambda x: int(x.root), response.css(PAGE_PATTERN))))

        for link in response.css(SN_PATTERN):
            parsed_url = urlparse(link.root)
            sn = parse_qs(parsed_url.query)['sn'][0]
            yield scrapy.Request(f'https://ani.gamer.com.tw/animeRef.php?sn={sn}', callback=self.parse_episode, meta={'sn': sn})

    def parse_episode(self, response):
        self.info[response.meta['sn']] = {_parse_url_sn(response.url)}
        for link in response.css(EPISODE_PATTERN):
            sn = _parse_url_sn(link.root)
            self.info[response.meta['sn']].add(sn)

        for sn in self.info[response.meta['sn']]:
            yield scrapy.Request('https://ani.gamer.com.tw/ajax/danmuGet.php', callback=self.parse_danmu, method='POST', headers={
                'Content-Type': 'application/x-www-form-urlencoded',
            }, body=f'sn={sn}', meta={'title': response.css(TITLE_PATTERN)[0].root})


    def parse_danmu(self, response):
        AniGamerCrawler.count += 1
        danmus = response.json()
        for danmu in danmus:
            item = DanmuItem(
                    color=danmu.get('color', None),
                    position=danmu.get('position', None),
                    size=danmu.get('size', None),
                    sn=danmu.get('sn', None),
                    text=danmu.get('text', None),
                    time=danmu.get('time', None),
                    userid=danmu.get('userid', None),
                    title=response.meta.get('title', None),
                )
            yield item





if __name__ == '__main__':
    pass