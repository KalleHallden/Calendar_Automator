

import datetime

class Task:
    total_time = 0
    date = datetime.datetime.now()

    def __init__(self, name, start_time, end_time, color):
        self.name=name
        self.start_time=start_time
        self.end_time=end_time
        self.color=color

    def get_time_of_task(self):
        start = self.start_time.split(":")
        end = self.end_time.split(":")
        start_hour = self.make_int(str(start[0]))
        start_minutes = self.make_int(str(start[1]))
        
        end_hour = self.make_int(str(end[0]))
        end_minutes = self.make_int(str(end[1]))

        start_is_greater = False
        extra = 0

        if start_minutes > 0:
            start_hour+=1
            start_is_greater = True

        time = end_hour-start_hour
        if time < 0:
            time = time*-1
        if start_is_greater:
            extra = 60-start_minutes
        time = ((time*60) + extra + end_minutes)/60.0
        self.total_time = time
    
    def make_int(self,time):
        arr = []
        for line in time:
            if line.strip(): 
                try:           # line contains eol character(s)
                    n = int(line) 
                    arr.append(n) 
                except Exception as e:
                    pass 
        hour_string = str(arr[0]) + str(arr[1])
        int_hour = int(hour_string)
        return int_hour