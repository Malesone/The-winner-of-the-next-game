import time

class Statistic:    
    def __init__(self, type):
        self.type = type
        self.time = time.time()
    
    def stop_time(self):
        self.time = (time.time()-self.time)/60

    def get_string(self):
        return "Time to " + str(self.type) + ": " + str(self.time) + " minutes"