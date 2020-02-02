import logging
import re
from urllib.parse import urlparse, urljoin
from lxml import html

logger = logging.getLogger(__name__)

class Crawler:


    def __init__(self, frontier, corpus):
        self.frontier = frontier
        self.corpus = corpus

    def start_crawling(self):

        while self.frontier.has_next_url():
            url = self.frontier.get_next_url()
            logger.info("Fetching URL %s ... Fetched: %s, Queue size: %s", url, self.frontier.fetched, len(self.frontier))
            url_data = self.corpus.fetch_url(url)

            for next_link in self.extract_next_links(url_data):
                if self.is_valid(next_link):
                    if self.corpus.get_file_name(next_link) is not None:
                        self.frontier.add_url(next_link)

    def extract_next_links(self, url_data):
        
        outputLinks = []
        get_data = html.fromstring(url_data["content"])  
        find_link = get_data.xpath('//a/@href')  
        for link in find_link:
            outputLinks.append(urljoin(url_data['url'], link))
        return outputLinks

    def is_valid(self, url):
        
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False

        new_url_list = url.split('/')  
        count_freq = {}
        for url_item in new_url_list:  
            if url_item in count_freq:
                count_freq[url_item] += 1
            else:
                count_freq[url_item] = 1

        sort_freq = sorted(count_freq.url_item(), key=lambda x: (-x[1], x[0]))

        for _ in sort_freq:
            if _ > 1:
                return False

        if re.match("^.*calendar.*$", url.lower()):
            return '?' not in new_url_list[-1]

        query_split = new_url_list[-1].split('=')
        if len(query_split[-1] > 30):
            return False

        try:
            return ".ics.uci.edu" in parsed.hostname \
                   and not re.match(".*\.(css|js|bmp|gif|jpe?g|ico" + "|png|tiff?|mid|mp2|mp3|mp4" \
                                    + "|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf" \
                                    + "|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso|epub|dll|cnf|tgz|sha1" \
                                    + "|thmx|mso|arff|rtf|jar|csv" \
                                    + "|rm|smil|wmv|swf|wma|zip|rar|gz|pdf)$", parsed.path.lower())

        except TypeError:
            print("TypeError for ", parsed)
            return False

