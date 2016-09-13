# coding:utf8
from baike_spider import url_manager, html_downloader, html_parser, html_outputer


class SpiderMain(object):
    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownLoader()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()

    # 爬虫调度程序
    def craw(self, root_url):
        count = 1
        self.urls.add_new_url(root_url)
        while self.urls.has_new_url():
            try:
                new_url = self.urls.get_new_url()
                print 'craw %d:%s' % (count, new_url)
                html_cout = self.downloader.download(new_url)
                new_urls, new_data = self.parser.parse(new_url, html_cout)
                self.urls.add_new_urls(new_urls)
                self.outputer.collect_data(new_data)

                if count == 100:
                    break
                count += 1
            except:
                print 'craw exception'
        self.outputer.output_html()


if __name__ == "__main__":
    root_url = "http://baike.baidu.com/s?wd="
    obj_spider = SpiderMain()
    search_word = raw_input("input your search words:")
    root_url += search_word
    obj_spider.craw(root_url)
