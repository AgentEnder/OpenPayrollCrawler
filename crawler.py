import scrapy
from scrapy.crawler import CrawlerProcess
import os

class crawler(scrapy.Spider):
    name="openPayrollCrawler"
    EMPLOYEE_ROW_CSS = "tr[itemprop='employee']"
    EMPLOYEE_NAME_CSS = "span[itemprop='name']::text"
    EMPLOYEE_NEXT_BUTTON_XPATH = '//a[@rel="next"]/@href'
    EMPLOYEE_DETAIL_BUTTON = ":last-child>a::attr(href)"
    EMPLOYEE_DETAIL_NAME = "h1>span[itemprop='name']::text"
    EMPLOYEE_DETAIL_TITLE = "span[itemprop='jobTitle']::text"
    EMPLOYEE_DETAIL_SALARY = "span[data-toggle='popover']::text"

    def __init__(self, location, file_out = "data.csv"):
        self.start_urls = [f"https://openpayrolls.com/search/employees/{location}"]
        open(file_out, 'w+').close() # Create the file, clear it if it already exists
        self.file_out = file_out
            

    def parse(self, response):
        for emp in response.css(self.EMPLOYEE_ROW_CSS):
            print(f"Parsing: {emp.css(self.EMPLOYEE_NAME_CSS).get()}")
            link = emp.css(self.EMPLOYEE_DETAIL_BUTTON).extract()[0]
            print(link)
            yield response.follow(response.urljoin(link), callback=self.parse_details)
        print("Following link")
        link = emp.xpath(self.EMPLOYEE_NEXT_BUTTON_XPATH).extract()[0]
        print(link)
        yield response.follow(response.urljoin(link), callback=self.parse)

    def parse_details(self, response):
        print("PARSING DETAILS")
        with open(self.file_out, 'a') as f:
            f.write(response.css(self.EMPLOYEE_DETAIL_NAME).get().replace(",",'&c;') + ',')
            f.write(response.css(self.EMPLOYEE_DETAIL_TITLE).get().replace(",",'&c;') + ',')
            f.write(response.css(self.EMPLOYEE_DETAIL_SALARY).get().replace(",",'') + '\n')
        
if __name__ == "__main__":
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(crawler, location="university-of-kentucky", file_out="uk_data.csv")
    process.start()