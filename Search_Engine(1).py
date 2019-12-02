import json
from pymongo import MongoClient
from collections import defaultdict

testing = True

class Search_Engine:
    def __init__(self, jsonFileName, myDbName:str, collectionName:str):
        """
        Connect with mongodb and reach the given collection
        """
        #Store json name into class for further
        self.fileName = jsonFileName
        #Connect to mongodb localhost
        self.dbHost = MongoClient('mongodb://localhost:27017')
        #Direct to the given database name
        self.dbName = self.dbHost[myDbName]
        #Direct to the given database collection
        self.collection = self.dbName[collectionName]

    def match(self, query:str)->list:
        """
        return a top 10 url list that matches the given query by the tf-idf score
        :return: top 10 url list
        """
        matched_list = []  # the match list that will contain top 20 url result.
        score_dict = defaultdict(lambda: [0.0,0]) # helper dictionary {URL: (tf-idf-sum:float, mathced:int)}, store URL as key and the score matching tuple as its value
        with open(self.fileName) as loadFile: #open & Load json file as data_dict with stored fileName -> so that we can find matched url from its docId
            data_dict = json.load(loadFile)

        for word in query.split(): #split the input query str into single word for futher search
            try:
                counts = 0
                raw_dict = self.collection.find({"id":word.lower()}).next()["info"] #in the database collection, find the id strat with te reuqired word(from query), assign it info dictionary to raw_dict
                sorted_doc = sorted(raw_dict.keys(), key = lambda x: -raw_dict[x]["tf-idf"]) #Sort the keys(docId) from raw_dict with decreasing "tf-idf" value inside the dictionary, then assigen the sored docId to sorted_doc

                for docId in sorted_doc:#iter the docId which is sored from highest tf-idf to lowest tf-idf
                    counts += 1 #undate counts
                    score_dict[data_dict[docId]][0] += raw_dict[docId]["tf-idf"] #update the url key with its tf-idf-sum socre (add tf-idf number stored in the raw_dict)
                    score_dict[data_dict[docId]][1] += 1 #update the url key with it matched time (number of the words from the query that matched the doc)

                    if (counts == 20):break #We only need top 20 result for each word in the query, so don't wast space.

            except StopIteration: pass #if the word can not be found in our database, we pass this loop



            if testing:  # For testing
                #print(len(sorted_doc))
                print(len(score_dict))
                pass

        return matched_list

if __name__ == "__main__":
    search_engine = Search_Engine("WEBPAGES_RAW/bookkeeping.json","invertedIndex", "Documents")
    search_engine.match("Informatics")
