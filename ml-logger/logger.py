import platform
import requests
import subprocess
import os
import time
import json
import psutil
import platform
import shutil
import pynvml
import multiprocessing
import yaml
from functools import wraps
import csv
import statistics
import sys
import io
import uuid

def NewLogger(conf:dict,info:dict):
    log = Logger(config=conf)
    log.Start(info=info)
    return log
        

def single(cls):
    _instance = {}
    @wraps(cls)
    def _single(*args,**kargs):
        # nonlocal _instance
        if cls not in _instance :
            _instance[cls] = cls(*args,**kargs) 
        else:
            pass
        return _instance[cls]
    return _single

def run_in_sub_process(func):
    @wraps(func)
    def _sub(*arg,**krags):
        
        pass
    return _sub

def get_os_info() ->dict:

    device = get_gpu_list()
    try:
        print("采集系统信息")
        info = {
                "hostname":platform.node(),
                "platform":platform.platform(),
                "system":platform.system(),
                "python_version":platform.python_version(),
                "architecture":platform.architecture()[0],
                "processor":platform.processor(),
                "uname":str(platform.uname()),
                "cpu_logical_count":psutil.cpu_count(),
                "cpu_count": psutil.cpu_count(logical=False),
                "total_memory": psutil.virtual_memory().total /100000,
                "active_memory": psutil.virtual_memory().active /100000,
                "available_memory": psutil.virtual_memory().available /100000,
                "total_swap_memory":psutil.swap_memory().total /100000,
                "nvidia_gpu_info":str(device),
                "python_path":sys.executable,
                "run_path":os.getcwd()
        }
    except:
        raise BaseException("系统信息采集失败")

    return info

def watch_cpu(main_pid:int,path:str)->None:
    try:
        os.makedirs(path,mode=0o777,exist_ok=True)
        sleep_time = 5
        i =0
        count = 0
        running = is_process_running(main_pid=main_pid)
        while running:
            with open(f"{path}/cpu-{count}.log","a") as f:
                while True:
    
                    running = is_process_running(main_pid=main_pid)
                    cpu_percent = psutil.Process(pid=main_pid).cpu_percent()
                    memory = psutil.Process(pid=main_pid).memory_info().rss
                    f.write(str({"time":time.strftime('%Y-%m-%d %X', time.localtime()),"cpu_percent":cpu_percent,"memory":memory})+"\n")
                    f.flush()
                    time.sleep(sleep_time)
                    i+=1
                    if i ==(1800/sleep_time):
                        i =0
                        break
            count +=1
            continue
    except:
        raise BaseException("cpu状态监控进程启动失败")
    return
    
def save_dict_to_json(dict_value:dict , save_path:str) ->None:
    with open(save_path, 'w') as file:
        file.write(json.dumps(dict_value, indent=2))
        file.flush()
    return

def save_dict_to_yaml(dict_value: dict, save_path: str):
    with open(save_path, 'w') as file:
        file.write(yaml.dump(dict_value, allow_unicode=True))
        file.flush()
    return

def read_yaml_to_dict(yaml_path: str):
    with open(yaml_path) as file:
        dict_value = yaml.load(file.read(), Loader=yaml.FullLoader)
        return dict_value
    
def save_list_to_csv(data_list:list, output_file:str)->None:
    headers = set()
    for item in data_list:
        headers.update(item.keys())

    with open(output_file, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        
        writer.writerow(headers)
        
        for item in data_list:
            row = [item.get(key, '') for key in headers]
            writer.writerow(row)
    return

def watch_gpu(main_pid:int,path:str)->None:
    
    try:
        os.makedirs(path,mode=0o777,exist_ok=True)
        pynvml.nvmlInit()
        sleep_time =5
        device_count = pynvml.nvmlDeviceGetCount()
        running = is_process_running(main_pid=main_pid)
        i =0
        count = 0
        while running:
            with open(f"{path}/gpu-{count}.log","w") as f:
                running = is_process_running(main_pid=main_pid)
                while running:
                    running = is_process_running(main_pid=main_pid)
                    device_status =[]

                    for i in range(device_count):
                        handle = pynvml.nvmlDeviceGetHandleByIndex(i)
                        gpu_percent = pynvml.nvmlDeviceGetUtilizationRates(handle)
                        gpu_memory = pynvml.nvmlDeviceGetMemoryInfo(handle)
                        status = {"time":time.strftime('%Y-%m-%d %X', time.localtime()),"gpu_percent":gpu_percent.gpu,"gpu_memory":gpu_memory.used}
                        device_status.append(status)
                    f.write(str(device_status)+"\n")
                    f.flush()
                    time.sleep(sleep_time)
                    i+=1
                    if i == 1800/sleep_time:
                        i = 0
                        break
                count+=1
                continue
    except:
        raise BaseException("gpu监控进程启动失败")

def is_process_running(main_pid:int) ->bool:
    try:
        ps = psutil.Process(pid=main_pid)
        return ps.is_running
    except:
        return False
    



def save_conda_info(path:str) ->bool:
    try:
        result = subprocess.run(['conda', 'list'], capture_output=True, text=True)
        output = result.stdout
        with open(f"{path}/conda.info","a") as file:
                file.write(output)
                file.flush()
        return True
    except:
        return False

def get_gpu_list() ->list:
    device_list =[]
    try:
        print("获取Nvidia显卡信息 \n")
        pynvml.nvmlInit()
        device_count=pynvml.nvmlDeviceGetCount()

        for i in range(device_count):
            handle = pynvml.nvmlDeviceGetHandleByIndex(i)
            device_list.append(str(pynvml.nvmlDeviceGetName(handle)))

    except:
        print("未获取到Nvidia显卡信息 \n")

def has_multiple_keys(dictionary:dict, *keys):
    return set(keys).issubset(dictionary.keys())



def get_init_trainning_status()->dict:
    return {"epoch":[],"next_start_at":0,"count":0}

def get_process_pid():
    return os.getpid()

def get_all_recorded_element(data)->list:
    elemet_list = []
    for d in data :
        elemet_list.extend(list(d.keys()))
    result = list(set(elemet_list))
    print(result)
    return result
    
def quick_analysis(status:list) ->dict:
    result = {}
    element_list = get_all_recorded_element(status)
    for e in element_list:
        result[e] = []
        for s in status:
            if e in s.keys():
                result[e].append(s[e])
        result[e+"_max"] = max(result[e])
        result[e+"_min"] = min(result[e])
        result[e+"_viriance"]=statistics.variance(result[e])
        result[e+"_stdev"]=statistics.variance(result[e])
        result[e+"_avg"] = statistics.mean(result[e])
    
    return result
                
                                           
    
    
    
    
@single
class Logger():
    def __init__(self,config:dict,host="127.0.0.1") -> None:

        if not has_multiple_keys(config, 'access_token', 'project',"discription"):
            raise BaseException("缺失启动信息,请补充config参数")
        
        config["experiment"] = str(uuid.uuid4())
        
        self.__config = config
        print("验证代理客户端状态 \n")
        self.__verify_my_client()
        self.__save_config()

        self.__pid = get_process_pid()

        self.__api_load_save_path = f"http://{host}:5560/ml_client/client/loadSavePath"
        self.__api_notice_experiment = f"http://{host}:5560/ml_client/client/noticeExperiment"
        self.__api_notice_run = f"http://{host}:5560/ml_client/client/noticeRun"
        

        self.__trainning_status  = get_init_trainning_status()
        self.__watcher()

        
    def __verify_my_client(self) ->None:
        try:
            # resp  = requests.get(utl=self.__loadSavePath)
            print("开发阶段跳过校验 \n")
        except:
            raise BaseException("用户校验失败，请检查客户端是否启动\n")
        else:
            print("代理客户端验证通过 \n")
            self.__login = True
            self.__location = f".location/{self.__config['experiment']}"
            self.__savedir = f".{self.__config['experiment']}/code"
            self.__codedir = "src"
            self.__srcignore = "datasets"
            i = 0
            self.__epochid = f"run-{i}"
            
            while os.path.exists(f"{self.__location}/run-{i}"):
                i+=1
                self.__epochid = f"run-{i}"

        os.makedirs(f"{self.__location}/{self.__epochid}",mode=0o777,exist_ok=True)
        return

    def __watcher(self) ->None:
        cpu_dir =f"{self.__location}/watcher/cpu"
        self.__watcher_cpu = multiprocessing.Process(target=watch_cpu ,daemon=True, args=(self.__pid,cpu_dir))
        self.__watcher_cpu.start()

        gpu_dir =f"{self.__location}/watcher/gpu"
        self.__watcher_gpu = multiprocessing.Process(target=watch_gpu,daemon=True, args=(self.__pid,gpu_dir))
        self.__watcher_gpu.start()

        return

    def Start(self,info:dict) ->None:

        if not save_conda_info(self.__location):
            print("未采集到conda信息")

        try:
            now = time.strftime("%Y-%m-%d %X", time.localtime())
            print(f"运行开始时间：{now} \n")
            self.__trainning_status["start_at"] = now

            self.__osinfo = get_os_info()
            
            os_info_json_path =f"{self.__location}/os_info.json"
            os_info_yaml_path =f"{self.__location}/os_info.yaml"

            save_dict_to_json(self.__osinfo,os_info_json_path)
            save_dict_to_yaml(self.__osinfo,os_info_yaml_path)
            
            super_arg_json_path = self.__location+"/super_arg.json"
            super_arg_yaml_path = self.__location+"/super_arg.yaml"

            save_dict_to_json(info,super_arg_json_path)
            save_dict_to_yaml(info,super_arg_yaml_path)
            
            with open(f"{self.__location}/start.tag",mode="w") as f:
                f.write(f"{now} | {self.__epochid} \n")
                f.flush()
                
            # self.__stdout = sys.stdout
            # self.__stderr = sys.stderr

            # self.__console = open(f"{self.__location}/console.log","w")
        
            # sys.stdout = self.__console
            # sys.stderr = self.__console
            if os.path.exists("./requirements.txt"):
                shutil.copy("./requirements.txt",f"{self.__location}")
            
        except:
            raise BaseException("日志实例启动失败\n")

        else:
            pass
        return
        
        
    def SaveFile(self,path_list:list) ->None:
        os.makedirs(f"{self.__location}/{self.__epochid}/files",exist_ok=True)
        for path in path_list:
            if os.path.exists(path):
                shutil.copy(path,f"{self.__location}/{self.__epochid}/files")
        return
    
        
    def EpochStart(self) ->None:
        now = time.strftime("%Y-%m-%d %X", time.localtime())
        
        with open(f"{self.__location}/{self.__epochid}/start.tag",mode="w") as f:
            f.write(f"{now} | {self.__epochid} \n")
            f.flush()

        #通知客户端开始
        
        return

    def EpochLog(self,info:dict) ->None:
        
        self.__trainning_status["count"] += 1

        try:
            this_epoch = info
            self.__trainning_status["epoch"].append(this_epoch)
                
            #通知客户端结束
        except:
            raise BaseException("Epoch日志采集失败")
        
        return
    
    def EpochEnd(self) ->None:
        
        i=0
        while os.path.exists(f"{self.__location}/run-{i}"):
            i+=1
            self.__epochid = f"run-{i}"
        
        os.makedirs(f"{self.__location}/{self.__epochid}",exist_ok=True)
        
        result_path =f"{self.__location}/{self.__epochid}/results.json"
    
        save_dict_to_json(self.__trainning_status["epoch"][self.__trainning_status["next_start_at"]:self.__trainning_status["count"]],result_path)
        
        self.__trainning_status["next_start_at"] = self.__trainning_status["count"]

        return
    
    
    def End(self) ->None:
        now = time.strftime("%Y-%m-%d %X", time.localtime())
        print(f"运行结束时间：{now}\n")
        self.__trainning_status["end_at"] = now
        with open(f"{self.__location}/"+"/finish.tag",mode="a") as f:
            f.write(f"{now} | {self.__epochid} \n")
            f.flush()
        with open(f"{self.__location}/finish.tag",mode="w") as f:
            f.write(f"{now} | {self.__epochid} \n")
            f.flush()
        self.__save_code()
        self.__watcher_cpu.kill()
        self.__watcher_gpu.kill()
        
        result_csv_path = f"{self.__location}/result.csv"
        save_list_to_csv(self.__trainning_status["epoch"],result_csv_path)
        dict = quick_analysis(status=self.__trainning_status["epoch"])
        analysis_json_path = f"{self.__location}/analysis.json"
        analysis_yaml_path = f"{self.__location}/analysis.yaml"
        save_dict_to_json(dict,analysis_json_path)
        save_dict_to_yaml(dict,analysis_yaml_path)
        

        
        return
    
    def __save_config(self) ->None:
        try:
            config_path_json = self.__location +"/"+"config.json"
            save_dict_to_json(self.__config,config_path_json)
            config_path_yaml = self.__location +"/"+"config.yaml"
            save_dict_to_yaml(self.__config,config_path_yaml)
        except:
            raise BaseException("保存配置信息失败 \n")
        return

    def __save_code(self,path=["datasets"])->None:
        ignore_path = [*path]
        try:
            if os.path.exists(".path_ignore"):
                with open(".path_ignore") as f:
                    line =  f.readline()
                    while line:
                        ignore_path.append(line.strip())
                        line = f.readline()
            shutil.copytree(src=self.__codedir,dst=self.__savedir,dirs_exist_ok=True,ignore=shutil.ignore_patterns(*ignore_path))
        except:
            raise BaseException("备份代码失败 \n")
        else:
            return


    #废弃方法，请从Start()接口输入超参数    
    def SuperArg(self,info:dict)->None:
        path =self.__location+"/"+self.__epochid+"/super_arg.json"
        with open(path,mode="w") as f:
            f.write(f"{json.dumps(info)}")
        return

    #ShowStatus ：仅开发过程使用
    def ShowStatus(self) -> str:
        return json.dumps(self.__trainning_status["epoch"],indent=2)
    
