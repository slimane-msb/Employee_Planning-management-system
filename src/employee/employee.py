from datetime import datetime
from datetime import timedelta

from src.shift.ShiftList import ShiftList
from src.shift.shift import Shift


class Employee:

    def __init__(self, name, lastname):
        self.name = name
        self.last_name = lastname
        self.shift_list = ShiftList()
        self.contract_start = None
        self.last_day = None
        self.contract_total = None
        self.work_balance_type = True
        self.total = timedelta()

    def __str__(self) -> str:
        res = self.name + " " + self.last_name
        res += str(self.shift_list)
        return res

    def save_in_csv(self):
        print(self)
        try:
            f = open("../output/csv/" + self.last_name + "_" + self.name + ".csv", "w+")
            f.write(self.shift_list.__repr__())
            f.close()
        except FileNotFoundError as fnfe:
            print("FileNotFoundError")

    def add_shift(self, shift: Shift):
        self.shift_list.add_shift(shift)
        self.update_total(shift)

    def add_list_shift(self, shifts):
        for shift in shifts:
            self.add_shift(shift)

    def update_total(self, shift):
        self.total += shift.length


    def get_hours_per_day(self):
        """

        :return: timedelta we have to work per day
        """
        time_float = self.contract_total / 4.33 / 7
        hours = int(time_float)
        min = int((time_float - hours)*60)
        return timedelta(hours=hours, minutes=min)

    def number_of_day_until_date(self, date):
        return (date - self.contract_start).days

    def get_balance(self, last_day):
        return self.total - (self.get_hours_per_day() * self.number_of_day_until_date(last_day))

    def fix_absence(self):
        for shift in self.shift_list.shifts:
            if shift.title == "Absence Autorisée":
                self.total -= shift.length


