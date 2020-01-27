import logging
import re
from urllib.parse import urlparse, urljoin
from corpus import Corpus
from lxml import html
import os
from collections import defaultdict

logger = logging.getLogger(__name__)


class Crawler:
    

    def __init__(self, frontier):
        self.frontier = frontier
        self.corpus = Corpus()
        self.subdomain = defaultdict(int)
        self.out_link = defaultdict(int)
        self.valid_list = []
        self.invalid_list = []

    def start_crawling(self):
        """
        This method starts the crawling process which is scraping urls from the next available link in frontier and adding
        the scraped links to the frontier
        """
        analytic_file = open("Analytic.txt", "w")
        valid_file = open("valid_url.txt", "w")
        invalid_file = open("invalid_url.txt", "w")

        while self.frontier.has_next_url():
            
            
            url = self.frontier.get_next_url()
            #if any(url[5:] in s for s in self.valid_list): #or any(url[5:] in s for s in self.invalid_list):
            for link in self.valid_list:
                if url.split("://")[1] == link.split("://")[1] and self.frontier.has_next_url():
                    url = self.frontier.get_next_url()
        
            parsed = urlparse(url)
            logger.info("Fetching URL %s ... Fetched: %s, Queue size: %s", url, self.frontier.fetched,
                        len(self.frontier))
            url_data = self.fetch_url(url)
            self.subdomain[parsed.hostname] += 1
            self.valid_list.append(url)


            for next_link in self.extract_next_links(url_data):
                if self.corpus.get_file_name(next_link) is not None:
                    if self.is_valid(next_link):
                        self.frontier.add_url(next_link)
                        self.out_link[url] += 1
                    else:
                        self.invalid_list.append(url)

        
        analytic_file.write("This is the analytic of the crawling result: \n")
        analytic_file.write("The number of URLs processed from each subdomain: \n")
    
        for x, y in self.subdomain.items():
            analytic_file.write('{0:30} {1:4}'.format(x, str(y)))
            analytic_file.write("\n")

        outlink_sorted = sorted(self.out_link.items(), key = lambda x: -x[1])
        most_outlink = outlink_sorted[0]
        analytic_file.write("\n The page with most valid out links is: " + most_outlink[0] +
            " with " + str(most_outlink[1]) + " links. \n")
        
        
        valid_file.write("Here is the list of VALID URLs: \n")
        for x in self.valid_list:
            valid_file.write(x + "\n")
        
        
        invalid_file.write("Here is the list of DUPLICATE AND INVALID URLs: \n")
        for y in self.invalid_list:
            invalid_file.write(y + "\n")
        
        analytic_file.close()
        valid_file.close()
        invalid_file.close()

    def fetch_url(self, url):
        """
        This method, using the given url, should find the corresponding file in the corpus and return a dictionary
        containing the url, content of the file in binary format and the content size in bytes
        :param url: the url to be fetched
        :return: a dictionary containing the url, content and the size of the content. If the url does not
        exist in the corpus, a dictionary with content set to None and size set to 0 can be returned.
        """
        # use the given url, find the corresponding file in the corpus, and return the corresponding things.
        # corpus.get_file_name() only return the address of the file

        url_data = {
            "url": url,
            "content": None,
            "size": 0
        }
        # get the file address, if the file address is not none, enter the block
        # and get the file content and file size.
        if self.corpus.get_file_name(url) is not None:
            file = open(self.corpus.get_file_name(url), "rb")  # read binary
            url_data["content"] = file.read()
            url_data["size"] = len(url_data["content"])
            file.close()

        return url_data

    def extract_next_links(self, url_data):
        """
        The url_data coming from the fetch_url method will be given as a parameter to this method. url_data contains the
        fetched url, the url content in binary format, and the size of the content in bytes. This method should return a
        list of urls in their absolute form (some links in the content are relative and needs to be converted to the
        absolute form). Validation of links is done later via is_valid method. It is not required to remove duplicates
        that have already been fetched. The frontier takes care of that.

        Suggested library: lxml
        """
        # use the url_data, should return a list of urls in absolute form.
        outputLinks = []
        data = html.fromstring(url_data["content"])  # convert the format from binary to element object
        findUrl = data.xpath('//a/@href')            # pull all the tag start with the "href", which are links
        for x in findUrl:
            outputLinks.append(urljoin(url_data["url"], x))  
            # urljoin is used to convert the links to absolute form, and add to the list
        return outputLinks

    def is_valid(self, url):
        """
        Function returns True or False based on whether the url has to be fetched or not. This is a great place to
        filter out crawler traps. Duplicated urls will be taken care of by frontier. You don't need to check for duplication
        in this method
        """
        # repeat, containing a ? and/or a &

        parsed = urlparse(url)  # The url address is disassembled
        if parsed.scheme not in set(
                ["http", "https"]):  # Check the protocol of the links, only valid for http and https
            return False
        

        # create a dictionary, then tokenize the url using slash sign '/',
        # then count the tokens' occurrence in the url
        # and then save the tokens as key and the occurrence as value in the dictionary
        # since a URL with repeating directories is a trap,
        # we can get rid of URLs with repeating directories by analyzing the dictionary
        url_split_list = url.split("/")
        freq = {}
        for item in url_split_list:
            if item in freq:
                freq[item] += 1
            else:
                freq[item] = 1
        j = sorted(freq.items(), key=lambda x: (-x[1], x[0]))

        for _, y in j:
            if y > 1:
                return False
        
        if re.match("^.*calendar.*$", url.lower()):
            return '?' not in url_split_list[-1]

        query_split = url_split_list[-1].split("=")
        if len(query_split[-1]) > 30:
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

