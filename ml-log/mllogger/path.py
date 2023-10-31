import utils 
import quene
from multiprocessing import Queue

@utils.single
class PathManager(object):
    def __init__(self,config:dict):
        self.__quene = NewPathQuene()
        self.__quene.SetLen(1)
        return
    def GetRunPath()->str:
        
        return
    def NewRunPath()->str:
        return
    
def NewPathManager() -> PathManager:
    return PathManager()

@utils.single
class PathQuene(quene.Quene):
    def __init__(self) ->None:
        super().__init__()
    def Read(self) -> str:
        p = self.__quene.get()
        return p
    def Write(self,path:str) ->None:
        self.__quene.put(path)
        return
    def OnlyRead(self)->None:
        p = self.__quene.get()
        self.Write(p)
        return p 
    def SetLen(self, length: int) ->None:
        super().SetLen(length)
        return
    def GetLen(self) -> int:
        return super().GetLen()
                
def NewPathQuene():
    return PathQuene()
    