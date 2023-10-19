from spider.nike2 import Nike2Spider
from spider.nikeparsing import NikeparsingSpider

if __name__ == "__main__":
    spider : Nike2Spider = Nike2Spider(search_query="easy")
    productLink = spider.get_pages()
    print(len(productLink))

    parse = NikeparsingSpider(listLink=productLink)
    parse.req_page()
