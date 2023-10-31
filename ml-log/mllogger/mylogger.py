
from status import NewStatus
from clinet import NewClientConn
from path import NewPathManager
from utils import single,format_time,has_multiple_keys,new_experiment_id
import random
import time

@single
class Logger(object):
    def __init__(self,config:dict)->None:
        if not has_multiple_keys(config, 'access_token', 'project',"description","experiment_name"):
            raise BaseException("缺失启动信息,请补充config参数: access_token project description experiment ;可选配置项: repository_id")
        config["experiment_id"] = new_experiment_id()
        config["experiment_name"] = f'{self.__config["experiment_name"]}-{format_time()}'
        self.__config = config
        self.__status = NewStatus()
        self.__client = NewClientConn()
        
        return
    def Start(self,info:dict)->None:
        
        return
    def Run(self)->None:
        
        pass
    def End(self)->None:
        pass
    
    def Submit(self)->None:
        pass
    



    

