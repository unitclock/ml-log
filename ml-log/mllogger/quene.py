from multiprocessing import Queue as Q

#消息管理基类
class Quene():
    def __init__(self):
        self.__quene = Q(maxsize=0)
        return
    def SetLen(self,length:int) ->None:
        __new_quene = Q(maxsize=length)
        while not self.__quene.empty():
            __new_quene.put(self.__quene.get())
        self.__quene = __new_quene
        return
    def Read(self)->None:
        return
    def Write(self) ->None:
        return
    def GetLen(self) ->int:
        return self.__quene.qsize()