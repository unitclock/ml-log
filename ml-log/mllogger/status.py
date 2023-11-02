from .path import GetRunPath
class Status():
    def __init__(self,config:dict) ->None:
        self.__config = config
        self.__status = {}
        return
    def Log(self,statu:dict) ->None:
        rp = GetRunPath()
        if not rp in self.__status.keys():
            self.__status[rp] = []
        self.__status[rp].append(statu)
        return
    def WriteToDisk(self,rp:str) ->None:
        print(self.__status)
        return


def NewStatus(config:dict) ->Status:
    return Status(config=config)