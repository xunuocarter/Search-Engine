from collections import defaultdict
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup
import math
import os
import json

class search:

	def __init__(self,dir_path,dataSet):
		self.dir_path = dir_path
		self.dataSet = dataSet
		self.json_file = os.path.join(dir_path,"bookkeeping.json")
		with open(self.json_file) as f:
			self.bookkeeping = json.load(f)
		with open(os.path.join(dir_path,dataSet)) as g:
			self.dataSet = json.load(g)
		self.total_files = len(self.bookkeeping.keys())


	def searching(self,query):
		query_in_word=word_tokenize(query)
		files_set=set()
		#print(query_in_word)
		for word in query_in_word:
			try:
				files_set.update(self.dataSet[word].keys())
			except:
				#if word in query does not appear in dataset
				pass

		#print(files_set)
		self.score_dict = defaultdict(float)
		for file in files_set:
			self.score_dict[file] = self.cosine_similarity(query,file)
		sort_sort = sorted(self.score_dict.items(), key=lambda x: (-x[1], x[0]))
		#print(sort_sort)
		doc_id=[]
		for i in range(20):
			if i <= len(sort_sort)-1:
				#print(sort_sort[i][0])
				doc_id.append(sort_sort[i][0])
		output_links=[]
		for j in doc_id:
			output_links.append(self.bookkeeping[j])
		return output_links



	def cosine_similarity(self,query,file):
		soup = BeautifulSoup(open(os.path.join(self.dir_path,file)),'lxml')
		for item in soup(["script", "style"]):
			item.extract()
		text = soup.get_text(separator=' ')
		text = text +" " + query
		token=word_tokenize(text)
		# print(query)
		# print(file)
		# print(token)
		query_l = word_tokenize(query)
		# for  query
		#key: word  value: index 0 -> wt index 1 -> n'lize 
		dict1= defaultdict(lambda:[0.0,0.0])
		# for file
		dict2= defaultdict(lambda:[0.0,0.0])
		for item in token:
			if item in self.dataSet:
				# print(item)
				if item in query_l:
					# print(item," ",query_l.count(item))
					tf_query = 1 + math.log10(query_l.count(item))
				else:
					tf_query = 0
				df = len(self.dataSet[item].keys())
				idf = math.log10(self.total_files / (df+1)) 
				#print("--------------",tf_query,"    ",idf)
				wt_query = tf_query * idf
				dict1[item][0] = wt_query

				try:
					dict2[item][0] = self.dataSet[item][file][1]
				except:
					dict2[item][0] = 0

		length_query=0
		length_doc=0

		for i in dict1:
			length_query += dict1[i][0]**2
			length_doc += dict2[i][0]**2
		length_query =math.sqrt(length_query)
		length_doc = math.sqrt(length_doc)

		for item in dict1:
			dict1[item][1] = dict1[item][0]/length_query
			dict2[item][1] = dict2[item][0]/length_doc

		prod=[]
		for i in dict1:
			prod.append( dict1[i][1]*dict2[i][1] )
		return sum(prod)


if __name__ =="__main__":
	t1 =search("C:\Users\Nuo\Desktop\WEBPAGES_RAW","C:\Users\Nuo\Desktop\WEBPAGES_RAW\invertedIndex.json")
	links=t1.searching("open")
	for j in links:
		print(j)


