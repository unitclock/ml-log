from multiprocessing import Process
from .path import NewCpuFilePath,GetCpuFilePath,NewGpuFilePath,GetGpuFilePath,PM
import time
import psutil
from .format import Formater
import pynvml


class CpuWatcher(Process):
    def __init__(self, name=""):
        print(1)
        super(CpuWatcher,self).__init__()
        if name:
            self.name = name
        self.__cpu_log_count = 0
    def run(self):
        print("Start Cpu Watching Process:", self.name)
        self.daemon = True  
        self.cpu_watch_loop()
        print("Exiting Cpu Watching Process:", self.name)
    def start(self) -> None:
        print(2)
        return super().start()
    def close(self) -> None:
        return super().close()
    def cpu_watch_loop(self):
        NewCpuFilePath()
        _gen = self.__cpu_info_gen()
        for _info in _gen:
            _path = GetCpuFilePath()
            Formater.append_fo_file(_path,_info)
            self.__cpu_log_count +=1
            if self.__cpu_log_count >= 360:
                NewCpuFilePath()
                self.__cpu_log_count =0
                continue

    def __cpu_info_gen(self):
        while True:
            data = {
                    "time":time.strftime('%Y-%m-%d %X', time.localtime()),
                    "cpu_percent":psutil.cpu_percent(),
                    "memory":psutil.virtual_memory().used
            }
            time.sleep(5)
            yield str(data)+"\n"
    
class GpuWatcher(Process):
    def __init__(self, name=""):
        # Process.__init__(self) 
        super(GpuWatcher,self).__init__()
        self.daemon = True  
        if name:
            self.name = name
        self.__gpu_log_count = 0

    def run(self):
        print("Start Gpu Watching Process:", self.name)
        self.__gpu_watch_loop()
        print("Exiting Gpu Watching Process:", self.name)

    def __gpu_watch_loop(self):
        _n_gen = NewGpuFilePath()
        time.sleep(0.1)
        _i_gen = self.__gpu_info_gen()
        for _ in _n_gen:
            for info in _i_gen:
                path = PM["gpu_file_path"]
                Formater.append_fo_file(path=path,sth=info)
                if self.__gpu_log_count >= 360:
                    self.__gpu_log_count = 0
                    break

    def __gpu_info_gen(self):
        try:
            pynvml.nvmlInit()
            device_count = pynvml.nvmlDeviceGetCount()
            while True:
                device_status =[]
                for i in range(device_count):
                    handle = pynvml.nvmlDeviceGetHandleByIndex(i)
                    gpu_percent = pynvml.nvmlDeviceGetUtilizationRates(handle)
                    gpu_memory = pynvml.nvmlDeviceGetMemoryInfo(handle)
                    status = {"time":Formater.format_time(),"gpu_percent":gpu_percent.gpu,"gpu_memory":gpu_memory.used}
                    device_status.append(status)
                yield str(device_count)
                time.sleep(5)
        except:
            print("No Nvidia GPU Or Bad Driver Version")
            yield ""
                       

def NewCpuWatcher():
    w = CpuWatcher()
    return w

def NewGpuWatcher():
    w = GpuWatcher()
    return w
