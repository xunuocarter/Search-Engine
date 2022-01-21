import logging
import re
from urllib.parse import urlparse
from corpus import Corpus

logger = logging.getLogger(__name__)

class Crawler:
    

    def __init__(self, frontier):
        self.frontier = frontier
        self.corpus = Corpus()

    def start_crawling(self):
        
        while self.frontier.has_next_url():
            url = self.frontier.get_next_url()
            logger.info("Fetching URL %s ... Fetched: %s, Queue size: %s", url, self.frontier.fetched, len(self.frontier))
            url_data = self.fetch_url(url)

            for next_link in self.extract_next_links(url_data):
                if self.corpus.get_file_name(next_link) is not None:
                    if self.is_valid(next_link):
                        self.frontier.add_url(next_link)

    def fetch_url(self, url):
        
        url_data = {
            "url": url,
            "content": None,
            "size": 0
        }
        return url_data

    def extract_next_links(self, url_data):
        
        outputLinks = []
        return outputLinks

    def is_valid(self, url):
        
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
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

