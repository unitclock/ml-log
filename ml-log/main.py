
from mllogger.mllogger import NewLogger
import sys
print(sys.version_info > (3,6))
import time
import multiprocessing

def main():
    multiprocessing.freeze_support()
    l = NewLogger(
    #此处录入配置文件信息：如access_token，项目id，项目描述
    config={
    'access_token':"eyJhbGciOiJIUzI1NiIsInppcCI6IkdaSVAifQ.H4sIAAAAAAAAAKtWKi5NUrJS8kotcSwtyff1UdJRSq0oULIyNLO0MLMwNDMw0FEqLU4t8kwBipkDRS0NTA0sjA2NjQxNLM0tIJJ-ibmpQEMyShPz0itKU_Lz0pVqAV0AZlNaAAAA.IsqnyZC_OLIU-jTzEJ1QSfrVD7efzmKAxCaLq2bvQf0",
    'project':"907", 
    "description":"description ， 111",
    "experiment_name":"experiment_name 111",
    "repository_id":"e4107e9add2646d9b85a6a4c9fa43136"
    },
    #此处录入实验超参数
    info={
    "learnning_rate":0.02,
    "epoch":3,
    "batch_size":8
    }
    )
    for t in range(3):
        l.Run()
        for i in range(4):
                time.sleep(2)
                l.Log({"acc":0.9})
        l.End()

    l.Submit()



if __name__ == "__main__":

     main()
