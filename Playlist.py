
class Playlist:
    def __init__(self, name) -> None:
        self.name=name
        self.URLList=[]
        self.MetaData=[]
        self.PlaylistPos=0
        self.PercentPos=0
    
    def Remove(self, url : str):
        self.URLList.remove(url)
        print("test")
        pass

    def Add(self, url):
        self.URLList.append(url)

    def Shuffle(self):
        pass

    def Current(self):
        return self.URLList[self.PlaylistPos]

    def Next(self):
        if self.PlaylistPos < len(self.URLList)-1:
            self.PlaylistPos+=1
        else:
            self.PlaylistPos = 0
        return self.URLList[self.PlaylistPos]

    def Previous(self):
        if self.PlaylistPos > 0:
            self.PlaylistPos-=1
        return self.URLList[self.PlaylistPos]

    def GetPlaylist(self):
        return self.URLList

    def ToString(self):
        return ", ".join(self.URLList)