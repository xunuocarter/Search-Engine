import json
from pymongo import MongoClient
from collections import defaultdict

testing = True

class Search_Engine:
    def __init__(self, jsonFileName, myDbName:str, collectionName:str):
        """
        Connect with mongodb and reach the given collection
        """
        
        self.fileName = jsonFileName
        
        self.dbHost = MongoClient('mongodb://localhost:27017')
        
        self.dbName = self.dbHost[myDbName]
        
        self.collection = self.dbName[collectionName]

    def match(self, query:str)->list:
        """
        return a top 10 url list that matches the given query by the tf-idf score
        :return: top 10 url list
        """
        matched_list = []  
        score_dict = defaultdict(lambda: [0.0,0]) 
        with open(self.fileName) as loadFile: 
            data_dict = json.load(loadFile)

        for word in query.split(): #split the input query str into single word for futher search
            try:
                counts = 0
                raw_dict = self.collection.find({"id":word.lower()}).next()["info"] 
                sorted_doc = sorted(raw_dict.keys(), key = lambda x: -raw_dict[x]["tf-idf"]) 

                for docId in sorted_doc:#iter the docId which is sored from highest tf-idf to lowest tf-idf
                    counts += 1 #undate counts
                    score_dict[data_dict[docId]][0] += raw_dict[docId]["tf-idf"] 
                    score_dict[data_dict[docId]][1] += 1 

                    if (counts == 20):break 

            except StopIteration: pass 



            if testing:  
                print(len(score_dict))
                pass

        return matched_list

if __name__ == "__main__":
    search_engine = Search_Engine("WEBPAGES_RAW/bookkeeping.json","invertedIndex", "Documents")
    search_engine.match("Informatics")
