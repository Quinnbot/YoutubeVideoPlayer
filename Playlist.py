
class Playlist:
    def __init__(self, name) -> None:
        self.name=name
        self.URLList=[]
        self.PlaylistPos=0
        self.PercentPos=0
    
    def Remove(self, url):
        pass

    def Remove(self, index):
        pass

    def Add(self, url):
        self.URLList.append(url)

    def Shuffle(self):
        pass
    def Current(self):
        return self.URLList[self.PlaylistPos]
    def Next(self):
        print(self.PlaylistPos)
        if self.PlaylistPos < len(self.URLList)-1:
            self.PlaylistPos+=1
        else:
            self.PlaylistPos = 0
        return self.URLList[self.PlaylistPos]

    def Previous(self):
        if self.PlaylistPos > 0:
            self.PlaylistPos-=1
        return self.URLList[self.PlaylistPos]

    def ToString(self):
        return ", ".join(self.URLList)