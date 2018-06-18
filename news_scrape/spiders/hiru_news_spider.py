import scrapy

class NewsSpider(scrapy.Spider):
    name = "hiru"
    start_urls = [
        'http://www.hirunews.lk/all-news.php?pageID=1',
        'http://www.hirunews.lk/sports/all-sports-news.php?pageID=1',
        'http://www.hirunews.lk/business/all-business-news.php?pageID=1',
        'http://www.hirunews.lk/entertainment/all-entertainment-news.php?pageID=1',
        'http://www.hirunews.lk/international-news.php?pageID=1',
    ]

    def parse(self, response):
        for i in range(len(response.css('div.middle-box div.rp-ltsbx div.rp-mian div.lts-cntp a::text').extract())):
            title = response.css('div.middle-box div.rp-ltsbx div.rp-mian div.lts-cntp a::text')[i].extract()
            date = response.css('div.middle-box div.rp-ltsbx div.rp-mian div.time::text')[i].extract()
            date = date.split(',')[1].strip().split(' ')
            date = date[0]+" "+date[1]+", "+date[2]
            category = response.url.split('/')[3]
            if("international" in category):
                category = "international"
            elif("all" in category):
                category = "local"
            yield {
                'text': title,
                'date': date,
                'category': category

            }

        current_page_number = int(response.css('div.pagi div.pagi_2 b::text').extract_first())
        next_page = response.url[:-1]+str((current_page_number+1))
        if(current_page_number<5):
            yield scrapy.Request(next_page, callback=self.parse)