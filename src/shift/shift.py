from datetime import datetime, timedelta


class Shift:

    def __init__(self, date):
        self.date = date
        self.start_time = None
        self.end_time = None
        self.title = ""
        self.length = None

    def update_length(self):
        if self.end_time is None or self.start_time is None:
            self.length = None
        else:
            end = self.end_time
            if 0 <= end.hour <= 8:
                end = datetime(end.year, end.month, end.day+1, end.hour, end.minute, end.second)

            time_interval = end - self.start_time
            self.length = time_interval



    def add_start(self, start_time):
        """
         :param start_time: '18:30'
        """
        self.start_time = datetime.strptime(start_time + ":00", "%H:%M:%S")
        self.update_length()

    def add_end(self, end_time):
        """
        :param end_time: '18:30'
        """
        self.end_time = datetime.strptime(end_time + ":00", "%H:%M:%S")
        self.update_length()

    def add_title(self, title):
        self.title = title

    def __str__(self):
        return "shift done in "+str(self.date)+" from: "+str(self.start_time)+" until: "+str(self.end_time)+" it lasted = "+str(self.length) + " worked in: " + self.title

    def __repr__(self):
        date = self.date.strftime("%m/%d/%Y")
        start_time = self.start_time.strftime("%H:%M")
        end_time = self.end_time.strftime("%H:%M")
        return "{},{},{},{},{}".format(date, start_time, end_time, self.length, self.title)








