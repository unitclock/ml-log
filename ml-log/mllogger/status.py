class Status():
    def __init__(self,config:dict) ->None:
        self.config = config
        return

def NewStatus(config:dict) ->Status:
    return Status(config=config)