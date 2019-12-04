from collections import defaultdict
import json
from pymongo import MongoClient
from tkinter import *
import urllib
from bs4 import BeautifulSoup
import webbrowser
import time
from tkinter.font import Font

webpage_path = "WEBPAGES_RAW"
json_path = "WEBPAGES_RAW/bookkeeping.json"

def tf_idf( token_info: (str, dict) ):
	return token_info[1]["tf-idf"]
	
class Search:

	def window_clear(self):
		for widget in self.main_win.winfo_children():
			widget.destroy()

	def new_search_page(self):
		self.window_clear()

		_middle_height = int(self.main_win.winfo_screenheight() / 2 )
		_middle_width = int(self.main_win.winfo_screenwidth() / 2 )

		uci_logo = PhotoImage(file = "uci_logo.png")
		logo = Label(self.main_win, image = uci_logo)
		logo.image = uci_logo
		logo.place(x = _middle_width , y = _middle_height - 250, anchor = "center")

		label = Label(self.main_win, text = "Enter to search:")
		label.config(font=("Arial ", 35))
		label.place(x = _middle_width , y = _middle_height - 40, anchor = "center")

		self.query_entry = Entry(self.main_win)
		# self.query_entry.bind("<Return>", self.new_result_page)
		self.query_entry.config(font = ("Arial ", 30), bd = 3)
		self.query_entry.place(x = _middle_width, y = _middle_height + 50, anchor = "center")
		

		search_button = Button(self.main_win, text = 'Search', command = self.new_result_page)
		search_button.config(width = 20, font = ("Arial ", 30), bg = "cornflowerblue", fg = "white")
		search_button.place(x = _middle_width, y = _middle_height + 150, anchor = "center")
		# search_button.bind("<Return>", self.new_result_page)
		
		quit_button = Button(self.main_win, text = 'Quit', command = self.main_win.quit)
		quit_button.config(width = 5, font = ("Arial ", 30), bg = "indianred")
		quit_button.place(x = _middle_width, y = _middle_height + 240, anchor = "center")


	def _open_link(self, event):
		webbrowser.open_new(str(event.widget.cget("textvariable")))

	def new_result_page(self):
		
		self.query_input = self.query_entry.get()
		self.window_clear() # clear window
		start = time.time()
		
		url_list = self.search(self.query_input.lower())

		if(len(url_list)!= 0):
			result_title = Label(self.main_win, text = "Here are the top {} results for '{}':".format(len(url_list),self.query_input))
			result_title.grid(row = 0, column = 1, sticky = "W")
			result_title.config(font=("Arial ", 24))

			time_used = Label(self.main_win, text = "(Search time: {} seconds)".format((time.time() - start)))
			time_used.config(font=("Arial ", 20))
			time_used.grid(row = 1, column = 1, sticky="W")


		current_row = 2
		result_num = 1
		for docID, socre in url_list:
			number_label = Label(self.main_win, text = str(result_num) + ".")
			number_label.grid(row = current_row, column = 0)
			number_label.config(font=("Arial ", 24))

			url_json = json.load(open(json_path)) 		# Contains the key for the docIDs to their urls
			url = url_json[docID]
			
			# Extracts title from doc; Done upon search instead of storing in db to save space
			html_id_info = docID.split("/") # stored in "folder/html_file" format
			file_name = "{}/{}/{}".format(webpage_path, html_id_info[0], html_id_info[1])
			html_file = open(file_name, 'r', encoding = 'utf-8')
			soup = BeautifulSoup(html_file, 'lxml')
			title_tag = soup.find('title')
		
			if ( (title_tag is None) or (title_tag.string is None) ): #Title doesn't exist or is length 0
				title = url # title defaults to url
			else:
				title = title_tag.string.strip() #Uses actual title	
			
			link_title = Label(self.main_win, text = title, textvariable="http://"+url, fg = "mediumblue", cursor="hand2")
			link_title.grid(row = current_row, column = 1, sticky = "W", columnspan = int(self.main_win.winfo_screenwidth()/2))
			f = Font(family="Arial ", size = 20)
			f.configure(underline = 1)
			link_title.config(font=f)
			link_title.bind("<Button-1>", self._open_link)
			current_row += 1

			url_string = Label(self.main_win, text = url, fg = "darkgreen")
			url_string.grid(row=current_row, column = 1, sticky = "W")
			url_string.config(font=("Arial ", 14))
			current_row += 1

			result_num += 1

		if (len(url_list) == 0):
			error_label = Label(self.main_win, text = "No results found!")
			error_label.grid(row = 2, column = 1, sticky = "W")
			error_label.config(font=("Arial ", 24))
			current_row += 1


		new_search_label = Button(self.main_win, text = "Search again", fg = "red", command=self.new_search_page)
		new_search_label.grid(row=current_row, column=1, sticky="W")
		new_search_label.config(font=("Arial ", 24))

	def __init__(self, myDbName, collectionName):
		self._db_host = MongoClient('mongodb://localhost:27017')
		self._db = self._db_host[myDbName]					# Name of the db being used
		self._collection = self._db[collectionName] 

		self.main_win = Tk()
		self.main_win.title('Project 3 Search Engine')

		screen_height = self.main_win.winfo_screenheight()
		screen_width = self.main_win.winfo_screenwidth()
		self.main_win.geometry("%dx%d" % (screen_width, screen_height))
		
		self.main_win.resizable(0, 0)
		self.query_entry = None
		self.query_input = None
		self.new_search_page()

	def search(self, queries: str)->list:
		"""
        return a top 20 url list that matches the given query by the tf-idf score
        :return: top 20 url list
        """
		matched_list = []  # the match list that will contain top 20 url result.
		score_dict = defaultdict(lambda: [0.0,0])  # helper dictionary {docId: (tf-idf-sum:float, mathced:int)}, store URL as key and the score matching tuple as its value

		for word in queries.split():  # split the input query str into single word for futher search
			try:
				counts = 0
				raw_dict = self._collection.find({"id": word.lower()}).next()[
					"info"]  # in the database collection, find the id strat with te reuqired word(from query), assign it info dictionary to raw_dict
				sorted_doc = sorted(raw_dict.keys(), key=lambda x: -raw_dict[x][
					"tf-idf"])  # Sort the keys(docId) from raw_dict with decreasing "tf-idf" value inside the dictionary, then assigen the sored docId to sorted_doc

				for docId in sorted_doc:  # iter the docId which is sored from highest tf-idf to lowest tf-idf
					counts += 1  # undate counts
					score_dict[docId][0] += raw_dict[docId]["tf-idf"]  # update the url key with its tf-idf-sum socre (add tf-idf number stored in the raw_dict)
					score_dict[docId][1] += 1  # update the url key with it matched time (number of the words from the query that matched the doc)

					if (counts == 20): break  # We only need top 20 result for each word in the query, so don't wast space.

			except StopIteration:
				pass  # if the word can not be found in our database, we pass this loop

			for docId, count_and_tf_idf in sorted(score_dict.items(), key=lambda x: (-x[1][1], -x[1][0])):
				if( len(matched_list) < 20 ):
					matched_list.append( [docId,count_and_tf_idf] )
				else:
					break

			return matched_list


if __name__ == "__main__":
	print("Starting search program...")
	search_program = Search("invertedIndex", "Documents")

	mainloop( )