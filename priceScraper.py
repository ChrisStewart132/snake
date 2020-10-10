import urllib.request as urllib
import time
from tkinter import *
from tkinter.ttk import *
import os.path

class Stock():
    def __init__(self, code):
        self.code = code
        self.buy = 0
        self.sell = 0
    def __str__(self):
        return "code: {}, buy: {}, sell: {}".format(self.code, self.buy, self.sell)
    def __lt__(self, other):
        return self.sell > other.sell

class Application():
    codesString = "AIR,ANZ,WBC,FBU,ZEL"

    def __init__(self, window):
        self.create_widgets()
        self.cacheFromFile()
 
    def create_widgets(self):
        '''display stuff'''
        font_style = "Arial"
        font_size = 13
        
        self.update_button = Button(window, text="UPDATE",command=self.update)
        self.update_button.grid(row=0,column=0)
        
        self.cache = Button(window, text="CACHE",command=self.cachePrice)
        self.cache.grid(row=1,column=0)

        self.stock_list_cache = []      #cache of below stock codes for comparison
        self.stock_list = []            #list of stock class objects initialized off a string of stock codes
        self.stock_code_labels = []
        self.stock_buy_labels = []
        self.stock_sell_labels = []
        self.stock_delta_labels = []
        for i, stock in enumerate(self.codesString.split(",")):
            self.stock_list_cache.append(Stock(stock))
            self.stock_list.append(Stock(stock))
            if i == 0:
                spacing = 20
            else:
                spacing = 0
            label_width = 6
            self.stock_code_labels.append(Label(window,text=self.stock_list[i].code,width=label_width,font=(font_style, font_size)))
            self.stock_code_labels[i].grid(row=0,column = 1 + i,padx=(spacing,0))
            
            self.stock_buy_labels.append(Label(window,text=self.stock_list[i].buy,width=label_width,font=(font_style, font_size)))
            self.stock_buy_labels[i].grid(row=1,column = 1 + i,padx=(spacing,0))
            
            self.stock_sell_labels.append(Label(window,text=self.stock_list[i].sell,width=label_width,font=(font_style, font_size)))
            self.stock_sell_labels[i].grid(row=2,column = 1 + i,padx=(spacing,0))
            
            self.stock_delta_labels.append(Label(window,text=self.stock_list[i].sell-self.stock_list_cache[i].sell,width=label_width,font=(font_style, font_size)))
            self.stock_delta_labels[i].grid(row=3,column = 1 + i,padx=(spacing,0))

        self.silver_label = Label(window,text="silver: ",font=(font_style, font_size))
        self.silver_label.grid(row=4,column=1,columnspan=5)
    
    def extract_price(self, s, start_quote, length=5):
        """s=web page string, start_quote=search query/tag, length=len of the price"""
        start = s.index(start_quote)
        offset=len(start_quote)
        price = ""
        for i in range(length):
                char = s[i+start+offset]
                if char.isnumeric() or char=='.':
                    price = price + char
        return price
        
    def update(self):
        '''main function, runs when update clicked, scrapes web page docs for targeted info'''
        b1 = "https://www.directbroking.co.nz/DirectTrade/dynamic/quote.aspx?qqsc="
        b2 = "&qqe=NZSE"
        for i, stock in enumerate(self.stock_list):
            url = b1+stock.code+b2
            obj = urllib.urlopen(url)
            s = obj.read().decode()
            self.stock_list[i].buy = self.extract_price(s, 'span id="quotebuy">')#tag from analysing web page for stock price
            self.stock_list[i].sell = self.extract_price(s, 'span id="quotesell">')#tag from analysing web page for stock price
            self.stock_buy_labels[i]['text'] = self.stock_list[i].buy
            self.stock_sell_labels[i]['text'] = self.stock_list[i].sell
            
        silverLink = 'http://www.livepriceofgold.com/silver-price/new-zealand.html'
        silverDoc = urllib.urlopen(silverLink)
        s = silverDoc.read()
        s = s.decode()
        silverPrice = self.extract_price(s, 'Silver Price per Kg in NZD</td><td>', 8)
        self.silver_label["text"]="SILVER (NZD/kg) : {}".format(silverPrice)  
    
    def cacheToFile(self):
        '''run inside cachePrice (when cache clicked)'''
        directory = "cache.txt"
        outfile = open(directory, 'w')
        print("cache to file...")
        result = ""
        for stock in self.stock_list:
            result += "{},{},{}\n".format(stock.code, stock.buy, stock.sell)
        result += self.silver_label['text']
        outfile.write(result[:-1])
        outfile.close()

    def cachePrice(self):
        '''run when button clicked, updates display and text file when clicked'''
        print("saving prices")
        for i, stock in enumerate(self.stock_list):
            self.stock_list_cache[i].buy = stock.buy
            self.stock_list_cache[i].sell = stock.sell
            print(self.stock_list_cache[i].code  + " " + self.stock_list_cache[i].buy + " "  + self.stock_list_cache[i].sell)
        self.cacheToFile()
        
    def cacheFromFile(self):
        '''runs on startup, loads cache.txt string to display'''
        if os.path.isfile("cache.txt"):
            infile = open("cache.txt")
            for i, line in enumerate(infile.read().split('\n')):
                print(line)
                if line.startswith("SILVER"):
                    self.silver_label['text'] = line
                else:
                    split_line = line.split(",")
                    self.stock_list_cache[i].code = split_line[0]
                    self.stock_list_cache[i].buy = split_line[1]
                    self.stock_list_cache[i].sell = split_line[2]
                    
                    self.stock_list[i].code = split_line[0]
                    self.stock_list[i].buy = split_line[1]
                    self.stock_list[i].sell = split_line[2]
                    self.stock_code_labels[i]['text'] = split_line[0]
                    self.stock_buy_labels[i]['text'] = split_line[1]
                    self.stock_sell_labels[i]['text'] = split_line[2]          
        else:
            print("error, no 'cache.txt' in directory, click update then cache to generate..")
    
window = Tk()
price_scraper_gui = Application(window)
window.mainloop()




    
