from Playlist import Playlist
import pickle

class PlaylistManager:
    def __init__(self) -> None:
        try:
            self.Load()
            print("loaded playlist")
        except Exception as E:
            print("loading playlists failed. reason: {}".format(E))
            self.playlists=[]
            self.Save()
        
        self.WorkingPlaylistIndex = 0
    
    def Load(self):
        self.playlists = pickle.load(open("PLS\\lists.playlist", "rb+"))

    def Save(self):
        pickle.dump(self.playlists, open("PLS\\lists.playlist", "wb+"))

    def AddPlaylist(self, playlist:Playlist):
        self.playlists.append(playlist)

    def SetWorkingPlaylist(self, index=0):
        self.WorkingPlaylistIndex = index

    def Remove(self, url):
        pass

    def Remove(self, index):
        pass

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

    def GetList(self):
        return self.playlists[self.WorkingPlaylistIndex]
    
    def ToString(self):
        return ", ".join(self.URLList)
        
if __name__ == "__main__":
    plm = PlaylistManager()
    plm.Load()
    pl = Playlist("default")
    pl.Add("https://www.youtube.com/watch?v=tSvkKcyQMVU")
    pl.Add("https://www.youtube.com/watch?v=ScHzMnAcn_s")
    plm.AddPlaylist(pl)

    plm.Save()
