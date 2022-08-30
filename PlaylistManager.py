from Playlist import Playlist
import pickle

class PlaylistManager:
    def __init__(self) -> None:
        self.WorkingPlaylistIndex = 0
        try:
            self.Load()
            print("loaded playlist")
            print(self.GetList().ToString())
        except Exception as E:
            print("loading playlists failed. reason: {}".format(E))
            self.LoadDefault()
    
    def Load(self):
        self.playlists = pickle.load(open("cache\\lists.playlist", "rb"))

    def Save(self):
        pickle.dump(self.playlists, open("cache\\lists.playlist", "wb+"))

    def LoadDefault(self):
        self.playlists = []
        t = Playlist("Default ;)")
        t.Add("https://www.youtube.com/watch?v=dQw4w9WgXcQ&t")
        self.playlists.append(t)
        self.Save()
        print(self.playlists)
        
    def AddPlaylist(self, playlist:Playlist):
        self.playlists.append(playlist)

    def SetWorkingPlaylist(self, index=0):
        self.WorkingPlaylistIndex = index

    def Remove(self, url : str):
        
        self.playlists[self.WorkingPlaylistIndex].Remove(url)

    def Add(self, url):
        self.playlists[self.WorkingPlaylistIndex].Add(url)

    def Shuffle(self):
        pass
    
    def SetPercentPos(self, percent):
        self.playlists[self.WorkingPlaylistIndex].PercentPos = percent

    def GetPercentPos(self):
        return self.playlists[self.WorkingPlaylistIndex].PercentPos

    def Current(self):
        return self.playlists[self.WorkingPlaylistIndex].Current()

    def Next(self):
        return self.playlists[self.WorkingPlaylistIndex].Next()

    def Previous(self):
        return self.playlists[self.WorkingPlaylistIndex].Previous()

    def GetList(self) -> Playlist:
        return self.playlists[self.WorkingPlaylistIndex]
    
    def ToString(self):
        return ", ".join(self.URLList)
        
if __name__ == "__main__":
    plm = PlaylistManager()
    plm.Load()

    plm.Save()
