import scrapy

class NewsSpider(scrapy.Spider):
    name = "dailyft"
    start_urls = [
        'http://www.ft.lk/news/56/',
    ]

    def parse(self, response):
        global newsList
        for i in range(len(response.css('div.col-md-7 p span::text').extract())):
            title = response.css('div.col-md-7 a h1::text')[i].extract()
            date = response.css('div.col-md-7 p span::text')[0].extract()
            date = date.split(',')[1].strip().split(' ')
            date = date[0]+" "+date[1]+", "+date[2]
            yield {
                'text': title,
                'date': date
            }

        current_page_number = int(response.css('div.page-nation li.active span::text').extract_first())

        if(current_page_number==1):
            next_page_number = (current_page_number+2)*10
            next_page = response.url + str(next_page_number)
        else:
            next_page_number = int(response.url[-2:])+30
            next_page = response.url[:-2]+str(next_page_number)
        if(current_page_number<10):
            yield scrapy.Request(next_page, callback=self.parse)