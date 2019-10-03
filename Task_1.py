from bs4 import BeautifulSoup
from urllib.request import urlopen
import sqlite3
conn = sqlite3.connect('localdb.sqlite')
cur = conn.cursor()
cur.execute('create table if not exists events(id integer primary key autoincrement,title text,conducted_by text,start_date text,end_date text,Location text,Price text,No_of_Views text, Description text)')
try:
    url = 'https://www.eventshigh.com/city/'+input("Enter City Name in small letters:")
    html = urlopen(url).read()
    soup = BeautifulSoup(html, "html.parser")
    tags = soup('a')
    
except:
    pass
count = 0
for tag in tags:
    val = tag.get('href',None)
    if(val is None):
        continue
    elif(val.startswith("/detail")):
         url = 'https://www.eventshigh.com'+val
    else:
        continue
    if(count>10):
        break
    count += 1
    html = urlopen(url).read()
    soup = BeautifulSoup(html, "html.parser")
    details = soup.find("div",{"class":"eh-main-details-container row"})
    try:
        descrip = soup.find("div",{"class":"eh-detail-slab-data-note"}).text
    except:
        descrip = ""
#print(BeautifulSoup.prettify(details))

    title = details.find("div",{"class":"eh-heading"}).text
    by = details.find("div","eh-table-row").text
    by = by[4:len(by)-9]
    i=0
    for result in details.find_all("div",{"class":"eh-main-details-desc"}):
        if(i==0):
            date = result.text
        elif(i==1):
            location = result.text.strip()
        elif(i==2):
            price = result.text.strip()
        elif(i==3):
            viewed = result.text.split(" ")[0]
        i += 1
    st_date = date.split("-")[0].strip()
    temp = date.split("-")[1].split(":")
    en_date = (temp[0]+":"+temp[1][:4]).strip()
    print(title)
    cur.execute('insert into events(title,conducted_by,start_date,end_date,Location,Price,No_of_Views,Description) values(?,?,?,?,?,?,?,?);',(title,by,st_date,en_date,location,price,viewed,descrip))
    print(by)
    print(st_date)
    print(en_date)
    print(location)
    print(price)
    print(viewed)
    print(descrip)
conn.commit() 
