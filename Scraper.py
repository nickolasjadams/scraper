#!/usr/local/bin/python3

from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import platform
from webbot import Browser
import re
from bs4 import BeautifulSoup
import os
import subprocess


class Scraper(Tk):

    def __init__(self):
        super().__init__()

        self.site = StringVar()
        def set_site(p1):
            self.site = self.siteEntry.get()
            print(self.site)

        self.selector = StringVar()
        def set_selector(p1):
            self.selector = self.selectorEntry.get()
            print(self.selector)

        self.dataStr = StringVar()
        def set_data_str(p1):
            self.dataStr = self.dataText.get("1.0", END).strip()
            print(self.dataStr)

        self.urls = []
        self.csvData = ""

        # window settings
        self.geometry("1000x800")
        self.title("Scraper")

        # set up frames
        self.frame = Frame(self)
        self.frame.pack()
        self.bottomFrame = Frame(self)
        self.bottomFrame.pack(side=BOTTOM, pady=10)

        # set top frame labels
        self.dataInputLabel = Label(
            self.frame,
            text="Data Urls\n\"Data title\" https://url.to/test"
        )
        self.dataInputLabel.pack(side=LEFT, padx=65)
        self.dataConfigLabel = Label(self.frame, text="Configuration")
        self.dataConfigLabel.pack(side=RIGHT, padx=150)

        # set data url text field on left
        self.dataText = Text(
            self.bottomFrame, height=50, width=80,
            borderwidth=2, relief=SUNKEN
        )
        self.dataText.pack(fill=X, padx=10, pady=10, side=LEFT)
        self.dataText.bind('<KeyRelease>', set_data_str)

        # get config data
        self.getConfig()

        # insert urls
        for entry in self.urls:
            self.dataText.insert(END, entry)

        # update data string
        self.dataStr = self.dataText.get("1.0", END).strip()

        # set up config entries on the right
        self.siteLabel = Label(self.bottomFrame, text="Site Url")
        self.siteLabel.pack(pady=5)

        

        self.siteEntry = Entry(self.bottomFrame, textvariable=self.site)
        self.siteEntry.pack(fill=X)
        self.siteEntry.bind('<KeyRelease>', set_site)
        self.siteEntry.insert(END, self.site)

        self.selectorLabel = Label(self.bottomFrame, text="Selector")
        self.selectorLabel.pack()

        self.selectorEntry = Entry(self.bottomFrame, textvariable=self.selector)
        self.selectorEntry.pack(fill=X)
        self.selectorEntry.bind('<KeyRelease>', set_selector)
        self.selectorEntry.insert(END, self.selector)


        # set up the results text area
        self.resultsLabel = Label(self.bottomFrame, text="Results")
        self.resultsLabel.pack()

        self.resultsText = Text(
            self.bottomFrame, height=25, width=50,
            borderwidth=2, relief=SUNKEN
        )
        self.resultsText.pack(fill=X, padx=10, pady=10)

        self.copiedMessage = Label(self.bottomFrame, text="")
        self.copiedMessage.pack()

        # Create the scrape button
        # Mac
        # if platform.system() == "Darwin":
        self.goButton = ttk.Button(
            self.bottomFrame, command=self.scrapeToOutput,
            text="Start Scraping"
        )
        # Windows or Linux
        # else:
        #     self.goButton = ttk.Button(
        #         self.bottomFrame, command=self.scrapeToOutput,
        #         text="Start Scraping", bg="Blue", fg="Black"
        #     )
        self.goButton.pack()

        self.openConfigButton = ttk.Button(
            self.bottomFrame, command=self.openConfigFile,
            text="Open Default Configuration File"
        )
        self.openConfigButton.pack(side=BOTTOM)

        
    def openConfigFile(self):
        messagebox.showwarning("Restart Required", "To see the changes made to the default confiugration file take effect, you will need to restart the app.") 
        subprocess.run(['open', os.path.abspath("url-data.txt")], check=True)

    def getConfigString(self, line, keyword, remove_whitespace):
        if remove_whitespace:
            line = line.replace(" ", "")
        line = line.replace(keyword + "=", "")
        line = line.replace("\"", "")
        line = line.rstrip()
        return line

    def getConfig(self):
        file = open(os.path.abspath("url-data.txt"), "r")
        for line in file:
            firstLetter = line[0:1]
            if firstLetter != "#" and len(line) != 1:
                if line[0:4] == "site":
                    self.site = self.getConfigString(
                        line, "site", True
                    )
                elif line[0:8] == "selector":
                    self.selector = self.getConfigString(
                        line, "selector", True
                    )
                else:
                    self.urls.append(line)


    def scrapeToOutput(self):
        self.resultsText.delete("1.0", END)
        print("starting webbot")
        web = Browser(showWindow=False)
        textToList = re.split(r"\n+", self.dataStr)
        print(textToList)
        self.csvData = ""

        for entry in textToList:
            if (entry[0:1] == "\"" or entry[0:1] == "\'"):
                entry = entry[1:]
                entry = entry.rstrip()

                entryList = re.split(r"[\"|\'][\ ]+", entry)

                entryTitle = entryList[0]
                entryUrl = entryList[1]
                if self.site != "":
                    entryUrl = self.site + entryUrl

                self.csvData = self.csvData + "\"" + entryTitle + "\","

                web.go_to(entryUrl)
                pageSrc = web.get_page_source()

                soup = BeautifulSoup(pageSrc, features="html.parser")

                scrapedStr = soup.select(self.selector)[0].string

                self.csvData = self.csvData + scrapedStr + ",\n"


        self.csvData = self.csvData[0:len(self.csvData)-1]
        lastChar = self.csvData[len(self.csvData)-1:len(self.csvData)]
        if lastChar == ",":
            self.csvData = self.csvData[0:len(self.csvData)-1]

        web.quit()

        f = open(os.path.abspath("results.csv"), "w")
        f.write(self.csvData)
        f.close()
        print(self.csvData)

        self.resultsText.insert(END, self.csvData)

        self.copiedMessage.config(text="Copied to Clipboard Automatically.")
        self.clipboard_clear()
        self.clipboard_append(self.csvData)
        self.update()



if __name__ == "__main__":
    app = Scraper()
    app.mainloop()
