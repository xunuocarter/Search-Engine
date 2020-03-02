import json
from collections import defaultdict
from bs4 import BeautifulSoup
import os
import re
import math
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import time

class search_Engine:
	stop_word=["a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't", "as",
             "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can't",
             "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down",
             "during", "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't",
             "having", "he", "he'd", "he'll", "he's", "her", "here","here's", "hers", "herself", "him", "himself",
             "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's",
             "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off",
             "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same",
             "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than", "that",
             "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they",
             "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up",
             "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's",
             "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with",
             "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself",
             "yourselves"]
	def __init__(self,dir_path):
		self.dir_path = dir_path
		self.json_file = os.path.join(dir_path,"bookkeeping.json")
		self.bookkeeping = dict()
		self.invertedIndex = defaultdict(lambda :  defaultdict(lambda: [0,0.0,0]))
		self.total_files = 0

	def lemmatization(self,word):
		wnl = WordNetLemmatizer()
		tag = nltk.pos_tag([word])
		if tag[0][1].startswith('NN'):
			return wnl.lemmatize(word, pos='n')
		elif tag[0][1].startswith('VB'):
			return wnl.lemmatize(word, pos='v')
		elif tag[0][1].startswith('JJ'):
			return wnl.lemmatize(word, pos='a')
		elif tag[0][1].startswith('R'):
			return wnl.lemmatize(word, pos='r')
		else:
			return word

	def inverted(self,docID,text,tag):
		content = word_tokenize(text)
		#print(content)
		for word in content:
			if word.lower() not in self.stop_word and word.isalnum()and len(word) >3:
				new_word = self.lemmatization(word)
				self.invertedIndex[new_word.lower()][docID][0]+=1
				if tag:
					self.invertedIndex[new_word.lower()][docID][2]+=1


	def tfidf(self):
		for i in self.invertedIndex:
			df = len(self.invertedIndex[i].keys())
			for j in self.invertedIndex[i]:
				tf = self.invertedIndex[i][j][0]
				idf= math.log10(self.total_files / (df+1) )
				tf_idf = tf * idf
				self.invertedIndex[i][j][1] = tf_idf
				if self.invertedIndex[i][j][2] != 0:
					self.invertedIndex[i][j][1] += self.invertedIndex[i][j][2]* self.invertedIndex[i][j][0]

	def start(self):
		with open(self.json_file) as f:
			self.bookkeeping = json.load(f)
		self.total_files = len(self.bookkeeping.keys())
		for docId in self.bookkeeping:
			try:
				print(docId)
				print(os.path.join(self.dir_path,docId))
				with open(os.path.join(self.dir_path,docId)) as j:
					soup = BeautifulSoup(j, 'lxml')
					for item in soup(["script", "style"]):
						item.extract()
					text_content = soup.get_text(separator=' ')
					self.inverted(docId,text_content,False)

					tag_list= ["h1","h2","h3","b","strong"]
					for tag in tag_list:
						#print(tag)
						item=soup.find_all(tag)
						for i in item:
							i_content = i.get_text()
							self.inverted(docId,i_content,True)
			except:
				pass
		self.tfidf()
		print("write in file")
		json_str = json.dumps(self.invertedIndex, indent = 4)
		with open(os.path.join("C:\Users\Nuo\Desktop\WEBPAGES_RAW\121test","invertedIndex.json"),"w") as json_file:
			json_file.write(json_str)



if __name__ == "__main__":
    t1 = search_Engine("C:\Users\Nuo\Desktop\121test")
    t1.start()







