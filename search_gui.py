from search import search
import webbrowser
from tkinter import *


class Interface(object):
    def __init__(self):
        self.WEBPAGES_RAW_PATH = "C:\Users\Nuo\Desktop\WEBPAGES_RAW"
        self.invertedIndex_PATH = "C:\Users\Nuo\Desktop\WEBPAGES_RAW\invertedIndex.json"
        self.root = Tk()
        self.root.title("CS121: project3")
        self.root.geometry("900x800")    
        self.root["padx"] = 30
        self.root["pady"] = 20
        # create all of the main containers
        self.top_frame = Frame(self.root, bg='grey', width = 850, height=100)
        self.btm_frame = Frame(self.root, bg='grey', width = 850, height = 650)

        # layout all of the main containers
        self.root.grid_rowconfigure(6, weight=1)
        self.root.grid_columnconfigure(6, weight=1)
        
        self.top_frame.grid(row=0, sticky="ew")
        self.btm_frame.grid(row=1, sticky="ewn")
        # create the widgets for the top frame
        queryLabel = Label(self.top_frame, bg='grey',text="Enter a Query: ")
        self.queryEntry = Entry(self.top_frame, width=50)
        # self.queryEntry.bind("<Return>", lambda e: self.doSearch())

        button = Button(self.top_frame, bg='grey', text ="Go!", command = self.doSearch)
        button.grid(row=0, columnspan = 10,column = 12)

        # layout the widgets in the top frame
        queryLabel.grid(row = 0, columnspan = 5)
        self.queryEntry.grid(row = 0, column = 6)


    def launch(self):
        self.root.mainloop()

    def doSearch(self):
        self.resultrow =0
        queryString = self.queryEntry.get() 
        t1 =search(self.WEBPAGES_RAW_PATH,self.invertedIndex_PATH)
        print(queryString)
        links=t1.searching(queryString)
        for link in links:
            print(link)
        self.queryEntry.delete(0, END)
        self.btm_frame.destroy()
        self.btm_frame = Frame(self.root, bg='lavender', width = 850, height = 650, pady=3)
        self.btm_frame.grid(row=1, sticky="ewn")
        resultsNumber = 1
        if len(links) > 0:
            for result in links:
                number_label = Label(self.btm_frame, text=str(resultsNumber) + ".")
                number_label.grid(row=self.resultrow, column=0)
                number_label.config(font=("Arial "))                
                link = Label(self.btm_frame, text = result, textvariable="http://" + result, fg = "mediumblue", cursor = "hand2")
                link.grid(row=self.resultrow, column = 1, sticky = "W")
                link.bind("<Button-1>", lambda e: self.openPage(result, e))
                self.resultrow +=1
                resultsNumber += 1

        else:
            link = Label(self.btm_frame, text="No results found!", fg="blue")
            link.grid(row=self.resultrow)

    def openPage(self, url, event):
        try:
            webbrowser.open_new(str(event.widget.cget("textvariable")))
        except:
            print ("cant access")


if __name__ == "__main__":
    gui = Interface()
    gui.launch()