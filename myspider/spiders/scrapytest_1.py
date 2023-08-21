import scrapy
from ..items import MyspiderItem


class NoonProductBot(scrapy.Spider):
    name = "myspider"
    # allowed_domains = ["amazon.com"]
    start_urls = ["https://www.noon.com/uae-en/electronics-and-mobiles/noon-deals-ae/?sort%5Bby%5D=popularity&sort"
                  "%5Bdir%5D=desc&gclid"
                  "=CjwKCAjwloynBhBbEiwAGY25dAMNAN7j5WGT0xRy4wivr4aZ_ejcp5cuqitfCG3DPOWzqgXGNJm9fBoCTb0QAvD_BwE"
                  "&utm_campaign=C1000035425N_ae_en_web_on_go_s_ex_cb_nbr_c1000088l_&utm_medium=cpc&utm_source"
                  "=c1000088L"]
    page_no = 2

    def parse(self, response, **kwargs):
        info = MyspiderItem()
        products = response.css('.grid , .amount')[1:]

        for product in products:
            try:
                info['name'] = product.css('.iSZeeH span::text').extract()[0]
            except:
                info['name'] = product.css('.iSZeeH span::text').extract()
            info['price'] = product.css('.amount::text').extract()

            if not info['name']:
                continue  # Skip to the next iteration of the loop
            yield info

        next_page = f'https://www.noon.com/uae-en/electronics-and-mobiles/noon-deals-ae/?limit=50&page={NoonProductBot.page_no}&searchDebug=false&sort%5Bby%5D=popularity&sort%5Bdir%5D=desc&gclid=CjwKCAjwloynBhBbEiwAGY25dAMNAN7j5WGT0xRy4wivr4aZ_ejcp5cuqitfCG3DPOWzqgXGNJm9fBoCTb0QAvD_BwE&utm_campaign=C1000035425N_ae_en_web_on_go_s_ex_cb_nbr_c1000088l_&utm_medium=cpc&utm_source=c1000088L'

        if NoonProductBot.page_no < 300:
            NoonProductBot.page_no += 1
            yield response.follow(next_page, callback=self.parse)
