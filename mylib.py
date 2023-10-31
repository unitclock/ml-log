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
import random

def single(cls):
    _instance = {}
    @wraps(cls)
    def _single(*args,**kwargs):
        # nonlocal _instance
        if cls not in _instance :
            _instance[cls] = cls(*args,**kwargs) 
        else:
            pass
        return _instance[cls]
    return _single

def run_as_daemon(func):
    @wraps(func)
    def _process(*arg,**kwargs):
        p    = multiprocessing.Process(target=func,args=arg,kwargs=kwargs,daemon=True)
        p.start()
        return p
    return _process

def get_os_info() ->dict:

    device = get_gpu_list()
    try:
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

@run_as_daemon
def watch_cpu(path:str):
    os.makedirs(path,mode=0o777,exist_ok=True)
    sleep_time = 5
    cut_time =1800
    i =0
    count = 0
    while True:
        with open(f"{path}/cpu-{count}.log","a") as f:
            while True:
                cpu_percent = psutil.cpu_percent()
                memory = psutil.virtual_memory().used
                f.write(str({"time":time.strftime('%Y-%m-%d %X', time.localtime()),"cpu_percent":cpu_percent,"memory":memory})+"\n")
                f.flush()
                time.sleep(sleep_time)
                i+=1
                if i ==(cut_time/sleep_time):
                    i =0
                    break
        count +=1
        continue
    
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

@run_as_daemon
def watch_gpu(path:str)->None:
        os.makedirs(path,mode=0o777,exist_ok=True)
        pynvml.nvmlInit()
        sleep_time =5
        device_count = pynvml.nvmlDeviceGetCount()
        i =0
        count = 0
        while True:
            with open(f"{path}/gpu-{count}.log","a") as f:
                while True:
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
        pynvml.nvmlInit()
        device_count=pynvml.nvmlDeviceGetCount()

        for i in range(device_count):
            handle = pynvml.nvmlDeviceGetHandleByIndex(i)
            device_list.append(str(pynvml.nvmlDeviceGetName(handle)))
    except:
        print("未获取到Nvidia显卡信息 \n")
    return device_list

def has_multiple_keys(dictionary:dict, *keys):
    return set(keys).issubset(dictionary.keys())



def get_init_trainning_status()->dict:
    return {"epoch":[],"next_start_at":0,"count":0}

def get_process_pid() -> int:
    return os.getpid()

def get_all_recorded_element(data)->list:
    elemet_list = []
    for d in data :
        elemet_list.extend(list(d.keys()))
    result = list(set(elemet_list))
    return result
    
def quick_analysis(status:list) ->dict:
    result = {}
    element_list = get_all_recorded_element(status)
    for e in element_list:
        result[e] = {}
        origin_list = []
        for s in status:
            if e in s.keys():
                origin_list.append(s[e])
        result[e]["max"] = max(origin_list)
        result[e]["min"] = min(origin_list)
        result[e]["viriance"]=statistics.variance(origin_list)
        result[e]["stdev"]=statistics.stdev(origin_list)
        result[e]["avg"] = statistics.mean(origin_list)

    return result

def format_time() ->str:
    return time.strftime("%Y-%m-%d %X", time.localtime())

def timestamp() ->str:
    return time.strftime("%Y%m%d%H%M%S", time.localtime())
                
def copy_file_to_dir(srcfile,dstpath):                       # 复制函数
    if not os.path.isfile(srcfile):
        print ("%s not exist!"%(srcfile))
    else:
        fpath,fname=os.path.split(srcfile)             # 分离文件名和路径
        if not os.path.exists(dstpath):
            os.makedirs(dstpath)                       # 创建路径
        shutil.copy(srcfile, dstpath + fname)          # 复制文件

def get_experiment_id() -> str:

    digits = [str(random.randint(0, 9)) for _ in range(15)]

    result = "".join(digits)
    return  result 
    
def api(url:str,data:dict) ->dict:
    header = {'Content-Type': 'application/json'}
    resp = requests.post(url=url,headers=header,json=data)
    print(f"{format_time()} {data} {url}")
    msg =dict(resp.json())
    print(f"{format_time()} {msg} ")
    return msg
    
def append_fo_file(path:str,sth:str):
    with open(path,"a") as file:
            file.write(sth)
            file.flush()
    return    


def NewLogger(conf:dict,info:dict):
    log = Logger(config=conf)
    log.Start(info=info)
    return log


class Printer():
        def __init__(self,run_path:str) ->None:
            if os.path.exists(run_path):
                self.__location = run_path
                append_fo_file(self.__location,f"console init {format_time()}")
            return
        
        def Print(self,sth:str):
            append_fo_file(self.__location,sth=sth)
            return

@single
class Logger():
    def __init__(self,config:dict) -> None:

        if not has_multiple_keys(config, 'access_token', 'project',"description","experiment_name"):
            raise BaseException("缺失启动信息,请补充config参数: access_token project description experiment ;可选配置项: repository_id")
        config["experiment_id"] = get_experiment_id()
        self.__config = config
        self.__config["experiment_name"] = f'{self.__config["experiment_name"]}-{timestamp()}'
        self.__verify_my_client()
        self.__save_config()

        self.__trainning_status  = get_init_trainning_status()
        return

    def Print(self,sth:str):
        save_path =f"{self.__location}/{self.__runid}/console.log"
        append_fo_file(path=save_path,sth=sth)            
        pass

        
    def __verify_my_client(self,host="127.0.0.1") ->None:

        self.__api_load_save_path = f"http://{host}:5560/ml_client/client/loadSavePath"
        self.__api_notice_experiment = f"http://{host}:5560/ml_client/client/noticeExperiment"
        self.__api_notice_run = f"http://{host}:5560/ml_client/client/noticeRun"

        try:

            send_data={}
            send_data["userToken"] = self.__config["access_token"]
            send_data["projectId"] = self.__config["project"]
            send_data["description"] = self.__config["description"]
            send_data["experimentName"] = self.__config["experiment_name"]
            try:
                send_data["repositoryId"] = self.__config["repository_id"]
            except:
                pass

            msg =api(url=self.__api_load_save_path,data=send_data)
            if not msg["code"] == 200:
                raise ConnectionError
            self.__location = msg["data"]
        except:
            raise ConnectionError
        else:
            self.__location = f"{self.__location}/{self.__config['experiment_id']}"
            self.__savedir = f"{self.__location}/code"
            self.__codedir = os.getcwd()
            i = 0
            self.__runid = f"run-{i}"

        os.makedirs(f"{self.__location}",mode=0o777,exist_ok=True)
        return

    def __watcher(self) ->None:
        cpu_dir =f"{self.__location}/{self.__runid}/watcher/cpu"
        self.__watcher_cpu = watch_cpu(path=cpu_dir)
        gpu_dir =f"{self.__location}/{self.__runid}/watcher/gpu"
        self.__watcher_gpu = watch_gpu(path=gpu_dir)
        return

    def Start(self,info:dict) ->None:

        if not save_conda_info(self.__location):
            print("未采集到conda信息")
        try:
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
                f.write(f"{format_time()} | {self.__runid}\n")
                f.flush()
            if os.system("pip freeze > requirements.txt") == 0:
                if os.path.exists("./requirements.txt"):
                    shutil.copy("./requirements.txt",f"{self.__location}")    
            send_data = {
                        "experimentId":self.__config["experiment_id"],
                        "status":0
                        }
            self.__save_code()
            resp = api(url=self.__api_notice_experiment,data=send_data)
            if not resp["code"] == 200:
                raise ConnectionError      
        except:
            raise BaseException("日志实例启动失败\n")
        return
    
    def Save(self,path_list:list):
        for path in path_list:
            if os.path.exists(path):
                file_name = os.path.basename(path)
                copy_file_to_dir(file_name,f"{self.__location}/{self.__runid}/files/")
                with open(f"{self.__location}/{self.__runid}/file.tag","a") as f:
                    f.write(f"files/{file_name}\n")
                    f.flush()
        return
        
    def Run(self) ->None:

        os.makedirs(f"{self.__location}/{self.__runid}",exist_ok=True)

        with open(f"{self.__location}/{self.__runid}/start.tag",mode="w") as f:
            f.write(f"{format_time()} | {self.__runid}\n")
            f.flush()

        #通知客户端开始
        send_data ={
                        "experimentId":self.__config["experiment_id"],
                        "runName": self.__runid,
                        "status": 0
                    }
        
        resp = api(url=self.__api_notice_run,data=send_data)
        if not resp["code"] == 200:
            raise ConnectionError

        self.__watcher()
            
        return

    def Log(self,info:dict) ->None:
        try:
            self.__trainning_status["count"] += 1
            self.__trainning_status["epoch"].append(info)
        except:
            raise BaseException("Epoch日志采集失败")
        return 
    
    def End(self) ->None:

        
        send_data ={
                        "experimentId":self.__config["experiment_id"],
                        "runName": self.__runid,
                        "status": 1
                    }
        resp = api(url=self.__api_notice_run,data=send_data)
        if not resp["code"] == 200:
            raise ConnectionError
        result_path =f"{self.__location}/{self.__runid}/results.json"
        save_dict_to_json(self.__trainning_status["epoch"][self.__trainning_status["next_start_at"]:self.__trainning_status["count"]],result_path)
        result_csv_path=f"{self.__location}/{self.__runid}/results.csv"

        dict = quick_analysis(status=self.__trainning_status["epoch"][self.__trainning_status["next_start_at"]:self.__trainning_status["count"]])
        analysis_json_path = f"{self.__location}/{self.__runid}/analysis.json"
        analysis_yaml_path = f"{self.__location}/{self.__runid}/analysis.yaml"
        save_dict_to_json(dict,analysis_json_path)
        save_dict_to_yaml(dict,analysis_yaml_path)

        save_list_to_csv(self.__trainning_status["epoch"][self.__trainning_status["next_start_at"]:self.__trainning_status["count"]],result_csv_path)
        self.__trainning_status["next_start_at"] = self.__trainning_status["count"]
        last = self.__trainning_status["epoch"][len(self.__trainning_status["epoch"])-1]
        last_result_path = f"{self.__location}/{self.__runid}/last.json"
        save_dict_to_json(last,last_result_path)


        self.__kill_watcher()

        i=0
        while os.path.exists(f"{self.__location}/run-{i}"):
            i+=1   
        with open(f"{self.__location}/{self.__runid}/finish.tag",mode="a") as f:
            f.write(f"{format_time()} | {self.__runid} \n")
            f.flush()     
        self.__runid = f"run-{i}"
        return
    
    def __kill_watcher(self):
        self.__watcher_cpu.kill()
        self.__watcher_gpu.kill()
        return
    
    def Submit(self) ->None:
        try:
            send_data = {
                            "experimentId":self.__config["experiment_id"],
                            "status":1
                        }

            resp = api(url=self.__api_notice_experiment,data=send_data)
            if not resp["code"] == 200:
                raise ConnectionError

            # result_csv_path = f"{self.__location}/result.csv"
            # save_list_to_csv(self.__trainning_status["epoch"],result_csv_path)

            dict = quick_analysis(status=self.__trainning_status["epoch"])
            analysis_json_path = f"{self.__location}/analysis.json"
            analysis_yaml_path = f"{self.__location}/analysis.yaml"
            save_dict_to_json(dict,analysis_json_path)
            save_dict_to_yaml(dict,analysis_yaml_path)
            
            with open(f"{self.__location}/finish.tag",mode="a") as f:
                f.write(f"{format_time()} | finish \n")
                f.flush() 

        except:
            raise BaseException("END ERROR")
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
        return