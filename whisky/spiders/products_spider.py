from scrapy import Spider
from scrapy.http.request import Request
from ..items import WhiskyItem

class products_spider(Spider):
    name = 'products_spider'
    start_urls = [
        'https://www.whisky.de/shop/'
    ]

    def parse(self, response, check_urls = True):

        # This is for not trying to scroll on scrolled pages
        if ("?" in response.url):
            check_urls = False

        # Getting list of products from html reponse
        items = self.parse_products(response)
        for item in items:
            yield item

        # Checking for next page
        if (check_urls):

            # Getting categories from left navigation panel
            urls = self.parse_urls(response)
            for url in urls:
                yield Request(url = url, callback = self.parse)

            # Scrolling on current page for all products
            url_scroll = self.parse_url_scroll(response)
            for url in url_scroll:
                yield Request(url = url, callback = self.parse)

    def parse_url_scroll(self, response):
        # Getting scroll url for page
        next_page = response.xpath('//ol[@class="pagination lineBox pull-right"]/li[not(@class)]/a/@href').extract()

        if (next_page == None):
            return []
        return next_page

    def parse_urls(self, response):
        # Getting list of urls to scrape next
        nav = response.xpath('//div[@id="sidebar-left"]//ul//a/@href').extract()
        urls = []

        for url in nav:
            new_url = url
            if ('?' in new_url): new_url = url.split('?')[0]
            urls.append(new_url)

        return urls


    def parse_products(self, reponse):
        # extracting all products from page
        products = reponse.css(".panel-body")

        items = []

        for product in products:
            item = WhiskyItem()

            image_src = product.xpath('.//div[@class="article-left article-thumbnail"]/a/img/@data-src').extract_first()

            title = product.xpath('.//div[@class="article-title"]/a/text()').extract_first()

            attributes = product.xpath('.//div[@class="article-attributes"]//li')
            if (attributes != None):
                attributes = self.parse_attributes(attributes)

            description = product.xpath('.//div[@class="article-description-short"]/div/text()').extract_first()

            amount = product.xpath('.//div[@class="article-amount"]/span[1]/text()').extract_first()

            alcohol = product.xpath('.//div[@class="article-amount"]/span[2]/text()').extract_first()

            price = product.xpath('.//span[@class="article-price-default article-club-hidden"]/text()').extract_first()
            if (price != None):
                price = price.rstrip().strip()

            dilivery = product.xpath('.//div[@class="article-delivery-info"]/span/text()').extract_first()

            stock = product.xpath('.//div[starts-with(@class, "article-stock")]/span/text()').extract_first()
            if (stock != None):
                stock = stock.rstrip().strip()

            company = product.xpath('.//div[@class="article-company"]/text()').extract_first()
            if (company != None):
                company = company.rstrip().strip()

            item["title"] = title
            item["attributes"] = attributes
            item["description"] = description
            item["amount"] = amount
            item["alcohol"] = alcohol
            item["price"] = price
            item["dilivery"] = dilivery
            item["stock"] = stock
            item["company"] = company
            item["image_src"] = image_src

            items.append(item)

        return items

    def parse_attributes(self, attributes):
        # Since there can be any number of attributes, need to put them in a list
        attrib = {}
        for attribute in attributes:
            key = attribute.xpath('./strong/text()').extract_first()
            value = attribute.xpath('./span/text()').extract_first()

            attrib[key] = value

        return attrib
