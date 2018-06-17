import scrapy

class NewsSpider(scrapy.Spider):
    name = "news"
    start_urls = [
        'https://www.newsfirst.lk/category/local/',
        'http://www.ft.lk/news/56/',
        'http://www.hirunews.lk/sports/all-sports-news.php?pageID=1',
    ]

    def parse(self, response):
        if("www.newsfirst.lk" in response.url):
            titles = response.css('div.sub-1-news-block::attr(data-page-short-title)').extract()
            dates = response.css('div.sub-1-news-block::attr(data-post-date)').extract()
            for i in range(len(titles)):
                yield {
                    'text': titles[i],
                    'date': dates[i],
                    'source': 'News First',
                    'category': 'Local'
                }

            # for news in response.css('div.panel-heading'):
            #     yield {
            #         'text': news.css('h3.w-400::text').extract_first()
            #     }
            current_page_number = int(response.css('div.col-xs-12').css('li.active').css('span::text').extract_first())
            if(current_page_number==1):
                next_page = response.url+"page/"+str((current_page_number+1))+"/"
            else:
                next_page = response.url[:-2]+str((current_page_number+1))
            if(current_page_number<5):
                yield scrapy.Request(next_page, callback=self.parse)

        elif("www.ft.lk" in response.url):
            for i in range(len(response.css('div.col-md-7 p span::text').extract())):
                title = response.css('div.col-md-7 a h1::text')[i].extract()
                date = response.css('div.col-md-7 p span::text')[0].extract()
                date = date.split(',')[1].strip().split(' ')
                date = date[0]+" "+date[1]+", "+date[2]
                yield {
                    'text': title,
                    'date': date,
                    'source': 'DailyFT',
                    'category': 'Local'
                }

            current_page_number = int(response.css('div.page-nation li.active span::text').extract_first())

            if(current_page_number==1):
                next_page_number = (current_page_number+2)*10
                next_page = response.url + str(next_page_number)
            else:
                next_page_number = int(response.url[-2:])+30
                next_page = response.url[:-2]+str(next_page_number)
            if(current_page_number<5):
                yield scrapy.Request(next_page, callback=self.parse)

        elif("www.hirunews.lk" in response.url):
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