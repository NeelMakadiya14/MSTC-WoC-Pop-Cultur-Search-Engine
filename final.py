from tkinter import *
from functools import partial
import urllib.request
import bs4
import json
import numpy as np
import cv2

window=Tk()
window.title("Movie/Series Information")
window.configure(background='gray25')
window.geometry("1900x950")

output=Message()
output1=Message()


def url_image(url):
    resp = urllib.request.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    img= cv2.imdecode(image, -1)
    cv2.imshow('URL Image', img)
    cv2.waitKey()

def movie_info():
    name=namebox.get() 
    year=yearbox.get()

    if year=='':
        url="http://www.omdbapi.com/?t="+name.replace(" ","+")+"&r=json&plot=full&apikey=fdb54f51"
    else:
        url="http://www.omdbapi.com/?t="+name.replace(" ","+")+"&r=json&y="+year+"&plot=full&apikey=fdb54f51"
    source=urllib.request.urlopen(url).read()
    json_data=json.loads(source)
    json_to_info(json_data)

def Actors_pic(json):
    actors=(json['Actors']).split(',')
    for i in range(len(actors)):
        source=urllib.request.urlopen("https://en.wikipedia.org/wiki/"+actors[i].replace(" ","_"))
        soup=bs4.BeautifulSoup(source,"lxml")
        div=soup.find('a',class_='image')
        image=div.find("img")
        img_url='https:'+image.get("src")
        url_image(img_url)

def save(file,json):
    file=file+".sqlite"

    import sqlite3
    conn=sqlite3.connect(file)
    cur=conn.cursor()

    Title=json['Title']
    Released_Date=json['Released']
    Imdb_Rating=json['imdbRating']
    Type=json['Type']
    Duration=json['Runtime']
    Genre=json['Genre']
    Director=json['Director']
    Writer=json['Writer']
    Actors=json['Actors']
    Plot=json['Plot']
    Language=json['Language']
    Country=json['Country']
    Awards=json['Awards']

    cur.execute('''CREATE TABLE IF NOT EXISTS Movie_Info(Title,ReleasedDate TEXT,ImdbRating REAL,Type TEXT,Duration REAL,Genre TEXT,Director TEXt,Writer TEXT,Actors TEXT,Plot TEXT,Language TEXT,Country TEXt,Awards TEXt,BoxOffice_Collection TEXT,Production TEXT,Total_Seasons TEXT)''')
 
    if json['Type']=='movie':
        BoxOffice=json['BoxOffice']
        Production=json['Production']
        #cur.execute('ALTER TABLE Movie_Info ADD COLUMN BoxOffice_Collection TEXT')
        #cur.execute('ALTER TABLE Movie_Info ADD COLUMN Production TEXT')
        params=(Title,Released_Date,Imdb_Rating,Type,Duration,Genre,Director,Writer,Actors,Plot,Language,Country,Awards,BoxOffice,Production)
        cur.execute('''INSERT INTO Movie_Info(Title,ReleasedDate,ImdbRating,Type,Duration,Genre,Director,Writer,Actors,Plot,Language,Country,Awards,BoxOffice_Collection,Production)VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',params)
        conn.commit()
    else:
        Season=json['totalSeasons']
        #cur.execute('ALTER TABLE Movie_Info ADD COLUMN Total_Seasons TEXT')
        params=(Title,Released_Date,Imdb_Rating,Type,Duration,Genre,Director,Writer,Actors,Plot,Language,Country,Awards,Season)
        cur.execute('''INSERT INTO Movie_Info(Title,ReleasedDate,ImdbRating,Type,Duration,Genre,Director,Writer,Actors,Plot,Language,Country,Awards,Total_Seasons)VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',params)
        conn.commit()

    conn.close ()  


def save_in_database(json):
    window1=Tk()
    window1.title("Saving Data...")
    window1.configure(background='ivory3')

    Label(window1,text='Enter Name :').pack(side=LEFT)
    text=Entry(window1,width=20)
    text.pack(side=LEFT)
    Button(window1,text="Save",bg='maroon3',command=lambda: save(text.get(),json)).pack(side=BOTTOM)

    window1.mainloop()

    
def json_to_info(json):

    #output=Text(window,width='100',height='20',bg='white',wrap=WORD)
    #output.grid(row=6,column=0,columnspan=10,sticky=W) 
    #output.insert(END,json)  


    if json['Type']=='movie':
        output1=Message(window,fg='OliveDrab1',bg='gray25',width=1000,text=f" \n Imdb Rating : {json['imdbRating']} \n BoxOffice Collectino : "+json['BoxOffice']+ "\n Production : " + json['Production']+ "\n ",font='none 11 italic')
        output1.grid(row=7,column=1,columnspan=46)
    else:
        output1=Message(window,fg='OliveDrab1',bg='gray25',width=1000,text=f"\n Imdb Rating : {json['imdbRating']} \n Total Season : {json['totalSeasons']}\n",font='none 11 italic')
        output1.grid(row=7,column=1,columnspan=46)
    
    output=Message(window,width=1000,fg='OliveDrab1',bg='gray25',text=f"\n Released Date : {json['Released']}  \n Type : {json['Type']} \n Duration : {json['Runtime']} \n Genre : {json['Genre']} \n\n Director : {json['Director']} \n Writer : {json['Writer']} \n Actors : {json['Actors']} \n\n Plot : {json['Plot']}  \n\n Language : {json['Language']}  \n Country : {json['Country']} \n Awards : {json['Awards']}",font='none 11 italic')
    output.grid(row=8,column=1,columnspan=46)
            
    Button(window,text='Wanna see the pics of starcast',command=lambda: Actors_pic(json),bg='maroon3',width=30,font='none 13 italic').grid(row=9,column=1,sticky=W,padx=10,ipadx=25,pady=5,columnspan=7)
    Button(window,text='Save Data',command=lambda: save_in_database(json),bg='maroon3',width=10,font='none 13 italic').grid(row=9,column=9,sticky=W,padx=10,ipadx=25,pady=5,columnspan=4)
    Button(window,text='Exit',command=lambda: Exit(window),bg='maroon3',width=10,font='none 13 italic').grid(row=9,column=14,sticky=W,padx=10,ipadx=25,pady=5,columnspan=5)

    def Exit(window):
        window.destroy()
        exit()

def fun(i,search_list,button):
    #print(i,search_list)
    for but in button:
        but.grid_forget()
    id=search_list[i-1][7:16]
    url="http://www.omdbapi.com/?i="+id+"&plot=full&r=json&apikey=fdb54f51"
    source=urllib.request.urlopen(url).read()
    json_data=json.loads(source)
    if json_data['Poster']!='N/A':
        img=json_data['Poster']
        url_image(img)
    json_to_info(json_data)

    
def name_to_list_info():

    name=namebox.get()
    url1='https://www.imdb.com/find?ref_=nv_sr_fn&q='+name.replace(" ","+")+'&s=all'
    source1=urllib.request.urlopen(url1).read()
    soup1=bs4.BeautifulSoup(source1,'lxml')
    

    i=1
    search_list=[]
    subdiv=soup1.find('div',class_='findSection')
    button=list()
    for div in subdiv.find_all('td',class_="result_text"):
        link=div.find('a')
        search_list.append(link.get('href'))
        movie_name=str(i)+'.'+div.text
        button.append(Button(window,bg='royal blue',text=movie_name,width='70',command=partial(fun,i,search_list,button)))
        button[-1].grid(row=4+i,column=1,sticky=W,columnspan=10,ipadx=25,pady=5)
        i=i+1    


def name_to_json():
    
    output.grid_forget()
    output1.grid_forget()

    name=namebox.get()
    year=yearbox.get()

    if year=='':
        url="http://www.omdbapi.com/?t="+name.replace(" ","+")+"&r=json&plot=full&apikey=fdb54f51"
    else:
        url="http://www.omdbapi.com/?t="+name.replace(" ","+")+"&r=json&y="+year+"&plot=full&apikey=fdb54f51"
    source=urllib.request.urlopen(url).read()
    json_data=json.loads(source)
    
    if json_data['Response']=='True':

        if json_data['Poster']!='N/A':
            img=json_data['Poster']
            url_image(img)
            Label(window,text="Is this expected output yes or no ?",bg='gray25',fg='firebrick1',font='none 15 italic',width='30').grid(row=3,column=1,sticky=W,columnspan=7,pady=5)
            
            Button(window,text='Yes',width='3',command=movie_info,bg='maroon3').grid(row=3,column=10,sticky=W,padx=10,ipadx=25,pady=5)
            Button(window,text='No',width='3',command=name_to_list_info,bg='maroon3').grid(row=3,column=12,sticky=W,padx=20,ipadx=25,pady=5)

    else:
        name_to_list_info()
        
Label(window,bg='sienna1',text='Pop Culture Search Engine',fg='dark slate blue',font='none 40 italic',width=50).grid(row=1,column=0,columnspan=46,pady=40,ipady=20)
Label(window,bg='medium spring green',height=50,width=5).grid(row=1,rowspan=50,column=0,padx=5)
Label(window,bg='medium spring green',height=50,width=5).grid(row=1,rowspan=50,column=43,padx=5)

Label(window,text="Enter the movie or series name : ",bg='gray25',fg='firebrick1',font='none 15 italic',width=29).grid(row=2,column=1,columnspan=8,sticky=W,pady=5)
namebox=Entry(window,width=80,bg='ivory2')
namebox.grid(row=2,column=10,sticky="",columnspan=15,pady=5)

Label(window,bg='gray25',width=5).grid(column=26,row=2,columnspan=4)

Label(window,text="Enter the year :",bg='gray25',fg='firebrick1',font='none 15 italic',width=16).grid(row=2,column=31,sticky=W,columnspan=8,pady=5)
yearbox=Entry(window,width=8,bg='ivory2')
yearbox.grid(row=2,column=40,sticky=W,pady=5)


Button(window,text='Search',width='6',command=name_to_json,bg='firebrick1').grid(row=2,column=41,sticky=W,ipadx=25,padx=30,pady=5)

window.mainloop()
