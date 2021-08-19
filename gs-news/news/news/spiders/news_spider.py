import scrapy


class NewsSpider(scrapy.Spider):
    name = 'news'
    start_urls = ['http://www.gansudaily.com.cn/']

    def parse(self, response):
        for item in response.css('div.conter.margin-top-10 ul li'):
            text= item.css('a::text').get(default='not-found')
            url = item.css('a::attr(href)').get(default='not-found')
            # yield {
            #     'text': text,
            #     'url': url,
            # }
            yield scrapy.Request(url, callback=self.parse_content)

    def parse_content(self, response):
        content = response.xpath(
            '//div[@class="artical"]/div[@class="a-container"]//text()').extract()
        yield {'content': content}
