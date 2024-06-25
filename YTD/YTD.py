
import customtkinter as ctk
from tkinter import ttk
from pytube import YouTube
from pytube import Playlist
from datetime import datetime as dt
import os
from kivy.core.clipboard import Clipboard as Cb

def Button_clicked(hurl = None):
    url = hurl
    if url == None:
    	url = entry_url.get()
    queue = []
    sub = ""

    progress_bar.pack(pady=(10, 5))
    progress_label.pack(pady=(10, 5))
    status_label.pack(pady=(10, 5))

    if "playlist?list=" in url:
        p = Playlist(url)
        sub = "/" + p.title
        for suburl in list(p.video_urls):
            queue.append(suburl)
    else: queue.append(url)

    for i in range(len(queue)):
        status_label.configure(text=f"Downloading video {i + 1} of {len(queue)}")
        Download_video(queue[i], sub)

def Download_video(next, sub=""):
    try:
        yt = YouTube(next, on_progress_callback=on_progress)
        ##stream = yt.streams.first()
        stream = yt.streams.filter(only_audio=True).first()
        
        #download
        pathos = os.path.join("downloads" + sub)
        stream.download(output_path = pathos)
        
        neim = "/" + yt.title + ".mp4"
        niem = "/" + yt.title + ".mp3"
        os.rename(pathos + neim, pathos + niem)

        status_label.configure(text="Success")
    except Exception as e:
        status_label.configure(text=f"Error {str(e)}", text_color="white", fg_color="red")

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    progress = bytes_downloaded / total_size
    
    print(f"progress: {progress}")

    progress_label.configure(text=str(int(100*progress)) + "%")
    progress_label.update()

    progress_bar.set(progress)

def Paste_from_clipboard():
	Button_clicked(Cb.paste())

#create root window
root = ctk.CTk()
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

#title
root.title("YTD")

#scale bounds
root.geometry("600x800")
root.minsize(600, 800)

#attributes
root.attributes("-fullscreen", "True")

#create content frame
content_frame = ctk.CTkFrame(root)
content_frame.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)

title = ctk.CTkLabel(content_frame, text="YTD")
title.pack(pady=(10,5))
title.cget("font").configure(size=50)

#create label and entry widget
url_label = ctk.CTkLabel(content_frame, text="Enter YT video link or playlist link (will download ALL content on playlist, may not work on private or unlisted playlists).")
entry_url = ctk.CTkEntry(content_frame, width=400, height=40)
url_label.pack(pady=(10, 5))
entry_url.pack(pady=(10, 5))

#create button
download_button = ctk.CTkButton(content_frame, text="Download", command=Button_clicked)
download_button.pack(pady=(10, 5))

#paste from clipboard
paste_button = ctk.CTkButton(content_frame, text="Paste from clipboard", command=Paste_from_clipboard)
paste_button.pack(pady=(10, 5))

#progress label and bar
progress_label = ctk.CTkLabel(content_frame, text="paste: " + str(Cb.paste()))
progress_label.pack(pady=(10,5))
progress_bar = ctk.CTkProgressBar(content_frame, width=400)
progress_bar.set(0)


#create status
status_label = ctk.CTkLabel(content_frame, text="")



#start main
root.mainloop()