import scrapy


class ToubanSpider(scrapy.Spider):
    name = 'touban'
    start_urls = ['https://book.douban.com/tag/?view=type']

    def parse(self, response):
        for item in response.xpath('//*[@id="content"]/div/div[1]/div[2]'):

            tagName = item.xpath(
                '//div/table[@class="tagCol"]//tr//a//text()').extract()
            # tagUrl = item.xpath(
            #     '//div/table[@class="tagCol"]//tr//a/@href').extract()

            titles = item.xpath('//div/a/h2//text()').getall()
            tagTitle = []
            for title in titles:
                tagTitle.append(title.replace(' · · · · · · ', ''))

            # yield scrapy.Request(url, callback=self.parse_content)

            yield {
                "tagTitle": tagTitle, "tagName": tagName
            }
