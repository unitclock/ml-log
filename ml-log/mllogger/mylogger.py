
from .status import NewStatus
from .clinet import NewClientConn
from .path import GetStoragePath,GetRunPath,GetPM
from .utils import single,format_time,has_multiple_keys,new_experiment_id
import random
import time
from .watcher import NewCpuWatcher,NewGpuWatcher

@single
class Logger(object):
    def __init__(self,config:dict)->None:
        if not has_multiple_keys(config, 'access_token', 'project',"description","experiment_name"):
            raise BaseException("Params Missing: access_token project description experiment (repository_id)")
        config["experiment_id"] = new_experiment_id()
        self.__config = config
        self.__config["experiment_name"] = f'{self.__config["experiment_name"]}-{format_time()}'
        self.__status = NewStatus(config=self.__config)
        self.__client = NewClientConn(config=self.__config)
        self.__client.ShakeHand()
        return
    def Start(self,info:dict)->None:
        self.__client.NoticeExpStart()
        self.__start_tag()
        self.__pm = GetPM()
        return
    def Run(self)->None:
        self.__client.NoticeRunStart()

        self.__cpu_watcher = NewCpuWatcher()
        self.__cpu_watcher.start()
        self.__gpu_watcher = NewGpuWatcher()
        self.__gpu_watcher.start()
        self.__run_start_tag()
        return
    def Log(self,statu:dict):
        self.__status.Log(statu=statu)
        return
    def End(self)->None:
        rp = GetRunPath()
        self.__status.WriteToDisk(rp=rp)
        self.__client.NoticeRunStop()
        self.__run_finish_tag()
        pass
    def Submit(self)->None:
        self.__finish_tag()
        self.__client.NoticeExpStop
        return
    def __finish_tag(self)->None:
        path = GetStoragePath()
        with open(path+"/finish.tag","a") as file:
            file.write(format_time())
            file.flush()
        return
    def __start_tag(self)->None:
        path = GetStoragePath()
        with open(path+"/start.tag","a") as file:
            file.write(format_time())
            file.flush()
        return
    def __run_start_tag(self)->None:
        path = GetRunPath()
        with open(path+"/start.tag","a") as file:
            file.write(format_time())
            file.flush()
        return
    def __run_finish_tag(self)->None:
        path = GetRunPath()
        with open(path+"/finish.tag","a") as file:
            file.write(format_time())
            file.flush()
        return
    



    

