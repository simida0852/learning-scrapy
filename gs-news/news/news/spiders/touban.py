import scrapy


class ToubanSpider(scrapy.Spider):
    name = 'touban'
    start_urls = ['https://book.douban.com/tag/?view=type']
    global base_url
    base_url = 'https://book.douban.com'

    def parse(self, response):
        for item in response.xpath('//*[@id="content"]/div/div[1]/div[2]'):
            tagNames = item.xpath(
                '//div/table[@class="tagCol"]//tr//a//text()').extract()
            tagUrls = item.xpath(
                '//div/table[@class="tagCol"]//tr//a/@href').extract()

            for tagUrl in tagUrls:
                yield scrapy.Request(base_url + tagUrl, callback=self.parse_book_list)

    def parse_book_list(self, response):
        for list_item in response.css('div#content div#subject_list ul.subject-list li.subject-item'):

            bookSummary = list_item.css('div.info p::text').extract()

            bookUrl = list_item.css('div.info h2 a::attr(href)').extract()

            for name in list_item.css('div.info h2 a::text').extract():
                if(name):
                    bookName = name.strip()

            for pub in list_item.css('div.info div.pub::text').extract():
                if(pub):
                    bookPub = pub.strip()

            for rating in list_item.css('div.info div.star span.rating_nums::text').extract():
                if(rating):
                    bookRatingNums = rating.strip()

            for pl in list_item.css('div.info div.star span.pl::text').extract():
                if(pl):
                    bookPl = pl.strip()
            yield{
                'bookName': bookName,
                'bookPub': bookPub,
                'bookRatingNums': bookRatingNums,
                'bookPl': bookPl,
                'bookSummary': bookSummary,
                'bookUrl': bookUrl,
            }

        next_page = response.css('div.paginator span.next a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            print('=>'*10, next_page)
            yield scrapy.Request(base_url + next_page, callback=self.parse_book_list)
