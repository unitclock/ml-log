from .utils import single,format_time
from .quene import Quene
from multiprocessing import Queue, Value ,Manager
import os


PM = Manager().dict()

def GetPM():
    return PM

def NewStoragePath(sp:str) ->None:
    PM["storage_path"] =sp
    os.makedirs(name=PM["storage_path"],mode=0o777,exist_ok=True)
    os.makedirs(name=PM["storage_path"]+"/code",mode=0o777,exist_ok=True)
    #print(f"Storage Path: {sp}")
    return 

def GetStoragePath() ->str:
    sp = PM["storage_path"]
    return sp

def NewRunPath() ->None:
    try:
        if not "run_count" in PM.keys():
            PM["run_count"] = 0 
            PM["run_path"] = PM["storage_path"]+f"/run-{PM['run_count']}"
        else:
            PM["run_count"]  = PM["run_count"] +1
            PM["run_path"] = PM["storage_path"]+f"/run-{PM['run_count']}"
        run_path = PM["run_path"]
        os.makedirs(name=run_path,mode=0o777,exist_ok=True)
        PM["cpu_path"] = run_path+"/watcher/cpu"
        os.makedirs(name=run_path+"/watcher/cpu",mode=0o777,exist_ok=True)
        PM["gpu_path"] = run_path+"/watcher/gpu"
        os.makedirs(name=run_path+"/watcher/gpu",mode=0o777,exist_ok=True)
        os.makedirs(name=run_path+"/files",mode=0o777,exist_ok=True)
        with open(run_path+"/start.tag","a") as file:
            file.write(format_time())
            file.flush()
    except:
        raise InterruptedError("Storage Path Error")
    return

def GetRunPath()->str:
    rp = PM["run_path"]
    return rp

def GetRunCount() ->int:
    rc = PM["run_count"]
    return rc

def NewCpuFilePath() ->str:
    if not "cpu_file_count" in PM.keys():
        PM["cpu_file_count"] = 0
        rc = PM['run_count'] 
        sp = PM["storage_path"]
        PM["cpu_file_path"] = f"{sp}/run-{rc}/watcher/cpu/cpu-0"
    else:
        PM["cpu_file_count"]  = PM["cpu_file_count"] +1
        rc = PM['run_count'] 
        sp = PM["storage_path"]
        PM["cpu_file_path"] = f"{sp}/run-{rc}/watcher/cpu/cpu-{PM['cpu_file_count']}"
    cp = PM["cpu_path"]
    if not os.path.exists(cp):
        os.makedirs(cp,mode=0o777,exist_ok=True)
    cfp = PM["cpu_file_path"]
    with open(cfp,"w"):
        pass
    return cfp
def GetCpuFilePath()->str:
    cfp = PM["cpu_file_path"] 
    return cfp

def GetCpuPath()->str:
    cp = PM["cpu_path"]
    return cp

def GetGpuPath()->str:
    gp = PM["gpu_path"]
    return gp

def NewGpuFilePath():
    count = 0 
    while True:
        gp = GetGpuPath()
        gfp =f"{gp}/gpu-{count}"
        PM["gpu_file_path"] = gfp
        yield gfp
        count +=1

def GetGpuFilePath() ->str:
    gfp = PM["gpu_file_path"]
    return gfp