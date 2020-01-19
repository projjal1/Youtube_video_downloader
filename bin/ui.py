from __future__ import unicode_literals
from tkinter import *
from PIL import ImageTk,Image
import os
import youtube_dl
from tkinter.ttk import *
from tkinter import filedialog
import threading as t

root=Tk()
root.title("Youtube Video Downloader")

track=IntVar() #Keeps track of music content no.
type=StringVar()  #Track of single vid/playlist/channel

value1=StringVar()
value2=StringVar()
value3=StringVar()
value4=StringVar()  #Error tracking code

progress=Progressbar(root, orient = HORIZONTAL,length = 250, mode = 'determinate')

#Logger class
class MyLogger(object):
    def debug(self, msg):
        pass
    def warning(self, msg):
        pass
    def error(self, msg):
        value4.set("Video is blocked or internet lost. Cannot proceed further.")
        root.update_idletasks()

#Hook class to control events
def my_hook(d):
    if d['status'] == 'finished':
        value1.set('Download done, converting #'+str((track.get()+1)//2))
        track.set(track.get()+1)
        root.update_idletasks() 
    elif d['status']=='downloading':
        prog=float(d['_percent_str'][:-1])
        prog=int(prog)
        progress['value']=prog
        root.update_idletasks() 

#Checks url for playlist, channel, or single video
def check(url):
    if 'user' in url or 'channel' in url:
        type.set('channel')
        value3.set("Downloading complete channel's content")
    elif 'playlist' in url:
        type.set('playlist')
        value3.set("Downloading complete playlist content")
    else:
        if '&list' in url:
            pos=url.index('&list')
            url=url[:pos]
        type.set('single')
        value3.set("Single Video download content")
    root.update_idletasks() 
    return url

#Download code for content
def download():
    value1.set("")
    value2.set("")
    root.update_idletasks()

    opt=val.get()

    url=e1.get()

    url=check(url)

    base_path=folder_select()

    ydl_opts={}

    if(opt==1):
        ydl_opts={
            'format': 'bestaudio/best',
            'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            }],
            'outtmpl': base_path+'/%(title)s.%(ext)s',
            'logger':MyLogger(),
            'progress_hooks': [my_hook]}
    
    elif(opt==2):
        ydl_opts = {
            'outtmpl': base_path+'/%(title)s.%(ext)s',
            'logger':MyLogger(),
            'progress_hooks': [my_hook]}   
    else:
        return
        
    track.set(1) #Initialy we download content no. 1 (channel/playlist/single) 

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        root.update_idletasks() 
        ydl.download([url])

    value2.set('All videos downloaded and processes completed...')
    track.set(0)
    value3.set("")

#Destination folder select
def folder_select():
    folder_dir=filedialog.askdirectory()
    return folder_dir

#Multithread handler to prevent unresponsiveness
def download_handler():
    thread=t.Thread(target=download)
    thread.start()

Label(root,text="This software is OpenSource and made for distribution",font="bold",background="yellow",foreground="red").grid(row=1,columnspan=2)

img1 = ImageTk.PhotoImage(Image.open("logo.png").resize((500,250)))
panel1 = Label(root, image = img1).grid(row=2,column=0)

img2 = ImageTk.PhotoImage(Image.open("dn.png").resize((300,150)))
panel2=Label(root,image=img2).grid(row=2,column=1)

Label(root,text="Enter the url of playlist,channel or single video below",font="bold",foreground="blue").grid(row=4,columnspan=2)
e1=Entry(root,width=100,background="grey")
e1.grid(row=5,columnspan=2,pady=5)

Label(root,textvariable=value4,foreground="red").grid(row=7,pady=10,columnspan=2)

Button(text="Start to Download files",command=download_handler).grid(row=8,columnspan=2,pady=20)

val=IntVar()
r1=Radiobutton(root,text="Audio only",value=1,variable=val).grid(row=9,columnspan=1)
r2=Radiobutton(root,text="Video File",value=2,variable=val).grid(row=9,columnspan=2)

Label(root,textvariable=value3,foreground="red").grid(row=10,pady=10,columnspan=2)

Label(root,textvariable=value1,foreground="red").grid(row=11,pady=10,columnspan=2)

Label(root,text="Download Progress (single/channel/playlist):- ").grid(row=12)
progress.grid(row=12,column=1)

Label(root,textvariable=value2,foreground="red",font="bold").grid(row=13,pady=10,columnspan=2)

Label(root,text="@Copyright Under GNU license. Made by Projjal Gop using Open Frameworks.",font="bold").grid(row=14,pady=30,columnspan=2)

root.mainloop()
