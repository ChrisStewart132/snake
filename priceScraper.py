import urllib.request as urllib
import time
import tkinter as tk
import os.path

class Application(tk.Frame):
    itemListCache = []#stocks silver etc.
    priceListCache = []#prices of above
    delta = [0,0,0,0,0,0,0,0,0,0,0,0,0]#difference between cache and latest update
    
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        print("init..")
        self.cacheFromFile()
        
    def create_widgets(self):
        '''display stuff'''
        self.updateBtn = tk.Button(self)
        self.updateBtn["text"] = "\n    UPDATE  \n"
        self.updateBtn["command"] = self.update
        self.updateBtn.pack(side="top")

        self.space = tk.Message(self)
        self.space["text"] = "=                                                                            ="
        self.space.pack(side="top")
        
        self.message = tk.Message(self)
        self.message["text"] = ""
        self.message.pack(side="top")

        self.space2 = tk.Message(self)
        self.space2["text"] = "=                                                                            ="
        self.space2.pack(side="top")

        self.cache = tk.Button(self,text="  CACHE   \n\n",command=self.cachePrice)
        self.cache.pack(side="top")

        self.space2 = tk.Message(self)
        self.space2["text"] = "=                                                                            ="
        self.space2.pack(side="top")
        
        self.quit = tk.Button(self, text="QUIT", fg="red",command=self.master.destroy)
        self.quit.pack(side="top")

    def update(self):
        '''main function, runs when update clicked, scrapes web page docs for targeted info'''
        updateText = ""
        print("web update..")
        codesString = "AIR,ANZ,WBC,FBU,ZEL"
        b1 = "https://www.directbroking.co.nz/DirectTrade/dynamic/quote.aspx?qqsc="
        b2 = "&qqe=NZSE"
        urls = []
        codes = codesString.split(",")
        for code in codes:
            urls.append(b1+code+b2)
            if len(self.itemListCache)<len(codes)+1:#stocks + 1 for silver price..
                self.itemListCache.append(code)
        n = 0
        for url in urls:
            obj = urllib.urlopen(url)
            #print(codesString.split(",")[n])#nzx codes
            updateText = updateText + codesString.split(",")[n]#AIR
            s = obj.read()
            s = s.decode()#convert data from byte array to string
            start = s.index('span id="quotebuy">')
            quotebuy=""
            offset=len('span id="quotebuy">')
            for i in range(5):
                char = s[i+start+offset]
                if char.isnumeric() or char=='.':
                    quotebuy = quotebuy + char
            #print("buy:" + quotebuy)
            updateText = updateText + "     " + quotebuy#AIR 134
            start = s.index('span id="quotesell">')
            quotesell=""
            offset=len('span id="quotesell">')
            for i in range(5):
                char = s[i+start+offset]
                if char.isnumeric() or char=='.':
                    quotesell = quotesell + char
            quotesell = quotesell.replace(" ","")
            if len(self.priceListCache)<len(codes)+1:#stocks + 1 for silver price..
                self.priceListCache.append(float(quotesell))
            self.delta[n] = self.priceListCache[n] - float(quotesell)
            #print("{} : {} : {}".format(self.itemListCache[n], self.priceListCache[n],self.delta[n]))
            self.priceListCache[n] = float(quotesell)
            #print("sell:" + quotesell)
            updateText = updateText + "     " + quotesell + "     " + str(self.delta[n])#AIR 134 135
            n = n + 1
            time.sleep(0.5)
            updateText = updateText + "\n"

        silverLink = 'http://www.livepriceofgold.com/silver-price/new-zealand.html'
        silverDoc = urllib.urlopen(silverLink)
        s = silverDoc.read()
        s = s.decode()
        searchValue = 'Silver Price per Kg in NZD</td><td>'
        start = s.index(searchValue)
        silverPrice = ""
        for i in range(8):
            char = s[i+start+len(searchValue)]
            silverPrice = silverPrice + char
        self.message["text"]=updateText + "\nSILVER (NZD/kg) : {}".format(silverPrice)

    def cacheToFile(self):
        '''run inside cachePrice (when cache clicked)'''
        directory = "cache.txt"
        outfile = open(directory, 'w')
        print("cache to file...")
        stockStrings = self.message["text"]
        stockData = stockStrings.split("\n")
        result = ""
        for stock in stockData:
            result = result + stock + "\n"
        outfile.write(result)
        outfile.close()

    def cachePrice(self):
        '''run when button clicked, updates display and text file when clicked'''
        print("saving prices")
        stockStrings = self.message["text"]
        stockData = stockStrings.split("\n")
        result = ""
        for stock in stockData:
            result = result + stock + "\n"
        self.cache["text"]= "   CACHE   \n\n" + result
        self.cacheToFile()
        #below to cache prices as variables..
        temp = result.split("\n")
        temp2 = []
        for i in range(len(temp)):
            if len(temp[i])>=3:
                temp2.append(temp[i])
                #print(temp[i])
        temp3 = []
        for i in range(len(temp2)):
            temp3.append(temp2[i].replace("   ",":"))
            #print(temp3[i])
        temp3.pop()
        temp4 = []
        for i in range(len(temp3)):
            temp4.append(temp3[i].split(":"))
            #print(temp4[i])
            if len(self.itemListCache)<6:#manual update if increase/decrease stock codes..todo
                self.itemListCache.append(temp4[i][0])
            if len(self.priceListCache)<6:#stocks + 1 for silver price..
                self.priceListCache.append(float(temp4[i][2]))      
            self.delta[i] = self.priceListCache[i] - float(temp4[i][2])
            self.priceListCache[i] = float(temp4[i][2])
        
    def cacheFromFile(self):
        '''runs on startup, loads cache.txt string to display'''
        
        if os.path.isfile("cache.txt"):
            infile = open("cache.txt")
            self.cache["text"] = "   CACHE   \n\n" + infile.read()
        else:
            print("error, no 'cache.txt' in directory, click update then cache to generate..")

root = tk.Tk()
app = Application(master=root)
app.mainloop()




    
