from datetime import datetime


class ShiftList:

    def __init__(self):
        self.shifts = []

    def add_shift(self, shift):
        self.shifts.append(shift)

    def remove_shift(self, shift):
        self.shifts.remove(shift)

    def __str__(self):
        res = ""
        for shift in self.shifts:
            res += "\t" + str(shift) + "\n"
        return res

    def __repr__(self):
        res = "{},{},{},{},{}\n".format("date", "start time", "end time", "duration", "shift title")
        for shift in self.shifts:
            res += shift.__repr__() + "\n"
        return res

