#Library Imports

import tkinter as tk
import asyncio
from requests_html import AsyncHTMLSession
from bs4 import BeautifulSoup
import webbrowser
from string import punctuation
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')

#Neccesarry Variable Insitalization

session = AsyncHTMLSession()
headers = {'User-Agent': 'Mozilla/5.0'}
news = []
loop = asyncio.get_event_loop()

#Classes

class headline:
    """
    This class is used to hold information about the headlines extracted for webisites, their source
    and link to the articles
    """
    def __init__(self,href="",text="",publisher=""):
        self.href = href
        self.text = text
        self.publisher = publisher

#Asynchronous Functions

async def bbc():
    """
    Asynchronous functions the runs along with alj and cnn to extract
    information from bbc website using requests_html library to get
    html data from the source and uses the BeautifulSoup from bs4 library
    to pharse and format the html data
    """
    address = "https://www.bbc.com"
    website = await session.get(address,headers=headers)
    sourcecode = BeautifulSoup(website.content,'html5lib')
    h3 = sourcecode.findAll("h3",class_="media__title")
    for response in h3:
        if address not in response.a["href"]:
                news.append(headline(address+response.a["href"],response.text.strip().lower(),"BBC"))
                continue
        news.append(headline(response.a["href"],response.text.strip(),"BBC"))

async def alj():
    """
    Asynchronous functions the runs along with bbc and cnn to extract
    information from Al Jazeera website using requests_html library to get
    html data from the source and uses the BeautifulSoup from bs4 library
    to pharse and format the html data
    """
    address = "https://www.aljazeera.com"
    website = await session.get(address,headers=headers)
    sourcecode = BeautifulSoup(website.content,'html5lib')
    a = sourcecode.findAll("a")
    for response in a[26:-35]:
        news.append(headline(address+response["href"],response.text.strip(),"Al Jazeera"))

async def cnn():
    """
    Asynchronous functions the runs along with alj and bbc to extract
    infromation from cnn website using requests_html library to get
    html data from the source and uses the BeautifulSoup from bs4 library
    to pharse and format the html data
    """
    address = ["https://edition.cnn.com/data/ocs/container/coverageContainer_8DDF4E26-8632-6418-1586-B910547ED120:list-hierarchical-xs/views/containers/common/container-manager.html"
    ,"https://edition.cnn.com/data/ocs/container/coverageContainer_30520545-5527-A0DE-6AF4-0B5946BC001B:list-hierarchical-xs/views/containers/common/container-manager.html"
    ,"https://edition.cnn.com/data/ocs/container/coverageContainer_3CAD0E48-D9FB-532B-3601-0B56235E4DC2:list-hierarchical-xs/views/containers/common/container-manager.html"
    ,"https://edition.cnn.com/data/ocs/container/coverageContainer_3FC44C1D-B590-FC74-DDB7-AE3B16C4AADA:list-hierarchical-xs/views/containers/common/container-manager.html"
    ,"https://edition.cnn.com/data/ocs/container/coverageContainer_A0FA819C-B5F5-34C0-CFCB-0B50F45BCF5B:list-hierarchical-xs/views/containers/common/container-manager.html"
    ,"https://edition.cnn.com/data/ocs/container/coverageContainer_BCA237D5-94CD-9985-6A27-0B58111C0F5E:list-hierarchical-xs/views/containers/common/container-manager.html"
    ,"https://edition.cnn.com/data/ocs/container/coverageContainer_588D7620-5F4D-1989-FC00-302054186D22:list-hierarchical-xs/views/containers/common/container-manager.html"
    ,"https://edition.cnn.com/data/ocs/container/coverageContainer_C3738EDC-EB8F-750F-7B6D-0500FC0ABE09:list-hierarchical-small-horizontal/views/containers/common/container-manager.html"
    ,"https://edition.cnn.com/data/ocs/container/coverageContainer_937579B2-17A9-13BA-937A-301F1EC5279A:list-hierarchical-xs/views/containers/common/container-manager.html"
    ,"https://edition.cnn.com/data/ocs/container/coverageContainer_42A9B075-1119-8C37-E0FB-301D87BA2A5C:list-hierarchical-xs/views/containers/common/container-manager.html"
    ,"https://edition.cnn.com/data/ocs/container/coverageContainer_45F12FF6-D9C4-8C49-A118-3A4AEA87BF57:grid-small/views/containers/common/container-manager.html"]

    for x in address:
        website = await session.get(x,headers=headers)
        await website.html.arender(sleep=1,timeout=20)
        sourcecode = BeautifulSoup(website.content,'html5lib')
        h3 = sourcecode.findAll("h3")
        for response in h3:
            news.append(headline("https://www.cnn.com"+response.a["href"],response.text.strip(),"CNN"))

#Functions

def onbuttonclick():
    """
    function that runs when the submit button is clicked
    """
    loadframe = tk.Frame(interface,bg="#D4355A",width =interface.winfo_screenwidth()-15,border=1.3,relief="ridge",height=interface.winfo_screenheight()+15).place(relx=0.995,rely=0.015,anchor='ne')
    tk.Label(loadframe,image=bgimg,width=interface.winfo_screenwidth()-30, height=interface.winfo_screenheight()+10).place(relx=0.991,rely=0.020,anchor='ne')
    bar = tk.Frame(card1,bg="#BB0F37",relief="raised",border=1.3,width =interface.winfo_screenwidth()+50, height=interface.winfo_screenheight()/24).place(relx=1,rely=0.04,anchor='ne')

    tk.Label(bar,bg="#BB0F37",fg="#FFFFFF",text="LOADING . . .",font="Helvetica 16 bold").place(relx=0.5,rely=0.06,anchor="center")

    interface.update()

    task = [ cnn() , bbc() , alj() ]
    loop.run_until_complete(asyncio.wait(task))

    same = headline
    same.text = ""
    similar = []

    user_res = title.get().lower()
    for entries in news:
        if entries.text.lower() == user_res:
            same = entries

    user_res = " " + user_res
    for word in stopwords.words("english")+['the']:
        user_res = user_res.replace(" "+word+" "," ")
    for symbol in punctuation:
        user_res = user_res.replace(symbol,"")

    user_res = user_res.split()
    for entries in news:
        for word in user_res:
            if word in entries.text.lower():
                similar.append(entries)
                break

    results = tk.Frame(interface,bg="#D4355A",width =interface.winfo_screenwidth()+15,border=1.3,relief="ridge",height=interface.winfo_screenheight()+15).place(relx=1,rely=0.015,anchor='ne')

    scroll = tk.Scrollbar(results)
    scroll.pack(side="right",fill = "y")

    line = tk.Text(results,font="Helvetica 15 bold",bg="#D4355A",fg="#FFFFFF",width=130, height=32.45,yscrollcommand = scroll.set,border=0)


    posted = []

    if len(same.text) > 0:
        line.insert("insert","Exact Match Found:\n")
        line.insert("insert","  "+same.text+" -"+same.publisher+"\n\n")
        posted.append(same.text)
    else:
        line.insert("insert","No Exact Match Found\n\n")

    if len(similar) > 0:
        line.insert("insert","Similar News Found:\n")
        for x in range(len(similar)):
            if similar[x].text not in posted:
                line.insert("insert","  "+similar[x].text.capitalize()+" - "+similar[x].publisher+"\n")
                posted.append(similar[x].text)
    else:
        line.insert("insert","No Similar News Found\n\n")

    line.place(relx=0.01,rely=0.02)
    scroll.config(command=line.yview)

#Main Function

interface = tk.Tk()

interface.title("Credibility Check")

interface.minsize(width=interface.winfo_screenwidth(), height=interface.winfo_screenheight()+100)
interface.maxsize(width=interface.winfo_screenwidth(), height=interface.winfo_screenheight()+100)

interface["bg"] = "#9B0024"

bgimg = tk.PhotoImage(file="bgimg1.png")

card1 = tk.Frame(interface,bg="#D4355A",width =interface.winfo_screenwidth()-15,border=1.3,relief="ridge",height=interface.winfo_screenheight()+15).place(relx=0.995,rely=0.015,anchor='ne')
tk.Label(card1,image=bgimg,width=interface.winfo_screenwidth()-30, height=interface.winfo_screenheight()+10).place(relx=0.991,rely=0.020,anchor='ne')
card2 = tk.Frame(card1,bg="#BB0F37",relief="raised",border=1.3,width =interface.winfo_screenwidth()+50, height=interface.winfo_screenheight()/24).place(relx=1,rely=0.04,anchor='ne')

tk.Label(card2,bg="#BB0F37",fg="#FFFFFF",text="Headline:",font="Helvetica 16 bold").place(relx=0.45,rely=0.043,anchor='ne')

title = tk.Entry(card2,fg="#BB0F37",font="Helvetica 15 bold")
title.place(relx=0.6,rely=0.045,anchor="ne")


button = tk.Button(card2,border=1.5,text="Submit",fg="#FFFFFF",bg="#005868",font="Helvetica 15 bold",relief="groove",command=onbuttonclick).place(relx=0.53,rely=0.09,anchor="ne")

interface.mainloop()
loop.close()

#End Of Programne
