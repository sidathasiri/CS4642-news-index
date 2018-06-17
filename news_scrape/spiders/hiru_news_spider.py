import scrapy

class NewsSpider(scrapy.Spider):
    name = "hiru"
    start_urls = [
        'http://www.hirunews.lk/sports/all-sports-news.php?pageID=1',
    ]

    def parse(self, response):
        for i in range(len(response.css('div.middle-box div.rp-ltsbx div.rp-mian div.lts-cntp a::text').extract())):
            title = response.css('div.middle-box div.rp-ltsbx div.rp-mian div.lts-cntp a::text')[i].extract()
            date = date = response.css('div.middle-box div.rp-ltsbx div.rp-mian div.time::text')[0].extract()
            date = date.split(',')[1].strip().split(' ')
            date = date[0]+" "+date[1]+", "+date[2]
            yield {
                'text': title,
                'date': date,
                'source': 'Hiru News',
                'category': 'Sports'
            }

        current_page_number = int(response.css('div.pagi div.pagi_2 b::text').extract_first())
        print("currenttttttttttttttttttttttttttttttttttt", current_page_number)
        next_page = response.url[:-1]+str((current_page_number+1))
        if(current_page_number<5):
            yield scrapy.Request(next_page, callback=self.parse)