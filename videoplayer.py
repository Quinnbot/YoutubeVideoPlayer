from cProfile import label
from logging.handlers import WatchedFileHandler
import tkinter as tk
from youtube_dl import YoutubeDL as ytdl
from ScrollableFrame import ScrollableFrame
import mpv
import os
from PlaylistManager import PlaylistManager
from Playlist import Playlist

class VideoPlayer:

    def __init__(self):
        self.root = tk.Tk()
        self.root.grid_columnconfigure(0,weight=1)
        self.root.grid_rowconfigure(3,weight=1)
        self.startupComplete = None
        self.PLM = PlaylistManager()
        self.BuildUI()
        self.BuildHooks()
        # self.ResumePlayback()

    def BuildUI(self):
        self.playerFrame = tk.Frame(self.root, background="black", height=500)
        self.playerFrame.grid(row=0,sticky="nesw")
        self.player = mpv.MPV(wid=str(int(self.playerFrame.winfo_id())), input_default_bindings=True,input_vo_keyboard=True,osc=True)

        #playback control buttons
        self.ControlFrame = tk.Frame(self.root, background="grey", height=50)
        self.ControlFrame.grid(row=1,sticky="nesw")
        self.ControlFrame.grid_columnconfigure(4,weight=1)
        self.ControlFrame.grid_rowconfigure(2,weight=1)

        self.PlaybackButton = tk.Button(self.ControlFrame, text="play/pause",command=self.TogglePlayback).grid(column=2,row=0,sticky="nesw")
        self.NextButton = tk.Button(self.ControlFrame, text=">", command=self.Next).grid(column=3,row=0,sticky="nesw")
        self.PreviousButton = tk.Button(self.ControlFrame, text="<", command=self.Previous).grid(column=1,row=0,sticky="nesw")

        self.UrlEntryValue = tk.StringVar()
        self.UrlEntry = tk.Entry(self.ControlFrame, textvariable=self.UrlEntryValue).grid(column=4,row=1,sticky="nesw")
        self.AddToPlaylistButton = tk.Button(self.ControlFrame, text="Add", command=lambda : self.AddToPlaylist(self.UrlEntryValue.get()) ).grid(column=4,row=0,sticky="nesw")
        
        self.Volume = tk.DoubleVar(value=50)
        self.SetVolume(40)
        self.VolumeBar = tk.Scale(self.ControlFrame, from_=0, to=100, orient=tk.HORIZONTAL, variable=self.Volume, command=self.SetVolume).grid(column=3,row=1,sticky="nesw")

        #track bar
        self.PercentPos = tk.DoubleVar()
        self.TrackBar = tk.Scale(self.root, from_=0, to=100, orient=tk.HORIZONTAL, variable=self.PercentPos, command=self.SetPlaybackPos ).grid(row=2,sticky="nesw")

        #playlist half
        self.PlaylistFrame = ScrollableFrame(self.root)
        self.PlaylistFrame.grid(row=3,sticky="nesw")

        self.UpdatePlaylistUI()

    def ResumePlayback(self):
        if  self.startupComplete == None:
            self.startupComplete = False
            self.player.play(self.PLM.Current())
            self.TogglePlayback()

        if self.PLM.GetPercentPos() != 0:
            try:
                self.player._set_property("percent-pos", self.PLM.GetPercentPos())
                self.startupComplete = True
            except:
                print("retry failed, trying again in one second")
                self.root.after(1000, self.ResumePlayback)
        else:
            self.startupComplete = True

    def BuildHooks(self):
        self.root.protocol("WM_DELETE_WINDOW", self.OnClose)
        self.player.observe_property("percent-pos", handler=self.OnPositionChange)

    def SetPlaybackPos(self, SeekTo):
        self.player._set_property("time-pos", SeekTo)

    def OnPositionChange(self, name, percent):
        if percent != None and (self.startupComplete and self.startupComplete != None):
            self.PLM.SetPercentPos(percent)
            self.PercentPos.set(percent)
        if percent != None and(self.player._get_property("playtime-remaining") < .5):
            print("go next")
            self.Next()

    def OnClose(self):
        self.PLM.Save()
        self.root.destroy()

    def UpdatePlaylistUI(self):
        for widgets in self.PlaylistFrame.scrollable_frame.winfo_children():
            widgets.destroy()
        
        with ytdl() as ydl:
            for url in self.PLM.GetList().GetPlaylist():
                title = None
                if "youtube" in url:
                    info_dict = ydl.extract_info(url, download=False,)
                    title = info_dict.get("title", None)
                elif "tiktok" in url:
                    title = "TokTok Short"
                else:
                    title = url
                
                frame = tk.Frame(self.PlaylistFrame.scrollable_frame, background="black", border=10)
                frame.grid_columnconfigure(2, weight=1)
                tk.Button(frame, text="X", command= lambda URL = url : self.RemoveURL(URL)).grid(row=0, column=0)
                tk.Label(frame, text=title).grid(row=0, column=1)
                frame.pack(fill="both")

    def RemoveURL(self, URL):
        self.PLM.Remove(URL)
        self.UpdatePlaylistUI()
        self.player.play(self.PLM.Current())

    def AddToPlaylist(self, url):
        self.PLM.Add(url)
        self.PLM.Save()
        self.UrlEntryValue.set("")
        self.UpdatePlaylistUI()

    def TogglePlayback(self):
        if self.player._get_property("percent-pos") != None:
            self.player.command('keypress', 'space')
    
    def Next(self):
        # self.player.command("stop", "")
        self.player.play(self.PLM.Next())
    
    def Previous(self):
        if self.player._get_property("time-pos") > 3:
            self.player._set_property("time-pos", 0)
        elif self.player._get_property("time-pos") <= 3:
            self.player.play(self.PLM.Previous())
    
    def SetVolume(self, Volume):
        self.player._set_property("volume", Volume)
        
        

if __name__ == "__main__":
    vp = VideoPlayer()
    vp.ResumePlayback()
    vp.root.mainloop()