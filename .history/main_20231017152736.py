class Logger():

    def __init__(self) -> None:

        self.__loadSavePath = "http://127.0.0.1:5560/ml_client/client/loadSavePath"
        self.__noticeExperiment = "http://127.0.0.1:5560/ml_client/client/noticeExperiment"
        self.__noticeRun = "http://127.0.0.1:5560/ml_client/client/noticeRun"

        print("验证代理客户端状态 \n")

        try:
            # resp  = requests.get(utl=self.__loadSavePath)
            print("开发阶段跳过校验 \n")
        except:
            raise BaseException("代理客户端未启动,请重新检查\n")
        else:
            print("代理客户端验证通过 \n")
            self.__login = True
            self.__location = "."
            self.__savedir = "code"
            self.__codedir = "src"
            self.__srcignore = "datasets"


        i = 0
        while os.path.exists(f"run-{i}"):
            i+=1
        self.__uid = f"run-{i}"


        if os.path.exists(self.__location) :
            print(f"创建本次运行记录，记录位置：{self.__location}/{self.__uid} \n")
            os.makedirs(self.__location+f"/{self.__uid}",mode=0o777)
        else:
            print(f"目录 {self.__location} 不存在,将自动创建 \n")
            os.makedirs(self.__location+f"/{self.__uid}",mode=0o777)
        self.__trainning_status  = {"epoch":[]}


        

    def Watcher(self):
        # 此函数需要子进程执行
        def WatchCPU()->None:
            os.makedirs(self.__location+f"/{self.__uid}/watcher",mode=0o777)
            with open(f"{self.__location}/{self.__uid}/watcher/cpu.log","w") as f:
                while True:
                    # f.write())
                    f.write( f"{ time.strftime('%Y-%m-%d %X', time.localtime())} {psutil.Process().cpu_percent()} {psutil.Process().memory_info().rss} \n")
                    f.flush()
                    time.sleep(1)
        watch_cpu = multiprocessing.Process(target=WatchCPU)
        watch_cpu.daemon = True
        watch_cpu.start()

        def WatchGPU()->None:
            os.makedirs(self.__location+f"/{self.__uid}/watcher",mode=0o777)
            with open(f"{self.__location}/{self.__uid}/watcher/gpu.log","w") as f:
                while True:
                    # f.write())
                    f.write( f"{ time.strftime('%Y-%m-%d %X', time.localtime())} {psutil.Process().cpu_percent()} {psutil.Process().memory_info().rss} \n")
                    f.flush()
                    time.sleep(1)

    def Start(self,info:dict) ->None:
        self.Watcher()
        try:

            now = time.strftime("%Y-%m-%d %X", time.localtime())
            print(f"运行开始时间：{now} \n")
            self.__trainning_status["start_at"] = now

            device_list =[]

            try:
                print("获取Nvidia显卡信息......")
                pynvml.nvmlInit()
                device_count=pynvml.nvmlDeviceGetCount()

                for i in range(device_count):
                    handle = pynvml.nvmlDeviceGetHandleByIndex(i)
                    device_list.append(str(pynvml.nvmlDeviceGetName(handle)))

            except:
                print("未获取到Nvidia显卡信息......")
            
            self.__NvidiaGPU= device_list

            try:
                self.__osinfo = {
                "plantform":platform.platform(),
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
                "nvidia_gpu_info":str(self.__NvidiaGPU)
                
            }
            except:
                 raise BaseException("系统信息采集失败")
            
            
            with open(f"{self.__location}/os_info.json","w") as f:
                f.write(str(json.dumps(self.__osinfo,indent=2)))

            with open(self.__location+"/"+self.__uid+"/super_arg.json",mode="w") as f:
                f.write(f"{json.dumps(info)}")
            return

        except:
            raise BaseException("日志实例启动失败\n")
        


        
    def EpochInit(self) ->None:
        

        return

    def EpochLog(self,info:dict) ->None:
        try:


            this_epoch = info
            self.__trainning_status["epoch"].append(this_epoch)

            with open(f"{self.__location}/{self.__uid}/results.json","w") as f:
                f.write(str(json.dumps(self.__trainning_status["epoch"],indent=2)))
                f.close()
            data ={
                    "plantform":platform.platform(),
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
                    "nvidia_gpu_info":str(self.__NvidiaGPU)
                }

            with open(f"{self.__location}/{self.__uid}/os_info.json","w") as osfile:
                osfile.write(str(json.dumps(data,indent=2)))
        except:
            raise BaseException("循环日志采集失败")
        return

    def End(self) ->None:
        now = time.strftime("%Y-%m-%d %X", time.localtime())
        print(f"运行结束时间：{now}\n")
        self.__trainning_status["end_at"] = now
        with open(self.__location+"/finish.tag",mode="a") as f:
            f.write(f"{now} | {self.__uid} \n")
        
        self.SaveCode()
        return
    
    def SaveCode(self)->None:
        try:

                shutil.copytree(src=self.__codedir,dst=self.__savedir,dirs_exist_ok=True)
        except:
            raise BaseException("备份代码失败,检查代码路径 \n")
        
        else:
            return
        
    def SuperArg(self,info:dict)->None:
        with open(self.__location+"/"+self.__uid+"/super_arg.json",mode="w") as f:
            f.write(f"{json.dumps(info)}")
        return

    def ShowStatus(self) -> str:
        return json.dumps(self.__trainning_status,indent=2)
    # 
